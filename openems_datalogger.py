import config
import requests
import time
import logging as logger
import db_module as db
from datetime import datetime


def get_current_time():
    date_time_obj = datetime.now()
    timestamp_str = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp_str


class OpenEMSClient:
    def __init__(self, address):
        """
        Create client that connects to OpenEMS.

        :param address: OpenEMS REST/JSON websocket address
        :type openems_config: string
        """
        self.address = address

    def getValue(self, componentId, channel):
        """
        read out a single OpenEMS channel value

        :param componentID: selects component
        :type componentID: string
        :param channel: selects channel from component
        :type channel: string
        :return: channel value (or None on error)
        :rtype: channel-dependant
        """
        r = requests.get("{}/rest/channel/{}/{}".format(self.address, componentId, channel))
        if r.status_code != 200:
            # GET request returns HTML page
            logger.error(f"Response {r.status_code} ({r.reason})")
            return None
        return r.json().get("value")

    def setValue(self, componentId, channel, value):
        """
        set channel value

        :param componentId: component to update
        :type componentId: string
        :param channel: channel to update
        :type channel: string
        :param value: value to set
        :type value: any
        """
        r = requests.post("{}/rest/channel/{}/{}".format(self.address, componentId, channel), json={'value': value})
        if r.status_code != 200:
            logger.error(f"Response {r.status_code}: {r.json()['error']['message']}")


if __name__ == "__main__":

    # todo: create a new sqlite database if not exists
    # todo: th timcreate a new table wiestamp and channels_names as table columns (a new table is created with a random name everytime the script is run)
    # table column names = keys from the dictionary
    # functions to create a table

    # initialize OpenEMS to read channel values
    openems_address = "http://{}:{}@{}:{}".format(
        config.OPENEMS_USERNAME, config.OPENEMS_PASSWORD,
        config.OPENEMS_IP, config.OPENEMS_PORT)
    # IP of backend running on localhost
    client = OpenEMSClient(openems_address)

    conn = db.create_db()
    db.create_table(conn)

    while True:
        try:
            for channelname in config.CHANNELS_TO_LOG:
                componentID = config.CHANNELS_TO_LOG[channelname]
                channelValue = client.getValue(componentID, channelname)
                print(channelname, channelValue)  # Save to the DB
                log = (componentID, channelname, channelValue, get_current_time())
                db.save_to_db(conn, log)
                db.read(conn)
            # insert the values of all the channels in to the database

            time.sleep(config.LOGTIME)
        except Exception as e:
            print(e)

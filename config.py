OPENEMS_IP = "localhost"
OPENEMS_PORT = 8084
OPENEMS_USERNAME = "user"
OPENEMS_PASSWORD = "user"

#SQLITE_DB_NAME= "openEMSLogger"

LOGTIME = 10 #how often to log channel values (in seconds)
CHANNELS_TO_LOG = {'ConsumptionW': 'ctrlio.openems.edge.controller.sonnenbattery0',
                   'ProductionW': 'ctrlio.openems.edge.controller.sonnenbattery0'} #give "channel_name": "component_id" as keyvalue pairs

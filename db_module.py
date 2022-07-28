import sqlite3
import random
import string

'''
def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    print(result_str)
    return result_str
'''

file = 'LogsDB'

def create_db():
    conn = None
    try:
        conn = sqlite3.connect(file)
        print("Database formed.")
    except:
        print("Database not formed.")
    return conn


def create_table(conn):
    with conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS logs(
                            id INTEGER PRIMARY KEY,
                            component TEXT,
                            channel TEXT,
                            log_value TEXT,
                            log_timestamp TEXT
                    )"""
        )

        conn.commit()


def save_to_db(conn, log):
    """
     Create a new log
     :param conn:
     :param log:
     :return:
     """

    sql = ''' INSERT INTO logs(component, channel, log_value, log_timestamp)
               VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, log)
    conn.commit()
    return cur.lastrowid


def read(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs")
        rows = cur.fetchmany(10)

        print(rows)

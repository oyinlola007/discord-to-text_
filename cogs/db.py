import sqlite3

import cogs.config as config

conn = sqlite3.connect(config.DATABASE_NAME)

def initializeDB():
    try:
        conn.execute('''CREATE TABLE PHONE_RECORDS
                 (DISCORD_ID TEXT PRIMARY KEY NOT NULL,
                 PHONE TEXT);''')
    except:
        pass

    try:
        conn.execute('''CREATE TABLE CHANNEL_TO_ROLE
                 (CHANNEL_ID TEXT PRIMARY KEY NOT NULL,
                 ROLE_NAME TEXT);''')
    except:
        pass

    insert_channel_to_role("789644995904798750", "Shark Alerts")
    insert_channel_to_role("854496771932946433", "Printing Alerts")
    insert_channel_to_role("854797791045615646", "DT Alerts")
    insert_channel_to_role("855194259711721543", "Ben Alerts")
    insert_channel_to_role("866524824575017010", "Hostile Alerts")
    insert_channel_to_role("867617098636984350", "JPM Alerts")

    conn.commit()

def insert_phone(DISCORD_ID, PHONE):
    try:
        sqlite_insert_with_param = """INSERT INTO 'PHONE_RECORDS'
                ('DISCORD_ID', 'PHONE')
                VALUES (?, ?);"""

        data_tuple = (DISCORD_ID, PHONE)
        conn.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
    except:
        pass

def insert_channel_to_role(CHANNEL_ID, ROLE_NAME):
    try:
        sqlite_insert_with_param = """INSERT OR REPLACE INTO 'CHANNEL_TO_ROLE'
                ('CHANNEL_ID', 'ROLE_NAME')
                VALUES (?, ?);"""

        data_tuple = (CHANNEL_ID, ROLE_NAME)
        conn.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
    except:
        pass

def get_phone_count_for_user(DISCORD_ID):
    return conn.execute(f"SELECT COUNT(DISCORD_ID) FROM PHONE_RECORDS WHERE DISCORD_ID = '{DISCORD_ID}'").fetchone()[0]

def delete_phone(DISCORD_ID):
    conn.execute(f"DELETE FROM PHONE_RECORDS where DISCORD_ID = '{DISCORD_ID}'")
    conn.commit()

def is_channel_monitored(CHANNEL_ID):
    return conn.execute(f"SELECT COUNT(CHANNEL_ID) FROM CHANNEL_TO_ROLE WHERE CHANNEL_ID = '{CHANNEL_ID}'").fetchone()[0]

def get_channel_role(CHANNEL_ID):
    return conn.execute(f"SELECT ROLE_NAME FROM CHANNEL_TO_ROLE WHERE CHANNEL_ID = '{CHANNEL_ID}'").fetchone()[0]

def get_all_phone_records():
    return conn.execute(f"SELECT * FROM PHONE_RECORDS")







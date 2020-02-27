import mysql.connector
import numpy as np
import pandas

from utils.essentials import functions

config = functions.get("utils/config.json")
global mydb


def createConnection():
    global mydb
    mydb = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_pass,
        database=config.mysql_db,
        port=config.mysql_port
    )
    return mydb


def entry_check(Check, Row, Table):
    mydb = createConnection()
    cur = mydb.cursor(buffered=True)
    query = (f"SELECT {Row} FROM `{config.mysql_db}`.`{Table}`")
    cur.execute(query)

    for Row in cur:
        if Check in Row:
            cur.close()
            return True


def fetch(Row, Table, Where, Value):
    table = str.maketrans(dict.fromkeys("()"))
    cur = mydb.cursor()
    query = (f"SELECT {Row} FROM `{config.mysql_db}`.`{Table}` WHERE {Where} = {Value}")
    cur.execute(query)
    row = str(cur.fetchone())
    return row.translate(table)


'''Counter '''


def update_counter_leaderboard(user_id):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"UPDATE `{config.mysql_db}`.`counterlead` SET points = points +1 WHERE user_id = {user_id};")
    mydb.commit()


def update_global_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"UPDATE `{config.mysql_db}`.`counter` SET global = global +1 WHERE user_id = {user_id};")
    mydb.commit()


def update_main_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"UPDATE `{config.mysql_db}`.`counter` SET main = main +1 WHERE user_id = {user_id};")
    mydb.commit()


def update_cotd_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"UPDATE `{config.mysql_db}`.`counter` SET cotd = cotd +1 WHERE user_id = {user_id};")
    mydb.commit()


def get_cotd_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute(
        f"SELECT cotd FROM `{config.mysql_db}`.`counter` WHERE user_id = {user_id};")
    row = cur.fetchone()
    if row:
        points = row['points']


def get_global_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute(
        f"SELECT global FROM `{config.mysql_db}`.`counter` WHERE user_id = {user_id};")
    row = cur.fetchone()
    if row:
        points = row['points']

    return points


def get_main_counter(user_id):
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute(
        f"SELECT main FROM `{config.mysql_db}`.`counter` WHERE user_id = {user_id};")
    row = cur.fetchone()
    if row:
        points = row['points']

    return points


def fetch_counter_leaderboard():
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(
        f"SELECT user_id FROM `{config.mysql_db}`.`counterlead` GROUP BY user_id, points ORDER BY points DESC LIMIT 10")
    row = cur.fetchall()
    if row:
        df = pandas.DataFrame(np.array(row), columns=["ID"])
        return df.ID.values.tolist()


def get_winners():
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute(
        f"SELECT user_id FROM `{config.mysql_db}`.`counter` GROUP BY user_id, main ORDER BY main DESC LIMIT 1")
    row = cur.fetchall()
    if row:
        main_winner = row["user_id"]
    cur.execute(
        f"SELECT user_id FROM `{config.mysql_db}`.`counter` GROUP BY user_id, cotd ORDER BY cotd DESC LIMIT 1")
    row = cur.fetchall()
    if row:
        cotd_winner = row["user_id"]
    cur.execute(
        f"SELECT user_id FROM `{config.mysql_db}`.`counter` GROUP BY user_id, global ORDER BY global DESC LIMIT 1")
    row = cur.fetchall()
    if row:
        global_winner = row["user_id"]
    return main_winner, global_winner, cotd_winner


def fetch_points(user_id):
    points = 0
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute(
        f"SELECT points FROM `{config.mysql_db}`.`counterlead` WHERE user_id = {user_id};")
    row = cur.fetchone()
    if row:
        points = row['points']
    return points


def reset_data():
    mydb = createConnection()
    cur = mydb.cursor(dictionary=True)
    cur.execute("TRUNCATE TABLE counter")

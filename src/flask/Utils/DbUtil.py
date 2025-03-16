import logging

import pymysql
from . import Constants

from src.flask.Utils.Env import config


# print(config.db_port)

def prepare():
    conn = pymysql.connect(
        # host='192.168.2.124',
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        charset='utf8',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


# cursor.execute(sql)
# rst = cursor.fetchall()

def execute(exe):
    conn = prepare()
    try:
        rst = exe(conn)
    except Exception as e:
        logging.exception("DbUtil-error:")
        return Constants.rsp_se, 501

    culminate(conn)
    return rst


def culminate(conn):
    conn.cursor().close()
    conn.close()

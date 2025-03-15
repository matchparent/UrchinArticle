import pymysql
from . import Constants


def prepare():
    conn = pymysql.connect(
        # host='192.168.2.124',
        host='127.0.0.1',
        port=3306,
        user='sqljohn',
        password='123',
        database='urchin_article',
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
        print("DbUtil-error:", e)
        return Constants.rsp_se, 501

    culminate(conn)
    return rst


def culminate(conn):
    conn.cursor().close()
    conn.close()

import json
import os

import pymysql

from config import DIR_PATH
from bs4 import BeautifulSoup
import logging.handlers

# 读取数据工具
def read_json(filename, key):
    # 拼接读取文件的完整路径 os.sep动态获取/ \
    file_path = DIR_PATH + os.sep + "data" + os.sep + filename
    arr = []
    with open(file_path, "r", encoding="utf-8") as f:
        for data in json.load(f).get(key):
            arr.append(tuple(data.values())[1:])
    return arr
"""
参数化数据格式：
    [(),()] | [[],[]]
"""

# 日志工具
class GetLog:
    @classmethod
    def get_log(cls):
        cls.log = None
        if cls.log is None:
            # 1、获取日志文件
            cls.log = logging.getLogger()
            # 设置日志级别 info
            cls.log.setLevel(logging.INFO)
            filepath = DIR_PATH + os.sep + "log" + os.sep + "p2p.log"
            # 2、获取处理器 TimedRotatingFileHandler：日志保存到文件且根据时间去分割
            tf = logging.handlers.TimedRotatingFileHandler(
                filename=filepath, when="midnight", interval=1, backupCount=3, encoding="utf-8"
            )
            # 3、获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)
            # 4、将格式器添加到处理器中
            tf.setFormatter(fm)
            # 5、将处理器添加到日志器中
            cls.log.addHandler(tf)
        # 返回日志器
        return cls.log

# 提取html工具
def parser_html(result):
    # 1、提取html
    html = result.json().get("description").get("form")
    # 2、获取bs对象
    bs = BeautifulSoup(html, "html.parser")
    # 3、提取url
    url = bs.form.get("action")
    data = {}
    # 4、查找所有的input标签
    for input in bs.find_all("input"):
        data[input.get("name")] = input.get("value")
    return url, data

# 连接库工具
def conn_mysql(sql):
    conn = None
    cursor = None
    try:
        # 1、获取连接对象
        conn = pymysql.connect(host="121.43.169.97", user="student", password="P2P_student_2023", db="czbk_member", charset="utf8", autocommit=True)
        # 2、获取游标对象
        cursor = conn.cursor()
        # 3、执行sql语句
        cursor.execute(sql)
        # 判断sql语句是否为查询
        if sql.split(" ")[0].lower() == "select":
            # 返回所有结果
            return cursor.fetchall()
        # 否则
        else:
            # 返回受影响的行数
            return "受影响的行数: {}".format(cursor.rowcount)

    except Exception as e:
        GetLog.get_log().error(e)
        raise
    finally:
        # 4、关闭游标
        cursor.close()
        # 5、关闭连接
        conn.close()

# 清除数据
def clear_data():
    sql1 = """
        delete i.* from mb_member_info i inner join mb_member m on i.member_id=m.id where m.phone in ("15252292771","15252292772","15252292773","15252292774");
    """
    sql2 = """
        delete l.* from mb_member_login_log l inner join mb_member m on l.member_id=m.id where m.phone in ("15252292771","15252292772","15252292773","15252292774");
    """
    sql3 = """
        delete from mb_member_register_log where phone in ("15252292771","15252292772","15252292773","15252292774");
    """
    sql4 = """
        delete from mb_member where phone in ("15252292771","15252292772","15252292773","15252292774");
    """
    conn_mysql(sql1)
    conn_mysql(sql2)
    conn_mysql(sql3)
    conn_mysql(sql4)

if __name__ == '__main__':
    # read_json('register_login.json', "img_code")
    # GetLog.get_log().info("信息级别测试")
    sql = "select * from mb_member"
    print(conn_mysql(sql))
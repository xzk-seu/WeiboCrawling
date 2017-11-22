import pymysql.cursors
from user.DBServer import mysql_server


class MyDataBase:
    def __init__(self):
        self.__connect = None
        self.__sql_insert = """INSERT INTO `post` 
        (`nick_name`, `content`, `time`, `num_like`, `num_forward`, `num_comment`) 
        VALUES (%s, %s, %s, %s, %s, %s)"""

    def start(self):
        self.__connect = pymysql.Connect(
            host=mysql_server['host'],
            port=mysql_server['port'],
            user=mysql_server['user'],
            passwd=mysql_server['passwd'],
            db=mysql_server['db'],
            use_unicode=True,
            charset="utf8"
        )

    def db_insert(self, params):
        with self.__connect.cursor() as cursor:
            if isinstance(params, tuple):
                cursor.execute(self.__sql_insert, params)
            elif isinstance(params, list):
                cursor.executemany(self.__sql_insert, params)

    def close(self):
        self.__connect.commit()
        self.__connect.close()


if __name__ == '__main__':
    TS = MyDataBase()
    TS.start()
    TS.db_insert(('Jack', 'Wow', '2017-11-17 11:20', 20, 30, 30))
    TS.close()

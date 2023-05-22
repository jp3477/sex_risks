import pymysql
import pymysql.cursors

import os
from sshtunnel import SSHTunnelForwarder
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SSH_SERV = config['DATABASE']['ssh_server']
SSH_USER = config['DATABASE']['ssh_user']
SSH_PASS = config['DATABASE']['ssh_pass']

MYSQL_HOST = config['DATABASE']['mysql_host']
MYSQL_USER = config['DATABASE']['mysql_user']
MYSQL_DB = config['DATABASE']['mysql_db']
MYSQL_PASS = config['DATABASE']['mysql_pass']

USE_SSH_TUNNEL = True

SERVER = SSHTunnelForwarder((SSH_SERV, 22),
                            ssh_password=SSH_PASS,
                            ssh_username=SSH_USER,
                            remote_bind_address=('127.0.0.1', 3306))

SERVER.start()


class Database:

    def __init__(self, config):

        # Enter your database information here
        if config == 'Mimir from Munnin':
            self.host = MYSQL_HOST
            self.username = MYSQL_USER
            self.password = MYSQL_PASS
            #self.port = 3307
            self.port = SERVER.local_bind_port
            self.dbname = MYSQL_DB
            self.conn = None

    def open_connection(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host,
                                            port=self.port,
                                            user=self.username,
                                            passwd=self.password,
                                            db=self.dbname,
                                            connect_timeout=5)
        except pymysql.MySQLError as e:
            print(e)
            return False

        # print('Database connected')
        return True

    def run_query(self, query):
        if not self.conn: self.open_connection()
        try:
            with self.conn.cursor() as cur:
                records = []
                cur.execute(query)
                result = cur.fetchall()
                for row in result:
                    records.append(row)
                cur.close()
                return records
        except pymysql.MySQLError as e:
            print(e)

    def run(self, query):
        return self.run_query(query)

    def get_list(self, query):
        l = self.run(query)
        return [x[0] for x in l]

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print('Database connection closed.')
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import DictCursor


class Database(object):
    def __init__(self, db_host, db_port, db_user, db_pass, db_name):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def query(self, sql, *args):
        conn = psycopg2.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            cursor_factory=DictCursor
        )
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        values = cursor.fetchall()
        cursor.close()
        conn.close()
        return values

    def insert(self, sql, *args):
        conn = psycopg2.connect(
            database=self.db_name,
            user=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            cursor_factory=DictCursor
        )
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        conn.commit()
        values = cursor.fetchall()
        cursor.close()
        conn.close()
        return values

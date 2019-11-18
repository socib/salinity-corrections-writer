# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 06:16:43 2018

@author: cmunoz
"""

import sys
import re
import logging

import psycopg2

def connect_db():
    reload(sys)  
    sys.setdefaultencoding('utf8')
    conn = psycopg2.connect(dbname='dbname',host='host',port='port', user='user', password='password') #define connection
    logging.info('Connecting to database\n	->%s' % (conn))
    cursor = conn.cursor()  # conn.cursor will return a cursor object, you can use this cursor to perform queries
    logging.info('Connected!\n')
    return cursor, conn;    

def query_db(cursor, conn, query):    
    cursor.execute(query)
    query_output = cursor.fetchall()
    conn.close()
    return query_output;

def write_db(cursor, conn, query, arguments):
    cursor.execute(query,arguments)
    conn.commit()
    cursor.close()
    conn.close()
    return

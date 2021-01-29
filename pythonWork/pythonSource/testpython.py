"""
Requirements (working versions in brackets)

Python packages:
- pymssql (2.1.5)

MacOS brew packages:
- freetds (1.2.18)

"""

import pymssql
import socket
import random
import logging

log = logging.getLogger(__name__)

server = 'fyac-im-test.database.windows.net'
serverip = socket.gethostbyname(server)  # '104.40.168.105'
database = 'modelmodel'
username = 'fyayc-admin'
password = 'Pz@QxML8iL*AKVG*a7xBxb'

# enable_freetds_trace()
log.info('Connecting to {} ({})'.format(server, serverip))
conn = pymssql.connect(server=serverip, database=database, user=username + '@' + server, password=password)

log.info('Connection established')
with conn.cursor() as cursor:
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    while row:
        print('Server version: {}'.format(row))
        row = cursor.fetchone()
    cursor.close()


cursor = conn.cursor()
cursor.execute('SET IMPLICIT_TRANSACTIONS ON')
try:
    cursor.execute('create table modelmodel.dbo.temp (col0 varchar(128), col1 varchar(128))')
except Exception:
    log.info("Cannot create table")
finally:
    cursor.close()


cursor = conn.cursor()
try:
    cursor.execute("insert into temp values ('12','{}')".format(random.random()))
    cursor.execute('commit')
    cursor.execute('SELECT * FROM temp')
except Exception as err:
    log.exception('Cannot insert into temp database')

for row in cursor:
    print('row = {}'.format(row))
    """"""

    """cnxn = psycopg2.connect(
        dsn=,connection_factory=,cursor_factory=)
    "Driver={SQL Server Native Client 11.0};"
                          "Server=fyac-im-test.database.windows.net;"
                          "Database=modelmodel;"
                           "UID=fyayc-admin;"
                          "PWD=Pz@QxML8iL*AKVG*a7xBxb;"
                          "Trusted_Connection=yes;")"""
cursor.close()


def enable_freetds_trace():
    """Enable freetds driver level tracing"""
    import os
    os.environ['TDSDUMP'] = 'stdout'


"""
# Reference: https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?tabs=macos
# 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
import pyodbc
connection_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={};PORT=1433;DATABASE={};UID={};PWD={}' \
    .format(server, database, username, password)

print('Connecting to ' + connection_string)
try:
    conn = pyodbc.connect(connection_string)
except Exception as e:
    print('failed to connect')
"""

#import pymssql
import psycopg2
#conn = pymssql.connect(server="Server=fyac-im-test.database.windows.net",user="fyayc-admin")
cnxn = psycopg2.connect(host='34.65.164.219',database='postgres',user='postgres',password='8c-W.4_HoXU!aN43xED!Gr')

cursor = cnxn.cursor()
cursor.execute ("SET search_path = modelmodel")
try:
    cursor.execute("insert into temp values ('12','123123123')")
    cursor.execute('commit')
    cursor.execute('SELECT * FROM temp')
except Exception as err:
    print (err,type(err))

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


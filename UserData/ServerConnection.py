import mysql.connector
from mysql.connector import connection
from UserData.constants import DATA


db = mysql.connector.connect(
    host=DATA['HOST'],
    user=DATA['USER'],
    database=DATA['DATABASE'],
    passwd=DATA['PASSWORD']
)

cursor = db.cursor()
# cursor.execute("drop table meeting_id")
# db.commit()
# cursor.execute(
#     "create table meeting_id(id varchar(256) PRIMARY KEY NOT NULL,ip varchar(256))")
# db.commit()

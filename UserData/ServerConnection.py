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

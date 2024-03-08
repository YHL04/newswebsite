
import MySQLdb
import os

from auth import *

con = MySQLdb.connect(
    user=USERNAME,
    passwd=SQLPASSWORD,
    host=LOCALHOST,
    port=3306,
    db=DBNAME,
)
cur = con.cursor()
cur.execute("SELECT * FROM app_news")
data = cur.fetchall()
con.close()

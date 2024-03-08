
import MySQLdb
import os

SSHHOST = (os.environ['SSHHOST'])
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
SQLADDRESS = (os.environ['SQLHOST'], 3306)
LOCALHOST = os.environ['LOCALHOST']
SQLPASSWORD = os.environ['SQLPASSWORD']
DBNAME = os.environ['DBNAME']

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

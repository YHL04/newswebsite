

import MySQLdb
import sshtunnel
import ast
import os

try:
    # use auth.py for authentication if running on original machine
    from auth import *
except ImportError:
    # use environment variables for authentication if using github actions
    SSHHOST = (os.environ['SSHHOST'])
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    SQLADDRESS = (os.environ['SQLHOST'], 3306)
    LOCALHOST = os.environ['LOCALHOST']
    SQLPASSWORD = os.environ['SQLPASSWORD']
    DBNAME = os.environ['DBNAME']


sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


def str_rep_to_list(str):
    """changes string '['A', 'B', 'C']' to list ['A', 'B', 'C']"""
    return ast.literal_eval(str)


def reinit_db():
    with sshtunnel.SSHTunnelForwarder(
        SSHHOST,
        ssh_username=USERNAME,
        ssh_password=PASSWORD,
        remote_bind_address=SQLADDRESS
    ) as tunnel:
        con = MySQLdb.connect(
            user=USERNAME,
            passwd=SQLPASSWORD,
            host=LOCALHOST,
            port=tunnel.local_bind_port,
            db=DBNAME,
        )
        cur = con.cursor()
        # cur.execute("DROP TABLE app_news;")
        # cur.execute(
        #     "CREATE TABLE app_news"
        #     "("
        #     "id varchar(255) NOT NULL,"
        #     "title TEXT NOT NULL,"
        #     "date TEXT NOT NULL,"
        #     "authors TEXT NOT NULL,"
        #     "categories TEXT NOT NULL,"
        #     "link TEXT NOT NULL,"
        #     "text TEXT NOT NULL,"
        #     "citation_rank TEXT NOT NULL,"
        #     "final_rank TEXT NOT NULL,"
        #     "UNIQUE (id)"
        #     ")")
        # cur.execute("DROP TABLE app_user;")
        cur.execute(
            "CREATE TABLE app_user"
            "("
            "userid varchar(255) NOT NULL,"
            "UNIQUE (userid)"
            ")"
        )
        # cur.execute("DROP TABLE app_news_likes;")
        cur.execute(
            "CREATE TABLE app_news_likes"
            "("
            "id varchar(255) NOT NULL,"
            "userid varchar(255) NOT NULL,"
            "FOREIGN KEY (id) REFERENCES app_news(id),"
            "FOREIGN KEY (userid) REFERENCES app_user(userid),"
            "UNIQUE (id, userid)"
            ")"
        )
        con.commit()
        con.close()


def get_from_db():
    with sshtunnel.SSHTunnelForwarder(
        SSHHOST,
        ssh_username=USERNAME,
        ssh_password=PASSWORD,
        remote_bind_address=SQLADDRESS
    ) as tunnel:
        con = MySQLdb.connect(
            user=USERNAME,
            passwd=SQLPASSWORD,
            host=LOCALHOST,
            port=tunnel.local_bind_port,
            db=DBNAME,
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM app_news")
        data = cur.fetchall()

        data = [
            {
             'id'           : d[0],
             'title'        : d[1],
             'date'         : d[2][:10],  # only get year-month-day and exclude time
             'authors'      : str_rep_to_list(d[3]),
             'categories'   : str_rep_to_list(d[4]),
             'link'         : d[5],
             'text'         : d[6],
             'citation_rank': d[7],
             'final_rank'   : d[8],
            }
            for d in data
        ]
        con.close()

    return data


def store_to_db(data):
    with sshtunnel.SSHTunnelForwarder(
        SSHHOST,
        ssh_username=USERNAME,
        ssh_password=PASSWORD,
        remote_bind_address=SQLADDRESS
    ) as tunnel:
        con = MySQLdb.connect(
            user=USERNAME,
            passwd=SQLPASSWORD,
            host=LOCALHOST,
            port=tunnel.local_bind_port,
            db=DBNAME,
        )
        data = [(str(d['id']), str(d["title"]), str(d["date"]), str(d["authors"]), str(d["categories"]),
                 str(d["link"]), str(d["text"]), str(d["citation_rank"]), str(d["final_rank"]))
                for d in data]

        cur = con.cursor()
        cur.executemany(
            "INSERT IGNORE INTO app_news VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            data)
        con.commit()
        con.close()


def delete_from_db(data):
    with sshtunnel.SSHTunnelForwarder(
        SSHHOST,
        ssh_username=USERNAME,
        ssh_password=PASSWORD,
        remote_bind_address=SQLADDRESS
    ) as tunnel:
        con = MySQLdb.connect(
            user=USERNAME,
            passwd=SQLPASSWORD,
            host=LOCALHOST,
            port=tunnel.local_bind_port,
            db=DBNAME,
        )
        data = [(d["id"],) for d in data]

        cur = con.cursor()
        cur.executemany(
            "DELETE from app_news where id=%s",
            data
        )
        con.commit()
        con.close()


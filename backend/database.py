

import sqlite3
import ast


def str_rep_to_list(str):
    """changes string '['A', 'B', 'C']' to list ['A', 'B', 'C']"""
    return ast.literal_eval(str)


def reinit_db(file="db.sqlite"):
    # set the news database as news.db
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute("DROP TABLE app_news_likes;")
    cur.execute("DROP TABLE app_news;")
    cur.execute("DROP TABLE app_user;")

    cur.execute(
        "CREATE TABLE app_news"
        "("
        "news_id varchar(255) NOT NULL,"
        "title varchar(255) NOT NULL,"
        "date date NOT NULL,"
        "authors text NOT NULL,"
        "categories text NOT NULL,"
        "link varchar(255) NOT NULL,"
        "text text NOT NULL,"
        "affiliations text NOT NULL,"
        "citation_rank float NOT NULL,"
        "final_rank float NOT NULL,"
        "likes int NOT NULL,"
        "UNIQUE (news_id)"
        ")")
    cur.execute(
        "CREATE TABLE app_user"
        "("
        "user_id varchar(255) NOT NULL,"
        "UNIQUE (user_id)"
        ")"
    )
    cur.execute(
        "CREATE TABLE app_news_likes"
        "(news_id varchar(255) NOT NULL,"
        " user_id varchar(255) NOT NULL,"
        " FOREIGN KEY (news_id) REFERENCES app_news(news_id),"
        " FOREIGN KEY (user_id) REFERENCES app_user(user_id),"
        " unique (news_id, user_id)"
        ")"
    )
    cur.execute(
        "CREATE TABLE app_user_likes"
        "(news_id varchar(255) NOT NULL,"
        " user_id varchar(255) NOT NULL,"
        " FOREIGN KEY (news_id) REFERENCES app_news(news_id),"
        " FOREIGN KEY (user_id) REFERENCES app_user(user_id),"
        " unique (news_id, user_id)"
        ")"
    )
    cur.execute(
        "CREATE TABLE affiliations_table"
        "("
        "affiliations varchar(255) NOT NULL,"
        "weight float NOT NULL,"
        "count float NOT NULL,"
        "unique (affiliations)"
        ")"
    )
    con.commit()
    con.close()


def store_to_db(data, file="db.sqlite"):
    data = [(str(d['id']), str(d["title"]), str(d["date"]), str(d["authors"]), str(d["categories"]),
             str(d["link"]), str(d["text"]), str(d["affiliations"]), str(d["citation_rank"]), str(d["final_rank"]))
            for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO app_news VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            "ON CONFLICT DO NOTHING",
            data)
        con.commit()


def get_from_db(file="db.sqlite"):
    """
    retrieve everything from database in the form of
    List[dict] where dict has keys 'title', 'link', 'text'
    and all values are strings
    """

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT * FROM app_news"  # ORDER BY date DESC"
        )
        data = res.fetchall()

    data = [
        {
         'id'           : d[0],
         'title'        : d[1],
         'date'         : d[2],
         'authors'      : str_rep_to_list(d[3]),
         'categories'   : str_rep_to_list(d[4]),
         'link'         : d[5],
         'text'         : d[6],
         'affiliations' : d[7],
         'citation_rank': d[8],
         'final_rank'   : d[9],
        }
        for d in data
    ]

    return data


def delete_from_db(data, file="db.sqlite"):
    data = [(d["link"],) for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "DELETE from app_news where link=?",
            data)
        con.commit()


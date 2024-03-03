

import sqlite3
import ast


def str_rep_to_list(str):
    """changes string '['A', 'B', 'C']' to list ['A', 'B', 'C']"""
    return ast.literal_eval(str)


def reinit_db(file="db.sqlite"):
    # set the news database as news.db
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE app_news"
        "(id TEXT NOT NULL,"
        " title TEXT NOT NULL,"
        " date TEXT NOT NULL,"
        " authors TEXT NOT NULL,"
        " categories TEXT NOT NULL,"
        " link TEXT NOT NULL,"
        " text TEXT NOT NULL,"
        " citation_rank TEXT NOT NULL,"
        " final_rank TEXT NOT NULL,"
        " likes TEXT NOT NULL,"
        " unique (id)"
        ")")
    con.commit()

    con.close()


def store_to_db(data, file="db.sqlite"):
    data = [(str(d['id']), str(d["title"]), str(d["date"]), str(d["authors"]), str(d["categories"]),
             str(d["link"]), str(d["text"]), str(d["citation_rank"]), str(d["final_rank"]), str(d["likes"]))
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
         'date'         : d[2][:10],  # only get year-month-day and exclude time
         'authors'      : str_rep_to_list(d[3]),
         'categories'   : str_rep_to_list(d[4]),
         'link'         : d[5],
         'text'         : d[6],
         'citation_rank': d[7],
         'final_rank'   : d[8],
         'likes'        : d[9],
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


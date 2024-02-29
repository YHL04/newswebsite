

import sqlite3
import os
import ast


def str_rep_to_list(str):
    """changes string '['A', 'B', 'C']' to list ['A', 'B', 'C']"""
    return ast.literal_eval(str)


def store_to_db(data, file):
    data = [(str(d['id']), str(d["title"]), str(d["date"]), str(d["authors"]), str(d["categories"]),
             str(d["link"]), str(d["text"]), str(d["citation_rank"]), str(d["rank"]), str(d["likes"]))
            for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO app_news VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            "ON CONFLICT DO NOTHING",
            data)
        con.commit()


def get_from_db(file):
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
         'rank'         : d[8],
         'likes'        : d[9],
        }
        for d in data
    ]

    return data


def delete_from_db(data, file):
    data = [(d["link"],) for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "DELETE from app_news where link=?",
            data)
        con.commit()


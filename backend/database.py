

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
    cur.execute("DROP TABLE app_user_likes;")
    cur.execute("DROP TABLE affiliations_table;")
    cur.execute("DROP TABLE app_news;")
    cur.execute("DROP TABLE app_user;")
    cur.execute("DROP TABLE app_stats;")

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
        "like_count int NOT NULL,"
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
    cur.execute(
        "CREATE TABLE app_stats"
        "("
        "stats_id date NOT NULL,"
        "like_count int NOT NULL,"
        "transformers_count int NOT NULL,"
        "diffusion_count int NOT NULL,"
        "rl_count int NOT NULL,"
        "relevance float NOT NULL,"
        "unique (stats_id)"
        ")"
    )
    con.commit()
    con.close()


def store_to_db(data, file="db.sqlite"):
    data = [(str(d['id']), str(d["title"]), str(d["date"]), str(d["authors"]), str(d["categories"]),
             str(d["link"]), str(d["text"]), str(d["affiliations"]), str(d["citation_rank"]), str(d["final_rank"]),
             str(d["like_count"]))
            for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO app_news VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
         'like_count'   : d[10],
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


def modify_in_db(data, file="db.sqlite"):
    """only modifies affiliations, citation_rank, final_rank"""
    data = [(d["affiliations"], d["citation_rank"], d["final_rank"], d["id"],) for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "UPDATE from app_news SET affiliations=%s, citation_rank=%s, final_rank=%s WHERE news_id=%s",
            data
        )
        con.commit()


def get_from_stats(file="db.sqlite"):
    """get stats from app_stats table"""

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT * FROM app_stats"
        )
        data = res.fetchall()

    data = [
        {
         'id'                : d[0],
         'like_count'        : d[1],
         'transformers_count': d[2],
         'diffusion_count'   : d[3],
         'rl_count'          : d[4],
         'relevance'         : d[5],
        }
        for d in data
    ]

    return data


def store_to_stats(data, file="db.sqlite"):
    data = [(str(d['id']), str(d['like_count']), str(d["transformers_count"]), str(d["diffusion_count"]),
             str(d["rl_count"]), str(d["relevance"]))
            for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO app_stats VALUES(?, ?, ?, ?, ?, ?)"
            "ON CONFLICT DO NOTHING",
            data)
        con.commit()


def modify_in_stats(data, file="db.sqlite"):
    """only modifies affiliations, citation_rank, final_rank"""
    data = [(d["like_count"], d["transformers_count"], d["diffusion_count"], d["rl_count"], d["relevance"], d["id"],) for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "UPDATE from app_stats SET like_count=%s, transformers_count=%s, diffusion_count=%s, rl_count=%s, relevance=%s WHERE news_id=%s",
            data
        )
        con.commit()


def delete_from_stats(data, file="db.sqlite"):
    data = [(d["id"],) for d in data]

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        cur.executemany(
            "DELETE from app_stats where stats_id=?",
            data)
        con.commit()

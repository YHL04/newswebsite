

from backend import get_from_db


datas = get_from_db()


for data in datas:
    if data['date'].split()[0] == '2024-03-02':
        print(data['title'])
        print(data['date'])

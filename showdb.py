

from backend import get_from_db


datas = get_from_db()


for data in datas:
    if data['date'] == '2024-03-01':
        print(data['title'])
        print(data['date'])

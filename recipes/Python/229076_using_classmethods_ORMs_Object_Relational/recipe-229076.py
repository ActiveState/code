import psycopg
from config import DSN

conn = psycopg.connect(DSN)
cursor = conn.cursor()


class Animal:
    def __init__(self, id, name, breed):
        self.id = id
        self.name = name
        self.breed = breed

class Animals:
    def loadList(cls):
        cursor.execute('select * from animal')
        rows = cursor.fetchall()
        return [Animal(row[0], row[1], row[2]) for row in rows]

    classmethod(loadList)

animals = Animals()
print animals.loadList()

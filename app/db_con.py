import psycopg2
import os

url = "dbname='ireporter' host='localhost'\
        port='5432' user='postgres' password='calculus3'"
db_url = os.getenv('DATABASE_URL')
con = psycopg2.connect(db_url)
cur = con.cursor()
# result = con.execute()
con.close()

def connection(connect_url):
        conn = psycopg2.connect(connect_url)
        return conn

def init_db(url):
        conn = connection(url)
        return conn

def init_test_db(url):
        conn = connection(test_url)
        return conn


def create_tables(url):
        conn = connection(url)
        curr = conn.cursor(url)
        queries = tables()

        for query in queries:
                curr.execute(query)

def destroy_tables(url):
        db1 = """"""
        db2 = """"""
        db3 = """"""
        pass

def tables():
        users=
        incidents=

queries = [users,incidences]
return queries



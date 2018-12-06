import psycopg2
import os

url = "dbname='ireporter' host='localhost'\
        port='5432' user='postgres' password='calculus3'"
db_url = os.getenv('DATABASE_URL')
con = psycopg2.connect(db_url)
cur = con.cursor()
# result = con.execute()
con.close()

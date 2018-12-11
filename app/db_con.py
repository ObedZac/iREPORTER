""" This module holds the database migrations """
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = 'postgresql://localhost/ireporter?user=postgres&\
                    password=calculus3'
TEST_DATABASE_URL = 'postgresql://localhost/ireporter_test?user=postgres&\
                        password=calculus3'
CONNECTION_CREDS = {
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD')
}
TEST_CONNECTION_CREDS = {
    "host": os.getenv('TEST_DB_HOST'),
    "database": os.getenv('TEST_DB_NAME'),
    "user": os.getenv('TEST_DB_USER'),
    "password": os.getenv('TEST_DB_PASSWORD')
}


class Database ():
    """
        consists of methods to connect and query from db
    """

    def __init__(self, db):
        self.db_url = DATABASE_URL
        self.db_test_url = TEST_DATABASE_URL
        self.db_con_creds = CONNECTION_CREDS
        self.db_test_con_creds = TEST_CONNECTION_CREDS
        self.conn = self.choose_db(db)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def connection(self, *args, **url):
        """
            connect to postgres database
        """
        conn = psycopg2.connect(url)
        return conn

    def init_db(self):
        """
            connect to iReporter database
        """
        try:
            print("connecting to database...\n")
            try:
                conn = connection(self.db_url)
                print('connected successfully to db\n')
                return conn
            except:
                conn = psycopg2.connect(
                    'postgresql://localhost/ireporter?user=postgres\
                        &password=calculus3')
                print('connected successfully to db\n')
                return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('error connecting to database\n')

    def init_test_db(self):
        """
            connect to test db
        """
        try:
            print("connecting to test db...\n")
            try:
                conn = connection(self.db_test_url)
                print('connected to test db\n')
                return conn
            except:
                conn = psycopg2.connect(
                    'postgresql://localhost/ireporter_test?user=postgres\
                    &password=calculus3')
                print('connected successfully to test database\n')
                return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('error connecting to test database\n')

    def choose_db(self, db):
        """ choose database to connect to """
        if db == "main":
            conn = self.init_db()
            return conn
        elif db == "test":
            conn = self.init_test_db()
            return conn

    def create_app_tables(self):
        """
            create app tables in the database
        """
        tables = (
            """
                CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY NOT NULL,
                    firstname CHAR(20),
                    lastname CHAR(20),
                    othernames CHAR(20),
                    username VARCHAR(20) NOT NULL unique,
                    email VARCHAR(50) NOT NULL unique,
                    phoneNumber INT,
                    password VARCHAR(100) NOT NULL,
                    registered DATE NOT NULL ,
                    isAdmin BOOLEAN NOT NULL DEFAULT FALSE
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS incidents(
                    incident_id SERIAL PRIMARY KEY NOT NULL,
                    createdOn VARCHAR(50) NOT NULL ,
                    modifiedOn VARCHAR(50) NOT NULL,
                    record_type CHAR(20) NOT NULL,
                    location VARCHAR(50),
                    status CHAR(20) NOT NULL DEFAULT 'pending',
                    images VARCHAR(80),
                    video VARCHAR(80),
                    title VARCHAR(100) NOT NULL,
                    comment VARCHAR(250) NOT NULL unique,
                    createdBy INT REFERENCES users (user_id)

                )
            """
        )

        try:
            for table in tables:
                self.query(table)
            self.save()
            self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('could not create tables\n')
        finally:
            if self.conn is not None:
                self.conn.close()

    def drop(self, table):
        """ drop existing tables """
        try:
            self.query("DROP TABLE IF EXISTS" + table)
            self.save()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('could not drop tables\n')
        finally:
            if self.conn is not None:
                self.close()

    def save(self):
        """
        commit changes to the db
        """
        self.conn.commit()

    def close(self):
        """
            close the cursor and connection
        """
        self.cur.close()
        self.conn.close()

    def fetch_one(self):
        """ return row from query"""
        return self.cur.fetchone()

    def fetch_all(self):
        """ return all rows from query"""
        return self.cur.fetchall()

    def query(self, query):
        """
        Execute query.

        :param query:
        :return: True
        """
        self.cur.execute(query)

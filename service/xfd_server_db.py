#!/usr/bin/python3

import sqlite3 as sql
import sys
from contextlib import closing

class XfdServerDb:
    def __init__(self, path_to_database = ""):
        if not path_to_database: 
            self._path_to_database = "database.db"
        else:
            self._path_to_database = path_to_database

    def _create_tables(self):
        try:
            with closing(sql.connect(self._path_to_database)) as conn:
                c = conn.cursor()
                c.execute('''CREATE TABLE jobs (
                    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    description TEXT
                )''')

                c.execute('''CREATE TABLE config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    active_job INTEGER NOT NULL,
                    FOREIGN KEY(active_job) REFERENCES jobs(job_id)
                ) ''')

                c.execute('''CREATE TABLE states (
                    state_id INTEGER NOT NULL PRIMARY KEY,
                    state TEXT NOT NULL
                ) ''')

                c.execute('''INSERT INTO states(state_id, state) VALUES(-1, "FAILURE")''')
                c.execute('''INSERT INTO states(state_id, state) VALUES( 1, "SUCCESS")''')

                c.execute('''CREATE TABLE results (
                    job_id INTEGER NOT NULL,
                    build_id INTEGER NOT NULL,
                    state_id int NOT NULL,
                    PRIMARY KEY(job_id, build_id)
                    FOREIGN KEY(state_id) REFERENCES states(state_id)
                    FOREIGN KEY(job_id) REFERENCES jobs(job_id)
                ) ''')

                conn.commit()
        except:
            print(sys.exc_info())
            raise


    def load_address(self):
        # todo load it from DB
        return 1, "http://localhost:8080/job/hoge/api/json"

    def save_result(self, job_id, build_id, state):
        try:
            with closing(sql.connect(self._path_to_database)) as conn:
                c = conn.cursor()
                state_id = state
                c.execute('''INSERT INTO results VALUES(?,?,?)''',
                     (job_id, build_id, 1 if state == "SUCCESS" else -1))
                conn.commit()

        except sql.Error:
            print(sys.exc_info())

if __name__ == '__main__':
    db = XfdServerDb()
    db._create_tables()

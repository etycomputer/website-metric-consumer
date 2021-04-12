import psycopg2
import logging
from config import postgres_connection_config_params


class MyPostgresDB:
    log = None
    testing = None
    prefix = ''

    def __init__(self, log: logging, test_mode=None):
        self.log = log
        self.testing = test_mode
        self.prefix = '' if self.testing is True else 'testing_'

    def create_db(self):
        """Create the tables in PostgreSQL if they don't already exist"""
        queries = ("""CREATE TABLE {prefix}target_urls (
url_id SERIAL NOT NULL PRIMARY KEY, 
is_enabled BOOLEAN NOT NULL DEFAULT FALSE,  
sample_frequency_s INTEGER NOT NULL DEFAULT 60,
url_path TEXT NOT NULL, 
regex_pattern TEXT DEFAULT NULL)""".format(prefix=self.prefix),
                   """CREATE INDEX idx_is_enabled ON {prefix}target_urls(is_enabled)""".format(prefix=self.prefix),
                   """CREATE TABLE {prefix}url_performance_metrics (
sample_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, 
url_id INTEGER REFERENCES {prefix}target_urls(url_id) NOT NULL,
response_code INTEGER NOT NULL,
response_time DOUBLE PRECISION NOT NULL,
match_found BOOLEAN NOT NULL,
PRIMARY KEY (sample_timestamp, url_id))""".format(prefix=self.prefix))
        return queries if self.testing is not None else self.execute_queries(queries)

    def seed_db(self):
        """Populating the tables in PostgreSQL"""
        queries = ("""INSERT INTO {prefix}target_urls (is_enabled, sample_frequency_s, url_path, regex_pattern) 
VALUES (DEFAULT, DEFAULT, 'http://localhost', DEFAULT), 
(FALSE, DEFAULT, 'http://localhost/sleep', DEFAULT), 
(TRUE, 10, 'http://localhost/sleep/1', DEFAULT), 
(TRUE, 5, 'http://localhost/sleep/1/25', DEFAULT), 
(FALSE, DEFAULT, 'http://localhost/sleep/1', 'SUCCESSFUL'), 
(FALSE, DEFAULT, 'http://localhost/sleep/1/25', 'SKIPPED')""".format(prefix=self.prefix), )
        return queries if self.testing is not None else self.execute_queries(queries)

    def drop_db(self):
        """Remove the tables in PostgreSQL"""
        queries = ("Drop TABLE {prefix}url_performance_metrics RESTRICT".format(prefix=self.prefix),
                   "Drop TABLE {prefix}target_urls RESTRICT".format(prefix=self.prefix))
        return queries if self.testing is not None else self.execute_queries(queries)

    def insert_sample_measurements(self, measurements=None):
        isSuccessful = True
        if measurements is None:
            measurements = []
        if not measurements:
            pass
        query = """INSERT INTO {prefix}url_performance_metrics 
(url_id, sample_timestamp, response_code, response_time, match_found) 
VALUES (%s,%s,%s,%s,%s)""".format(prefix=self.prefix)
        connection = None
        cursor = None
        try:
            # connect to the PostgreSQL server
            connection = psycopg2.connect(**postgres_connection_config_params)
            cursor = connection.cursor()
            # execute the INSERT statement
            cursor.executemany(query, measurements)
            # commit the changes
            connection.commit()
            # close communication with the PostgreSQL database server
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log.info(error)
            isSuccessful = False
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return isSuccessful

    def execute_queries(self, queries=()) -> bool:
        isSuccessful = True
        connection = None
        cursor = None
        try:
            # connect to the PostgreSQL server
            connection = psycopg2.connect(**postgres_connection_config_params)
            cursor = connection.cursor()
            # drop tables one by one
            for query in queries:
                cursor.execute(query)
                # commit the changes
                connection.commit()
            # close communication with the PostgreSQL database server
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log.info(error)
            isSuccessful = False
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
        return isSuccessful


def create_producer(test_mode=None) -> MyPostgresDB:
    return MyPostgresDB(logging, test_mode)

import mysql.connector
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class MySQLWriter:
    def __init__(self):
        self.config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME")
        }
        self.conn = None
        self._setup_db()

    def _setup_db(self):
        """Creates the database and table if they don't exist."""
        try:
            # Connect without DB first to create it
            tmp_conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            cursor = tmp_conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            tmp_conn.close()

            # Now connect to the specific DB
            self.conn = mysql.connector.connect(**self.config)
            self._create_table()
        except mysql.connector.Error as e:
            logging.error(f" Database Setup Error: {e}")

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS repositories (
            repo_id INT PRIMARY KEY,
            name VARCHAR(255),
            full_name VARCHAR(255),
            owner_login VARCHAR(100),
            stars INT,
            forks INT,
            language VARCHAR(50),
            created_at DATETIME,
            updated_at DATETIME,
            url TEXT,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def load_batch(self, data):
        """Performs an 'Upsert' (Update or Insert) for a batch of records."""
        query = """
        INSERT INTO repositories 
        (repo_id, name, full_name, owner_login, stars, forks, language, created_at, updated_at, url)
        VALUES (%(repo_id)s, %(name)s, %(full_name)s, %(owner_login)s, %(stars)s, %(forks)s, %(language)s, %(created_at)s, %(updated_at)s, %(url)s)
        ON DUPLICATE KEY UPDATE
        stars = VALUES(stars),
        forks = VALUES(forks),
        updated_at = VALUES(updated_at);
        """
        try:
            cursor = self.conn.cursor()
            cursor.executemany(query, data)
            self.conn.commit()
            logging.info(f" Successfully loaded {cursor.rowcount} records to MySQL.")
        except mysql.connector.Error as e:
            logging.error(f" Database Load Error: {e}")
            self.conn.rollback()
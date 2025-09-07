import os
import django
from django.db import connection

try:
    import mysql.connector
except ImportError:
    mysql = None


class DBConnection:
    @staticmethod
    def getConnection():
        # Check if running on Render (DATABASE_URL is set)
        if os.getenv("DATABASE_URL"):
            # use Django’s default connection (Postgres on Render)
            return connection
        else:
            # Local MySQL connection
            if mysql is None:
                raise ImportError("mysql.connector not installed. Use Postgres in Render.")
            return mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                db="IIDPS"
            )


if __name__ == "__main__":
    print(DBConnection.getConnection())

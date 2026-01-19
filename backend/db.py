
import os
import pymysql

def get_conn():
    return pymysql.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT")),
        charset='utf8mb4'
    )


conn = get_conn()
print("Connected successfully!")  # Should print
conn.close()

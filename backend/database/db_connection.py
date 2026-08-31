import sqlite3



# Database connection

def db_connection(db_name=None):

    conn=sqlite3.connect(db_name)

    # cursor object to perform actions
    cursor=conn.cursor()

    # enforcing db to follow foriegn key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    return cursor,conn




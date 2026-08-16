import sqlite3
from config import users,orders,restaurants,dishes,db_name

def db_connection(db_name):

    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON")

    return cursor,conn

cursor , conn =db_connection(db_name)

cursor.executescript("""
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cuisine_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    spice INTEGER NOT NULL CHECK(spice BETWEEN 1 AND 5),
    price INTEGER NOT NULL,
    type_of_food TEXT NOT NULL,
    healthy_rating INTEGER NOT NULL,
    popularity_score REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
""")


cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_data(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    rest_id INTEGER,
    dish_id INTEGER,
    name TEXT NOT NULL,
    spice INTEGER,
    price INTEGER,
    type_of_food TEXT,
    healthy_rating INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (rest_id) REFERENCES restaurants(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);
""")


# cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?)", restaurants)
# cursor.executemany("INSERT INTO dishes VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dishes)
# cursor.executemany("INSERT INTO users VALUES (?, ?)", users)
# cursor.executemany(
#     "INSERT INTO user_data (user_id, rest_id, dish_id, name, spice, price, type_of_food, healthy_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#     orders
# )

conn.commit()
conn.close()
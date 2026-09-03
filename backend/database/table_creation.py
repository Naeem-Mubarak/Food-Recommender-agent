from database.db_connection import db_connection
from config.system_info import DB_PATH


cursor , conn =db_connection(DB_PATH)


cursor.executescript("""
CREATE TABLE IF NOT EXISTS restaurants (
    branch_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cuisine_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dishes (
    dish_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    spice INTEGER NOT NULL CHECK(spice BETWEEN 1 AND 5),
    sweet_level INTEGER NOT NULL DEFAULT 0 CHECK(sweet_level BETWEEN 0 AND 5),
    price INTEGER NOT NULL,
    type_of_food TEXT NOT NULL,
    healthy_rating INTEGER NOT NULL,
    popularity_score REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(branch_id)
);
""")


cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    cust_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_data(
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    rest_id INTEGER,
    dish_id INTEGER,
    name TEXT NOT NULL,
    spice INTEGER,
    sweet INTEGER,
    price INTEGER,
    type_of_food TEXT,
    healthy_rating INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(cust_id),
    FOREIGN KEY (rest_id) REFERENCES restaurants(branch_id),
    FOREIGN KEY (dish_id) REFERENCES dishes(dish_id)
);
""")

print("Table created successfully")

conn.commit()
conn.close()
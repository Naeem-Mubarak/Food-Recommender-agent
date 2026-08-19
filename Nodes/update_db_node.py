from Nodes.state import state_schema
from config.system_info import DB_PATH
from Database.db_connection import db_connection


cursor, conn = db_connection(DB_PATH)


def update_db(state : state_schema):

    item = state['selected_item']

    order = [state['user_id'],item['rest_id'],item['dish_id'],item['dish_name'],item['spice_level'],item['dish_price'],item['type_of_food'],item['healthy_rating']]

    cursor.executemany(
    "INSERT INTO user_data (user_id, rest_id, dish_id, name, spice, price, type_of_food, healthy_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    order)

    conn.commit()
    conn.close()

    return state


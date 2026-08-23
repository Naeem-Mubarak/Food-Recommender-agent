from graph.state import state_schema
from config.system_info import DB_PATH
from database.db_connection import db_connection

# db connection
cursor, conn = db_connection(DB_PATH)


def update_db(state : state_schema):

    """
    adding the final order of the user to his history so for next time agent can recommend him according to his history 
    """
    item = state['selected_item']

    order = [state['user_id'],item['rest_id'],item['dish_id'],item['dish_name'],item['spice_level'],item['dish_price'],item['type_of_food'],item['healthy_rating']]

    cursor.execute(
    "INSERT INTO user_data (user_id, rest_id, dish_id, name, spice, price, type_of_food, healthy_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    order)

    conn.commit()

    return state


from config.system_info import DB_PATH 
from database.db_connection import db_connection

cursor, conn =db_connection(DB_PATH)

def menu_loader():

    cursor.execute("""
          SELECT
          r.branch_id, r.name , r.cuisine_type, d.dish_id, d.name, d.spice, d.price, d.type_of_food, d.healthy_rating, d.popularity_score
          FROM dishes as d
          INNER JOIN restaurants as r
          ON r.branch_id = d.restaurant_id
    """)

    rows = cursor.fetchall()
    cols = ['rest_id', 'restaurant_name', 'cuisine_type', 'dish_id', 'dish_name', 'spice_level', 'dish_price', 'type_of_food', 'healthy_rating', 'popularity_score']

    menu = [dict(zip(cols, row)) for row in rows]

    return menu


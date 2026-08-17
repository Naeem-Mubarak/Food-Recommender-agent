from config.system_info import DB_PATH 
from Database.db_connection import db_connection

cursor, conn =db_connection(DB_PATH)

def menu_loader():

    cursor.execute("""
          SELECT
          r.branch_id, r.name , r.cuisine_type, d.dish_id, d.name, d.spice, d.price, d.type_of_food, d.healthy_rating, d.popularity_score
          FROM dishes as d
          INNER JOIN restaurants as r
          ON r.branch_id = d.restaurant_id
    """)

    menu = cursor.fetchall()

    return menu


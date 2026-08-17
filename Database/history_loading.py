import sqlite3
from config import db_name 
from Database.food_data_db import db_connection
from models.English_translator import english_translator
from models.voice_llm import voice_transcript_generator,path

order_details=english_translator(data)
user_id=order_details['id']
cursor, conn =db_connection(db_name)


def found_customer_data(user_id : int):

    cursor.execute(f"SELECT * FROM users WHERE cust_id==?",(user_id,))
    data=cursor.fetchone()
    if data:
        cursor.execute(f"""
            SELECT 
            r.name,u.name,u.spice,u.price,u.type_of_food,u.healthy_rating
            FROM user_data as u
            INNER JOIN restaurants as r
            ON u.rest_id = r.branch_id
            WHERE u.user_id=={user_id}
            """)
        customer_history=cursor.fetchall()

        return customer_history
    
    cursor.execute(f"INSERT INTO users (id,name) VALUES (?,?)",(user_id,order_details['name']))
    return []


user_id=4
d=found_customer_data(user_id)
print(d)




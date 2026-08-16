import sqlite3
from config import db_name 
from food_data_db import db_connection
from English_translator import english_translator
from voice_llm import voice_transcript_generator,path

data=voice_transcript_generator(path)
order_details=english_translator(data)
user_id=order_details['id']
cursor, conn =db_connection(db_name)


def found_customer_data(user_id : int):

    cursor.execute(f"SELECT * FROM users WHERE id==?",(user_id,))
    data=cursor.fetchone()
    if data:
        cursor.execute(f"SELECT * FROM user_data WHERE user_id=={data[0]}")
        customer_history=cursor.fetchall()

        return customer_history
    
    cursor.execute(f"INSERT INTO users (id,name) VALUES (?,?)",(user_id,order_details['name']))
    return []


user_id=4
d=found_customer_data(user_id)
print(d)




from config.system_info import DB_PATH 
from Database.db_connection import db_connection
from models.English_translator import english_translator
from models.voice_llm import voice_transcript_generator,path

data=voice_transcript_generator(path)
order_details=english_translator(data)
user_id=order_details['id']
cursor, conn =db_connection(DB_PATH)


def found_customer_data(user_id : int):

    cursor.execute("SELECT * FROM users WHERE cust_id=?",(user_id,))
    data=cursor.fetchone()
    if data:
        cursor.execute("""
            SELECT 
            r.name,u.name,u.spice,u.price,u.type_of_food,u.healthy_rating
            FROM user_data AS u
            INNER JOIN restaurants AS r
            ON u.rest_id = r.branch_id
            WHERE u.user_id=?
            """,(user_id,))
        customer_history=cursor.fetchall()

        return customer_history
    
    cursor.execute("INSERT INTO users (cust_id,name) VALUES (?,?)",(user_id,order_details['name']))
    conn.commit()
    return []






from Nodes.state import state_schema
from config.system_info import DB_PATH
from Database.db_connection import db_connection
from langgraph.types import interrupt
import random


cursor, conn = db_connection(DB_PATH)


def id_gen():

    # getting all the ids present in db

    li=cursor.execute("SELECT cust_id FROM users")
    
    id_gen = random.randint(0, 100)

    # generating a unique id which is not present in db

    while (id_gen,) in li:

        id_gen = random.randint(0,100)
            
    conn.close()
      
    return id_gen



def new_user(state : state_schema):

    # assigning new id to the new customer because he is not in the db 
        new_id = id_gen()

        new_user_name = interrupt({
             "type" : "New user",
             "message" : f"Your new_id is {new_id} now tell me your name" 
        })

        cursor.execute('INSERT INTO users VALUES (?,?)', (new_id , new_user_name))
        conn.commit()
        cursor.close()

        # updating state
        state['user_id'] = new_id
        state['name'] = new_user_name

        return state

        

        





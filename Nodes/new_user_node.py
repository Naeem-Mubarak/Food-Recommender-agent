from Nodes.state import state_schema
from config.system_info import DB_PATH
from Database.db_connection import db_connection
import random


cursor, conn = db_connection(DB_PATH)


def id_gen():

    li=cursor.execute("SELECT cust_id FROM users")
    
    id_gen = random.randint(0, 100)

    while (id_gen,) in li:

        id_gen = random.randint(0,100)
            
            
    return id_gen



def new_user(state : state_schema):

    name=cursor.execute("SELECT name FROM WHERE cust_id=?",(state['user_id'],))

    if state['name']!=name:

        # assigning new id to the new customer because he is not in the db 
        new_id=id_gen()

        cursor.executescript('INSERT INTO users VALUES (?,?)',(new_id,state['name']))
        cursor.commit()
        cursor.close()

        # updating state
        state['user_id']=new_id

        return state

        





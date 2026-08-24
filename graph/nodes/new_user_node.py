from graph.agent_schema import state_schema
from config.system_info import DB_PATH
from database.db_connection import db_connection
from langgraph.types import interrupt
from schemas.new_user_schema import chain
import random


cursor, conn = db_connection(DB_PATH)


def id_gen():

    # getting all the ids present in db
    li = [row[0] for row in cursor.execute("SELECT cust_id FROM users").fetchall()]

    # generating a unique id which is not present in db
    while True:
        id_gen = random.randint(0,100)

        if id_gen not in li:
             return id_gen



def new_user(state : state_schema):

        # assigning new id to the new customer because he is not in the db 
        new_id = id_gen()


        while True:

            # interrupting the flow to take user name
            new_user_name = interrupt({
                    "type" : "New_user",
                    "instruction" : f"Your new_id is {new_id} now tell me your name and remember your name and id after that whenever you have to use our application again you can easily login with your credentials" 
            })

            state['text'] = new_user_name
    
    
            response = chain.invoke({
                'text' : state['text']
            })
    
            # converting pydantic model to dict 
            name = response.model_dump()
    
            name = name['name']
    
            if name is None:

                continue

            # Only inserted when the name is provided
            cursor.execute(
                 'INSERT INTO users VALUES (?,?)', 
                 (new_id , name)

            )
            conn.commit()

            # updating state
            state['user_id'] = new_id
            state['name'] = name

            return state

        

        





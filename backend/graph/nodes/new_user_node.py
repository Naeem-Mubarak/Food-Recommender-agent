from graph.agent_schema import state_schema
from config.system_info import DB_PATH
from database.db_connection import db_connection
from langgraph.types import interrupt
from graph.schemas.new_user_schema import chain
import random


def id_gen(cursor):

    """Deterministic, not random - a replay of this node (which
    re-runs from the top on every resume) computes the SAME id both
    times, instead of a fresh random number that would mismatch what
    was already spoken to the user."""
    row = cursor.execute("SELECT COALESCE(MAX(cust_id), 0) + 1 FROM users").fetchone()
    return row[0]



def new_user(state : state_schema):

        cursor, conn = db_connection(DB_PATH)

        try:
            # assigning new id to the new customer because he is not in the db 
            new_id = id_gen(cursor)

            retry_note = None


            while True:


                instruction = (
                     f"Your new id is {new_id}. Now tell me your name, and remember"
                     f"your name and id - next time you can log in with these credentials."
                )

                if retry_note:
                     instruction = (
                        f"I heard '{retry_note}' but couldn't catch a clear name. "
                        f"Please tell me your name again."
                )
                     
                # interrupting the flow to take user name
                new_user_name = interrupt({
                        "type" : "New_user",
                        "instruction" : instruction,
                        "new_id" : new_id
                })

                state['text'] = new_user_name
        
        
                response = chain.invoke({
                    'text' : state['text']
                })
        
                # converting pydantic model to dict 
                name = response.model_dump()
                name = name['name']
                print(f"Transcribed: {state['text']!r} -> extracted name: {name!r}")
        
                if name is None:
                    retry_note = state['text']
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

        finally:
             conn.close()

        

        





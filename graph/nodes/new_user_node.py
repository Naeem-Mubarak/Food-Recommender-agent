from graph.state import state_schema
from config.system_info import DB_PATH
from database.db_connection import db_connection
from langgraph.types import interrupt
from config.system_info import model
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from langchain_core.prompts import ChatPromptTemplate
import random
from models.speech_to_text import voice_transcript_generator


cursor, conn = db_connection(DB_PATH)


def id_gen():

    # getting all the ids present in db
    li = [row[0] for row in cursor.execute("SELECT cust_id FROM users").fetchall()]
    random.seed(42)
    id_gen = random.randint(0, 100)

    # generating a unique id which is not present in db
    while id_gen in li:

        id_gen = random.randint(0,100)
      
    return id_gen



class name_schema(BaseModel):

     name : Annotated[
          Optional[str],
          Field(default=None,description='Name of the user')
     ]



def new_user(state : state_schema):

        # assigning new id to the new customer because he is not in the db 
        new_id = id_gen()


        while True:

             # interrupting the flow to take user name
            new_user_name = interrupt({
                    "type" : "New_user",
                    "instruction" : f"Your new_id is {new_id} now tell me your name and remember your name and id after that whenever you have to use our application again you can easily login with your credentials" 
            })

            state['path'] = new_user_name
            text = voice_transcript_generator(state['path'])
            state['voice'] = text
    
            prompt = ChatPromptTemplate.from_messages([
                ('system',"""You are an intelligent AI assistant so you have to fetch the name of from the given sentence. Instructions:                                                                                         - if nothing feels like name then return None.
                - Try you level best to find the name.
                - Don't pick useless things as name the name must be clear."""),
                ('human',"{text}")
            ])

            # enforcing schema
            structured_llm = model.with_structured_output(name_schema)

            chain = prompt | structured_llm
    
            response = chain.invoke({
                'text' : state['voice']
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

        

        





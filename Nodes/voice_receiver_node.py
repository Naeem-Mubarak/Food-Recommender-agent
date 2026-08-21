from Nodes.state import state_schema
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate
from langgraph.types import interrupt
from pydantic import BaseModel,Field
from typing import Annotated
from models.speech_to_text import voice_transcript_generator

class id_getter(BaseModel):

    u_id : Annotated[int,Field(default=None,ge=0,description="id of the user")]
    name : Annotated[str,Field(default=None,description="Name of the user")]


def reciever_node(state : state_schema):

    user_message = interrupt({
        'type' : 'starting point',
        'reason' : 'collecting users data',
        'instruction' : 'tell your id and name'
    })

    user_input = voice_transcript_generator(user_message)

    prompt = ChatPromptTemplate.from_messages([
    ("system",
            """
    You extract a user's ID and it's namefrom their message.
    Rules:
    1. A valid ID MUST be a number.
    2. Extract the number regardless of what words surround it.
    3. If the user mentions the word "ID" but does not provide a number,
    there is NO valid ID.
    4. Ignore all non-numeric information.
    5. Do not interpret words such as "my id", "ID", "identifier", etc.
    as an ID by themselves.
    6. If a numeric value exists in the message, return that number as u_id.
    7. Most important thing is there no number then return None and if there is no name then return None
    """),
        ("human", "{user_input}")
    ])

    structured_llm = model.with_structured_output(id_getter)
    chain = prompt | structured_llm

    response = chain.invoke({
        'user_input' : str(user_input)
    })
    response = response.model_dump()
    state['user_id'] = response['u_id']
    state['name'] = response['name']

    return state


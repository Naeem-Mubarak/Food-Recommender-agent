from Nodes.state import state_schema
from pydantic import BaseModel
from typing import Literal
from langgraph.types import interrupt
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate


class confirmation_response(BaseModel):

    sign : Literal['confirm','not-confirm']

def order_confirmation(state : state_schema):

    confirmation = interrupt({
        'type' : 'confirmation',
        'instruction' : 'yes if wants otherwise no'
    })

    structured_llm=model.with_structured_output(confirmation_response)
    prompt = ChatPromptTemplate.from_messages([
        ('system',
        """You are a restaurant waiter.
        The user is confirming whether they want to place the selected order.

        Return:
        - "confirm" if the user wants to place the order.
        - "not-confirm" if the user does not want to place the order.
        """),
        ('human','{confirmation}')
    ])

    chain = prompt | structured_llm

    response = chain.invoke({
        'confirmation' : confirmation
    })

    response=response.model_dump()

    state['confirm_order'] = response['sign']

    return state
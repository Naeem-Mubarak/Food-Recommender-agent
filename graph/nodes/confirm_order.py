from graph.state import state_schema
from pydantic import BaseModel,Field
from typing import Literal,Annotated
from langgraph.types import interrupt
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate
from models.speech_to_text import voice_transcript_generator
from langchain_core.output_parsers import StrOutputParser


class confirmation_response(BaseModel):

    sign : Annotated[
        Literal['confirm','not-confirm'],
        Field(default='confirm',description='Either order is final or not')
    ]

def order_confirmation(state : state_schema):

    item = state['selected_item'] 

    order_prompt = ChatPromptTemplate.from_messages([
        ('system',"""You are a senior waiter at a restaurant you job is to just confirm the order by narrating the order the customer
        For example:
        if you got an order like this {'rest_id': 9, 'restaurant_name': 'Roasters', 'cuisine_type': 'Traditional Spicy Food', 'dish_id': 44, 'dish_name': 'Spicy Roast Chicken', 'spice_level': 4, 'dish_price': 550, 'type_of_food': 'non-veg', 'healthy_rating': 6, 'popularity_score': 5}
        Then you have to simply summrize this into two lines 
        Sir do you want to confirm 'Spicy Roaster Chicken from Roasters with the spice level of 4 having price just 550 and it's a non-veg healthy food.
        """),
        ('human',"{item}")
    ])

    parser = StrOutputParser()

    chain = prompt | model | parser
    message = chain.invoke({
        'item' : item
    })

    confirmation = interrupt({
        'type' : 'confirmation',
        'instruction' : f'{message}'
    })

    state['path'] = confirmation
    text = voice_transcript_generator(state['path'])
    state['voice'] = text

    # enforcing schema on the LLM
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
        'confirmation' : state['voice']
    })

    # converting pydantic object to dict
    response=response.model_dump()

    # state updation
    state['confirm_order'] = response['sign']

    return state
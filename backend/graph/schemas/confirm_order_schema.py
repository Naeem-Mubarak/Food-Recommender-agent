from pydantic import BaseModel,Field
from typing import Literal,Annotated
from config.system_info import Gemini_model_provider
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = Gemini_model_provider()


class confirmation_response(BaseModel):

    sign : Annotated[
        Literal['confirm','not-confirm'],
        Field(default='confirm',description='Either order is final or not')
    ]




order_prompt = ChatPromptTemplate.from_messages([
        ('system',"""You are a senior waiter at a restaurant you job is to just confirm the order by narrating the order to the customer
        For example:
        if you got an order like this 'rest_id': 9, 'restaurant_name': 'Roasters', 'cuisine_type': 'Traditional Spicy Food', 'dish_id': 44, 'dish_name': 'Spicy Roast Chicken', 'spice_level': 4, 'dish_price': 550, 'type_of_food': 'non-veg', 'healthy_rating': 6, 'popularity_score': 5
        Then you have to simply summrize this into two lines 
        Sir do you want to confirm 'Spicy Roaster Chicken from Roasters with the spice level of 4 having price just 550 and it's a non-veg healthy food.
        """),
        ('human',"{item}")
    ])

parser = StrOutputParser()

chain1 = order_prompt | model | parser




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

chain2 = prompt | structured_llm

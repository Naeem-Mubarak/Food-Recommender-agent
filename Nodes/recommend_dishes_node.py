from pydantic import BaseModel
from typing import TypedDict,List
from config.system_info import model
from Nodes.state import state_schema
from Database.menu_loader import menu_loader
from langchain_core.prompts import ChatPromptTemplate


class menu_item(TypedDict):

    rest_id : int
    restaurant_name : str
    cuisine_type : str
    dish_id : int
    dish_name : str
    spice_level : int
    dish_price : int
    type_of_food : str
    healthy_rating : int
    popularity_score : int


class menu_schema(BaseModel):

    recommendations : List[menu_item]



def recommendation(state: state_schema):

    menu=menu_loader()

    prompt=ChatPromptTemplate.from_messages([
        ('system',
        '''You are a restaurant waiter.
        Your only task is to suggest dishes to the customer based on:
        1. Their previous order history
        2. Their current requirements
        3. Their order information
        4. The available menu

        Suggest a maximum of 5 dishes.

        The menu contains:
        restaurant_name, cuisine_type, dish_name, spice_level,
        dish_price, type_of_food, healthy_rating, popularity_score.
        '''),
        ('human',
        "history of customer: {history} \n customer current requirement order: {order} \n order_info: {order_info} \n if something is None it means not provided by the customer you have to manage that on the basis of previous history menu : {menu}")
    ])

    structured_llm=model.with_structured_output(menu_schema)

    chain = prompt | structured_llm
    recommendations=chain.invoke({
        'history':state['history'],
        'order':state['order'],
        'order_info' : state['order_info'],
        'menu': menu
    })

    state['recommendations']=recommendations

    return state
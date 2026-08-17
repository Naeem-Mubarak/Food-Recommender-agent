from typing import TypedDict,Optional,Annotated,List
from langgraph.graph import StateGraph,START,END
from Database.history_loading import found_customer_data
from models.English_translator import english_translator,voice_transcript_generator
from langchain_core.prompts import ChatPromptTemplate
from config.system_info import model
from pydantic import BaseModel,Field
from Database.menu_loader import menu_loader

class state_schema(TypedDict):

    path : str
    user_id : int
    order : str
    order_info : Optional[dict]
    history : Optional[dict]

    recommendations : List[dict]


class history_schema(BaseModel):

    rest_name : Annotated[Optional[str],Field(description='Name of the restaurant')] = None
    dish_name : Annotated[Optional[str],Field(description='Name of the Dish')] = None 
    spice_level : Annotated[Optional[int],Field(description='Level of spice')] = None
    price : Annotated[Optional[int],Field(description='Price of dish')] = None
    type_of_food : Annotated[Optional[str],Field(description='Type of Food veg or non-veg')] = None
    healthy_rating : Annotated[Optional[int],Field(description='How much food is healthy')] = None


def voice_receiver(state : state_schema):

    transcript=voice_transcript_generator(state['path'])
    data=english_translator(transcript)

    state['user_id']=data['id']
    state['order']=data['order']
    state['order_info']=data['order_info']

    return state


def history(state: state_schema):

    data=found_customer_data(state['user_id'])

    prompt=ChatPromptTemplate.from_messages([
        ('system','You are an intelligent AI assistant which can organize data into any form the user demands'),
        ('human','I run a restaurant and i want to suggest my customer according to his past orders so i will give you his past orders you have to organize them in such a way that an LLM can easily understand and return then into the form of python dictionary if order history is an empty list then you can also return an empty dictionary \n order_hisotry={data}')
    ])

    strucutred_llm=model.with_structured_output(history_schema)

    chain = prompt | strucutred_llm
    response = chain.invoke({
        'data':data
    })

    state['history']=response

    return state


class menu_item(TypedDict):

    restaurant_name : str
    cuisine_type : str
    dish_name : str
    spice_level : int
    dish_price : int
    type_of_food : str
    healthy_rating : int
    popularity_score : int


class menu_schema(BaseModel):

    recommendations : List[menu_item]



def select_item(state: state_schema):

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

    return recommendations




graph=StateGraph(state_schema)
graph.add_node('cust_order',voice_receiver)
graph.add_node('history',history)
graph.add_node('recommend',select_item)

graph.add_edge(START,'cust_order')
graph.add_edge('cust_order','history')
graph.add_edge('history','recommend')
graph.add_edge('recommend',END)

workflow=graph.compile()

path=r"/home/naeemmubarak/Desktop/Food Suggestion agent/sample.ogg"

output=workflow.invoke({
    'path':path
})


print(output)


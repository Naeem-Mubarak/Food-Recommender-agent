from Nodes.state import state_schema
from config.system_info import model
from pydantic import BaseModel,Field
from typing import Annotated,Optional,List
from langchain_core.prompts import ChatPromptTemplate
from Database.history_loading import found_customer_data






class history_schema(BaseModel):

    rest_name : Annotated[Optional[str],Field(description='Name of the restaurant')] = None
    dish_name : Annotated[Optional[str],Field(description='Name of the Dish')] = None 
    spice_level : Annotated[Optional[int],Field(description='Level of spice')] = None
    price : Annotated[Optional[int],Field(description='Price of dish')] = None
    type_of_food : Annotated[Optional[str],Field(description='Type of Food veg or non-veg')] = None
    healthy_rating : Annotated[Optional[int],Field(description='How much food is healthy')] = None


class history(BaseModel):

    history : List[history_schema] = []





def history_loader(state: state_schema):

    data=found_customer_data(state['user_id'])

    prompt=ChatPromptTemplate.from_messages([
        ('system','You are an intelligent AI assistant which can organize data into any form the user demands'),
        ('human','I run a restaurant and i want to suggest my customer according to his past orders so i will give you his past orders you have to organize them in such a way that an LLM can easily understand and return then into the form of python dictionary if order history is an empty list then you can also return an empty dictionary \n order_hisotry={data}')
    ])

    strucutred_llm=model.with_structured_output(history)

    chain = prompt | strucutred_llm
    response = chain.invoke({
        'data':data
    })

    state['history']=response

    return state
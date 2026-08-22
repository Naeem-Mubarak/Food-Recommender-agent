from Nodes.state import state_schema
from langgraph.types import interrupt
from config.system_info import model
from pydantic import BaseModel,Field
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate
from Nodes.recommend_dishes_node import menu_item
from models.speech_to_text import voice_transcript_generator
 


class dish_name(BaseModel):

    dish : Annotated[
        str,Field(default=None,description="Dish customer want to eat")
    ]

    data_of_dish : menu_item


def select_item(state : state_schema):

    # interrputing flow to get the final order from the user

    item = interrupt({
        "type" : 'Select dish',
        "message" : "Select the dish you want to final"
    })

    state['path'] = item
    text = voice_transcript_generator(state['path'])
    state['voice'] = text


    # enforcing schema 
    structured_llm=model.with_structured_output(dish_name)

    prompt = ChatPromptTemplate.from_messages([
        ('system',"""You are an intelligent AI agent system extract the dish data(provided by the user) from the menu"""),
        ('human',"""You have one dish selected by the user and then five other dishes(menu) now you have to fetch the complete reocrd of that dish from menu which is closely related to the dish provided by the user from the menu available \n dish_selected_by_user {item} \n menu: {menu}""")
    ])

    chain = prompt | structured_llm

    response = chain.invoke({
        'item' : state['voice'],
        'menu' : state['recommendations']
    })

    # converting pydantic mode to dict so we can extract info easily
    dish = response.model_dump()
    dish = dish['data_of_dish']

    # state updation
    state['selected_item'] = dish

    return state



    








from config.system_info import model
from pydantic import BaseModel,Field
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate
from graph.nodes.recommend_dishes_node import menu_item



class dish_name(BaseModel):

    dish : Annotated[
        str,Field(default=None,description="Dish customer want to eat")
    ]

    data_of_dish : menu_item


# enforcing schema 
structured_llm=model.with_structured_output(dish_name)

prompt = ChatPromptTemplate.from_messages([
    ('system',"""You are an intelligent AI agent system extract the dish data(provided by the user) from the menu"""),
    ('human',"""You have one dish selected by the user and then five other dishes(menu) now you have to fetch the complete reocrd of that dish from menu which is closely related to the dish provided by the user from the menu available \n dish_selected_by_user {item} \n menu: {menu}""")
])

chain = prompt | structured_llm
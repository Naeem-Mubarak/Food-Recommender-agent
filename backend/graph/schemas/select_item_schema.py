from config.system_info import model
from pydantic import BaseModel,Field
from typing import Annotated,Literal
from langchain_core.prompts import ChatPromptTemplate
from graph.schemas.recommend_dishes_schema import menu_item



class dish_name(BaseModel):

    """
    If user liked something and selected then liked_recommendation will become yes and the data of selcted dish will go into data of dish otherwise the recommendations get rejected (no) and there will be nothing in the dish
    """

    liked_recommendation : Annotated[
        Literal['yes','no'],
        Field(default='yes',description='Either user liked that order or not')
    ]

    dish : Annotated[
        str,Field(default=None,description="Dish customer want to eat")
    ]

    data_of_dish : menu_item


# enforcing schema 
structured_llm=model.with_structured_output(dish_name)

prompt = ChatPromptTemplate.from_messages([
    ('system',"""You are an intelligent AI agent system extract the dish data(provided by the user) from the menu or refusal by the user"""),
    ('human',"""There would be two cases wither user selects a dish from the given menu or either he dislikes them and ask for some other options
    1. You have one dish selected by the user and then some other dishes(menu) now you have to fetch the complete reocrd of that dish from menu which is closely related to the dish provided by the user from the menu available \n menu: {menu}
    2. if user says anything like 'recommend me something else', 'i don't like these things', 'do you have some other options then', 'show me some other items' then in the dish you have to pass None and in liked_recommendation you have to pass no because user didn't selected anything
    \n user_response {item}""")
])

chain = prompt | structured_llm
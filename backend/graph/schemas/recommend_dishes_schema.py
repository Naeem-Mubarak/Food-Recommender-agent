from pydantic import BaseModel
from typing import TypedDict,List
from config.system_info import Gemini_model_provider
from langchain_core.prompts import ChatPromptTemplate

model = Gemini_model_provider()

# defining schema which users will see to order
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


# list of dict (dishes) recommended by LLM
class menu_schema(BaseModel):

    recommendations : List[menu_item]


prompt=ChatPromptTemplate.from_messages([
        ('system',
        '''You are a restaurant waiter.
        Your only task is to suggest dishes to the customer based on:
        1. Their previous order history
        2. Their current requirements
        3. Their order information
        4. The available menu
        5. The items he didn't like

        Note : Rememeber one thing while suggesting that if in the provided data there is some dishes in the senction of Dishes user don't like then don't suggest these dishes and if user reject all the dishes of that kind which he wants let say he wants sweet and you have only 2 dishes then recommend him and if he rejects them then now you don't have any dish so simple you can say i don't have any sweet items do you want something else and for the availbility of the dishes you will have menu of the dishes.
        so keep this in mind and handle things carefully.

        Suggest a maximum of 2 dishes.

        The menu contains:
        rest_id, restaurant_name, cuisine_type, dish_id, dish_name, spice_level,
        dish_price, type_of_food, healthy_rating, popularity_score.
        Alert : And if user provides you some of the dishes he don't like then you don't have to recommend him those things
        '''),
        ('human',
        "history of customer: {history} \n customer current requirement order: {order} \n order_info: {order_info} \n if something is None it means not provided by the customer you have to manage that on the basis of previous history. \n menu : {menu} \n Dishes user don't like : {rejected_dishes}")
    ])

# enforcing schema
structured_llm=model.with_structured_output(menu_schema)

chain = prompt | structured_llm

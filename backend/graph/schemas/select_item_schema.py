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
        Field(default='yes',
              description=("Set to 'yes' when the user selects or accepts a recommended dish. "
                "Set to 'no' when the user rejects the recommendations or asks for alternatives.")
            )
    ]

    dish : Annotated[
        str,Field(
                  description=("The name of the dish selected by the user. "
                "Must be None when liked_recommendation is 'no' or he will tell you the number from the recommendation.")
                )
    ]

    data_of_dish : menu_item


# enforcing schema 
structured_llm=model.with_structured_output(dish_name)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a food-ordering assistant responsible for interpreting the user's response
to a list of recommended dishes.

Your task is to determine whether the user selected/accepted a dish or rejected
the recommendations and wants other options.

You MUST follow these rules:

1. SELECTION / ACCEPTANCE
If the user selects, accepts, or clearly expresses a desire for one of the dishes
in the provided menu or he says i want 1st one or 2nd one then you have to check out from the recommendations that which one is first one and which one it second one:
- liked_recommendation = "yes"
- dish = the name of the selected dish
- data_of_dish = the complete matching record from the provided menu

2. REJECTION / ALTERNATIVE REQUEST
If the user rejects the recommendations, dislikes them, or asks for different
options, such as:
- "recommend something else"
- "I don't like these"
- "show me other options"
- "give me something different"
- "none of these"
- "do you have anything else?"
then:
- liked_recommendation = "no"
- dish = None
- data_of_dish = None

3. MENU-ONLY MATCHING
When the user selects a dish, data_of_dish MUST come from the provided menu.
Never invent, modify, or fabricate a menu record.

4. NATURAL LANGUAGE
Understand natural variations of dish names. For example, if the menu contains
"Spicy Chicken Burger" and the user says "I'll take the spicy chicken burger",
treat it as a selection.

5. AMBIGUITY
If the user's response does not clearly select a dish and does not clearly reject
the recommendations, do not invent a selection. Prefer:
- liked_recommendation = "no"
- dish = None
- data_of_dish = None

6. CONSISTENCY
If liked_recommendation = "yes":
    dish MUST NOT be None
    data_of_dish MUST NOT be None

If liked_recommendation = "no":
    dish MUST be None
    data_of_dish MUST be None.
"""
    ),
    (
        "human",
        """
Here is the menu:

{menu}

Here is the user's response:

{item}

Determine whether the user selected one of the recommended dishes or rejected
the recommendations.

Return the structured result according to the rules above.
"""
    )
])

chain = prompt | structured_llm
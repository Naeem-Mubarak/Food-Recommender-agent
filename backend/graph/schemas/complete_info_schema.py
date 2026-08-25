from pydantic import BaseModel,Field
from typing import Optional,Annotated
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate


# Defining schema to allow LLM to extract exaclty these two things from the user order

class order_schema(BaseModel):

    order : Annotated[
        Optional[str],
        Field(description='Order user wants to eat')
    ] = None

    budget : Annotated[
        Optional[int],
        Field(ge=0,description='Budget user have')
    ] = None




prompt = ChatPromptTemplate.from_messages([
        ('system', """Extract the customer's food preference/order and budget.

        Rules:
        - Extract a specific food if mentioned: "I want a burger" → order = "burger".
        - If no food is mentioned, extract the requested preference: "I want something spicy" → order = "spicy".
        - Extract the budget as a numeric value if mentioned.
        - If order or budget is not mentioned, return None for that field.
        - Never guess or invent missing information.
        """),

        ('human', "{order_data}")
    ])

# forcing schema
structured_llm = model.with_structured_output(order_schema)

chain = prompt | structured_llm

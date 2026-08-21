from Nodes.state import state_schema
from langgraph.types import interrupt
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate


# Defining schema to allow LLM to extract exaclty these two things from the user order

class order_schema(BaseModel):

    order : Annotated[
        Optional[str],
        Field(description='Order user wants to eat')
    ]

    budget : Annotated[
        Optional[int],
        Field(ge=0,description='Budget user have')
    ]


def complete_info(state : state_schema):

    # interrupting flow to collect the data from user

    order_data = interrupt({
          'type' : "order info collection",
          'reason' : "missing order information",
          'instruction' : "Enter what you want to eat and what is your budget"
      })

    prompt = ChatPromptTemplate.from_messages([
        ('system','You are an inlligent AI assistant which can extract order and budget from the statement of the customer'),
        ('human',"{order_data}")
    ])

    # forcing schema

    structured_llm = model.with_structured_output(order_schema)

    chain = prompt | structured_llm
    response = chain.invoke({
        'order_data' : order_data
    })

    # converting pydantic object to dict
    output = response.model_dump()

    # state updation

    if output['order'] is not None:
        state['order'] = output['order']

    if output["budget"] is not None:
        state["order_info"]["budget"] = output["budget"]

    return state

    





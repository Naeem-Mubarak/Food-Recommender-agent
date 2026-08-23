from graph.state import state_schema
from langgraph.types import interrupt
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from config.system_info import model
from langchain_core.prompts import ChatPromptTemplate
from models.speech_to_text import voice_transcript_generator


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


def complete_info(state : state_schema):

    current_order = state['order']
    current_budget = state['order_info']['budget']

    if current_order is None and current_budget is None:
        instruction = 'Sir kindly give your order and budget'
    elif current_order is None:
        instruction = 'Sir kindly give your order'
    elif current_budget is None:
        instruction = 'Sir What is your budget'

    # interrupting flow to collect the data from user

    order_data = interrupt({
          'type' : "order info collection",
          'reason' : "missing order information",
          'instruction' : instruction
      })

    state['path'] = order_data
    text = voice_transcript_generator(state['path'])
    state['voice'] = text

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
    response = chain.invoke({
        'order_data' : state['voice']
    })

    # converting pydantic object to dict
    output = response.model_dump()

    # state updation

    if output['order'] is not None:
        state['order'] = output['order']

    if output["budget"] is not None:
        state["order_info"]["budget"] = output["budget"]

    return state

    





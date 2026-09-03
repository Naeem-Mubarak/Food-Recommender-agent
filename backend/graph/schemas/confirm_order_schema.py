from pydantic import BaseModel,Field
from typing import Literal,Annotated
from config.system_info import Gemini_model_provider
from langchain_core.prompts import ChatPromptTemplate


model = Gemini_model_provider()


class confirmation_response(BaseModel):

    sign : Annotated[
        Literal['confirm','not-confirm'],
        Field(default='confirm',description='Either order is final or not')
    ]




# enforcing schema on the LLM
structured_llm=model.with_structured_output(confirmation_response)
prompt = ChatPromptTemplate.from_messages([
    ('system',
    """You are a restaurant waiter.
    The user is confirming whether they want to place the selected order.

    Return:
    - "confirm" if the user wants to place the order.
    - "not-confirm" if the user does not want to place the order.
    """),
    ('human','{confirmation}')
])

chain2 = prompt | structured_llm

from config.system_info import Gemini_model_provider
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
from typing import Annotated


model = Gemini_model_provider()

class id_getter(BaseModel):

    u_id : Annotated[int,Field(default=None,ge=0,description="id of the user")]
    name : Annotated[str,Field(default=None,description="Name of the user")]



prompt = ChatPromptTemplate.from_messages([
    ("system",
            """
    You extract a user's ID and it's namefrom their message.
    Rules:
    1. A valid ID MUST be a number.
    2. Extract the number regardless of what words surround it.
    3. If the user mentions the word "ID" but does not provide a number,
    there is NO valid ID.
    4. Ignore all non-numeric information.
    5. Do not interpret words such as "my id", "ID", "identifier", etc.
    as an ID by themselves.
    6. If a numeric value exists in the message, return that number as u_id.
    7. Most important thing is there no number then return None and if there is no name then return None
    """),
        ("human", "{user_input}")
    ])

structured_llm = model.with_structured_output(id_getter)
chain = prompt | structured_llm

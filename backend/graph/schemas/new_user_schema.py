from langchain_core.prompts import ChatPromptTemplate
from config.system_info import Gemini_model_provider
from pydantic import BaseModel,Field
from typing import Optional,Annotated

model = Gemini_model_provider()


class name_schema(BaseModel):

     name : Annotated[
          Optional[str],
          Field(default=None,description='Name of the user')
     ]



prompt = ChatPromptTemplate.from_messages([
                ('system',"""You are an intelligent AI assistant so you have to fetch the name of from the given sentence. Instructions:                                                                                         - if nothing feels like name then return None.
                - Try you level best to find the name.
                - Don't pick useless things as name the name must be clear."""),
                ('human',"{text}")
            ])

# enforcing schema
structured_llm = model.with_structured_output(name_schema)

chain = prompt | structured_llm
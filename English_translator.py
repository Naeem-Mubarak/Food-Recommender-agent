from config import translator_llm_prompt
from voice_llm import voice_transcript_generator,path
from pydantic import BaseModel,Field
from typing import Annotated,Optional,Dict
from config import model




class order_info(BaseModel):

    taste : Annotated[Optional[str],Field(description='taste of food customer orders spicy or sweet')]
    budget : Annotated[Optional[str],Field(description='Budget of the user')]


class order_schema(BaseModel):

    id : Annotated[int,Field(ge=1,description='Unique id of the customer')]
    name : Annotated[str,Field(description='Name of the customer')]
    order : Annotated[str,Field(description='Order customer interested in')]
    order_info : order_info





def english_translator(data):

    
    structured_llm=model.with_structured_output(order_schema)
    chain = translator_llm_prompt | structured_llm
    response = chain.invoke({
        'sentence': data
    })

    output=response.model_dump()

    return output

from config.prompts import translator_llm_prompt
from pydantic import BaseModel,Field
from typing import Annotated,Optional
from config.system_info import model

from models.speech_to_text import voice_transcript_generator

# Schema which enforced the LLM to give output according to that
class order_info(BaseModel):

    type_of_food : Annotated[Optional[str],Field(default=None,description='taste of food customer orders spicy or sweet')]

    budget : Annotated[Optional[int],Field(default=None,description='Budget of the user')]

    spice_level : Annotated[Optional[int],Field(ge=0,le=10,default=0,description="rate sweet or spice according to the taste factor provided by the user if there is something")]

    sugar_level : Annotated[Optional[int],Field(ge=0,le=10,default=0,description="rate sweet level according to the taste factor provided by the user if there is something ")]


class order_schema(BaseModel):

    order : Annotated[Optional[str],Field(default=None,description='Order customer interested in')]
    
    order_info : order_info





def english_translator(data):

    
    structured_llm=model.with_structured_output(order_schema)
    chain = translator_llm_prompt | structured_llm
    response = chain.invoke({
        'sentence': data
    })

    output=response.model_dump()

    return output


# path = r"/home/naeemmubarak/Desktop/Food Suggestion agent/complete_info.wav"






# text=voice_transcript_generator(path)
# data=english_translator(text)
# print(data)

# {'order': None, 'order_info': {'type_of_food': None, 'budget': 0, 'spice_level': 0, 'sugar_level': 0}}


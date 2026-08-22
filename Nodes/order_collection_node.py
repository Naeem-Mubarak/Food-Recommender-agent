from Nodes.state import state_schema
from langgraph.types import interrupt
from models.speech_to_text import voice_transcript_generator
from models.English_translator import english_translator


def order_collection(state : state_schema):

    # interrupting flow to collect the data from user
    order_data = interrupt({
          'type' : "order info collection",
          'instruction' : "Tell me what kind of eatable you want"
      })

    state['path'] = order_data
    text = voice_transcript_generator(state['path'])
    order_info = english_translator(text)

    
    # state updation
    state['order'] = order_info['order']
    state["order_info"] = order_info['order_info']

    return state

    





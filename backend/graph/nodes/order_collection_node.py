from graph.agent_schema import state_schema
from langgraph.types import interrupt
from models.data_extractor import english_translator


def order_collection(state : state_schema):

    # interrupting flow to collect the data from user
    order_data = interrupt({
          'type' : "order info collection",
          'instruction' : "Tell me what kind of eatable you want"
      })

    state['text'] = order_data
    order_info = english_translator(state['text'])

    
    # state updation
    state['order'] = order_info['order']
    state["order_info"] = order_info['order_info']

    return state

    





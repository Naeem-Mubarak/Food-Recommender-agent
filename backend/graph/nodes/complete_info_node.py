from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.complete_info_schema import chain



def complete_info(state : state_schema):

    """Asking for info missed by user but agent requires for it's further processing"""

    current_order = state['order']
    current_budget = state['order_info']['budget']

    if current_order is None and current_budget is None:
        instruction = 'Sir kindly give your order and budget'
    elif current_order is None:
        instruction = 'Sir kindly give your order'
    elif current_budget is None or current_budget == 0:
        instruction = 'Sir What is your budget'


    # interrupting flow to collect the data from user
    order_data = interrupt({
          'type' : "order info collection",
          'reason' : "missing order information",
          'instruction' : instruction
      })

    state['text'] = order_data

    response = chain.invoke({
        'order_data' : state['text']
    })

    # converting pydantic object to dict
    output = response.model_dump()


    # state updation
    if output['order'] is not None:
        state['order'] = output['order']

    if output["budget"] is not None:
        state["order_info"]["budget"] = output["budget"]

    return state

    





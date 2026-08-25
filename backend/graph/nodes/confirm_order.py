from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.confirm_order_schema import chain1,chain2


def order_confirmation(state : state_schema):

    """Extracting selected item from the user and then update the state and then asking user for the confirmation and update the state for further process"""

    item = state['selected_item'] 

    message = chain1.invoke({
        'item' : item
    })

    confirmation = interrupt({
        'type' : 'confirmation',
        'instruction' : f'{message}'
    })

    state['text'] = confirmation

    response = chain2.invoke({
        'confirmation' : state['text']
    })

    # converting pydantic object to dict
    response=response.model_dump()

    # state updation
    state['confirm_order'] = response['sign']

    return state
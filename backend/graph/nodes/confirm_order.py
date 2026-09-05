from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.confirm_order_schema import chain2


def format_order(item: dict) -> str:

    """Formatting the order so agent can ask user for confirmation"""

    return (
        f"Do you want to confirm {item['dish_name']} from {item['restaurant_name']}, "
        f"spice level {item['spice_level']} out of five, priced at {item['dish_price']} rupees?"
    )


def order_confirmation(state : state_schema):

    """Extracting selected item from the user and then update the state and then asking user for the confirmation and update the state for further process"""

    item = state['selected_item'] 

    message = format_order(item)

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
from graph.agent_schema import state_schema
from langgraph.types import interrupt
from schemas.select_item_schema import chain



def select_item(state : state_schema):

    """
    accept user order which is selected from the recommendations provided by the agent and then updates the state
    """

    # interrputing flow to get the final order from the user
    item = interrupt({
        "type" : 'Select dish',
        "instruction" : "Select the dish you want to final"
    })

    state['voice'] = item

    response = chain.invoke({
        'item' : state['text'],
        'menu' : state['recommendations']
    })

    # converting pydantic mode to dict so we can extract info easily
    dish = response.model_dump()
    dish = dish['data_of_dish']

    # state updation
    state['selected_item'] = dish

    return state



    








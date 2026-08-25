from graph.agent_schema import state_schema
from database.history_loading import found_customer_data
from graph.schemas.history_loader_schema import chain




def history_loader(state: state_schema):

    """Loading history of the user and organizing history in a structured manner and updating state for further processing"""

    # history of the current user
    data=found_customer_data(state['user_id'])

    response = chain.invoke({
        'data':data
    })

    # state updation
    state['history']=response.model_dump()

    return state
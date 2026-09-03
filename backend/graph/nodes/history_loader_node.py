from graph.agent_schema import state_schema
from database.history_loading import found_customer_data




def history_loader(state: state_schema):

    """Loading history of the user and organizing history in a structured manner and updating state for further processing"""

    # history of the current user
    data=found_customer_data(state['user_id'])

    cols = ['restaurant_name', 'dish_name', 'spice_level', 'sweet_level' , 'price', 'type_of_food', 'healthy_rating']
    order_history = [dict(zip(cols,row)) for row in data]

    # state updation
    state['history']=order_history

    return state
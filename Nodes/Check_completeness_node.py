from Nodes.state import state_schema

def check_completeness_node(state : state_schema):

    """
    Both order and budget are must to be passed in the order info if any of these two is missing then the state get updated to missing the info and agent ask for entering info again
    """


    order = state['order']
    budget = state['order_info']['budget']

    if order is None:

        state['order_eval'] = 'missing'

        return state

    missing_budget = budget is None or budget == 0

    if missing_budget:

        state['order_eval'] = 'missing'
        return state

    else:
        state['order_eval'] = 'complete'
        return state

from Nodes.state import state_schema

def check_completeness_node(state : state_schema):


    order = state['order']
    budget = state['order_info']['budget']

    if order is None:

        state['order_eval'] = 'missing'

        return state

    missing_budget = (budget == 0)

    if missing_budget:

        state['order_eval'] = 'missing'
        return state

    else:
        state['order_eval'] = 'complete'
        return state

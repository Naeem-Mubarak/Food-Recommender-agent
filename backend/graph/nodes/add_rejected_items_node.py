from graph.agent_schema import state_schema

def add_rejected_items(state: state_schema):


    """
    if the order is rejected by the user then add the rejected or discarded order in the agent's memory so he didn't suggest these items in next iteration 
    """

    if state['recommendation_satisfaction'] == 'no':

        # passing recommendations in list because we used an reducer function to accumulate dishes 
        state['rejected_recommendations'] = [state['recommendations']]

    return state

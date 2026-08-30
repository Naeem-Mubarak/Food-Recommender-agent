from graph.agent_schema import state_schema

def add_rejected_items(state: state_schema):


    """
    if the order is rejected by the user then add the rejected or discarded order in the agent's memory so he didn't suggest these items in next iteration 
    """

    if state['recommendation_satisfaction'] == 'no':

        # accumulating the list of rejected items which user rejected so they don't come again in the recommendation of user again
        state['rejected_recommendations'] = state.get(['rejected_recommendations'],[]) + [state['recommendations']]

    return state

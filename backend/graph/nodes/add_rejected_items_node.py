from graph.agent_schema import state_schema

def add_rejected_items(state: state_schema):

    if state['recommendation_satisfaction'] == 'no':
        
        state['rejected_recommendations'] = [state['recommendations']]

    return state

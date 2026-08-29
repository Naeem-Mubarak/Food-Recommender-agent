from graph.agent_schema import state_schema


def initial_state() -> state_schema:

    """Initial state of agent"""
    
    return {
        'text': None,
        'user_id': None,
        'name': None,
        'evaluator': None,
        'order': None,
        'order_info': None,
        'history': [],
        'order_eval': None,
        'recommendations': [],
        'iteration': 0,
        'recommendation_satisfaction': None,
        'rejected_recommendations': [],
        'selected_item': {},
        'confirm_order': None
    }
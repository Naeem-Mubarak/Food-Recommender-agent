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
        'history': None,
        'order_eval': None,
        'recommendations': None,
        'iteration': None,
        'recommendation_satisfaction': None,
        'rejected_recommendations': None,
        'selected_item': None,
        'confirm_order': None
    }
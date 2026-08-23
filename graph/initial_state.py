from graph.state import state_schema

def create_initial_state(path: str) -> state_schema:
    return {
        'path': path,
        'voice': None,
        'user_id': None,
        'name': None,
        'evaluator': None,
        'order': None,
        'order_info': None,
        'history': None,
        'order_eval': None,
        'recommendations': None,
        'selected_item': None,
        'confirm_order': None
    }
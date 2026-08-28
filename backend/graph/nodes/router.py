from graph.agent_schema import state_schema
from typing import Literal



def router(state : state_schema) -> Literal['data_receiver','check_user']:

    """
    A new user genuinely has no ID to give - only a missing name means
    we need to ask again. check_user already handles a None user_id
    correctly (no match found -> routed to new_user).
    """

    if state['name'] is None:

        return 'data_receiver'
    else:
        return 'check_user'

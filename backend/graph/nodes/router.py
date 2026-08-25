from graph.agent_schema import state_schema
from typing import Literal



def router(state : state_schema) -> Literal['data_receiver','check_user']:

    """
    Ensuring move to the check user if both fields are provided if even one of these is missing then enter info again
    """

    if state['user_id'] is None or state['name'] is None:

        return 'data_receiver'
    else:
        return 'check_user'
from Nodes.state import state_schema
from typing import Literal



def router(state : state_schema) -> Literal['reciever','order_collection']:

    """
    Ensuring move to the check user if both fields are provided if even one of these is missing then enter info again
    """

    if state['user_id'] or state['name'] == None:

        return 'reciever'
    else:
        return 'order_collection'
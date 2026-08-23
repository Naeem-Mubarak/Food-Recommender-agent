from graph.state import state_schema
from typing import Literal



def confirmation_node(state: state_schema) -> Literal['update_db','select_item']:

    """
    router function which routes the flow to update_db final node if user confirm the order other wise go back to select item to choose order again 
    """

    if state['confirm_order'] == 'confirm':

        return 'update_db'
    return 'select_item'


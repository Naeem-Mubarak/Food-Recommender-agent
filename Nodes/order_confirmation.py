from Nodes.state import state_schema
from typing import Literal



def confirmation_node(state: state_schema) -> Literal['update_db','select_item']:

    if state['confirm_order'] == 'confirm':

        return 'update_db'
    return 'select_item'


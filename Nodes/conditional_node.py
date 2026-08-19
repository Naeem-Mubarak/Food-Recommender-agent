from Nodes.state import state_schema
from typing import Literal



def conditional_node(state : state_schema) -> Literal['new_user_node','history_loader']:

    if state['evaluator']=='correct':

        return 'history_loader'
    
    return 'new_user_node'    

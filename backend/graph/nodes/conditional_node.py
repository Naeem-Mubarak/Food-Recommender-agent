from graph.agent_schema import state_schema
from typing import Literal



def conditional_node(state : state_schema) -> Literal['new_user','history_loader']:

    """
    routes the flow according to the condition if user information is correc then load it's hisotry otherwise move it to the new user node which generates id automatically and tells the user (which user need to remember to visit next time) and then user has to tell it's name.
    """

    if state['evaluator']=='correct':

        return 'history_loader'
    
    return 'new_user'    

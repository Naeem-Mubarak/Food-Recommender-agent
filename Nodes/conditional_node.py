from config.system_info import DB_PATH
from Nodes.state import state_schema
from Database.db_connection import db_connection
from typing import Literal


cursor, conn =db_connection(DB_PATH)

def conditional_node(state : state_schema) -> Literal['new_user_node','history_loader']:

    if state['evaluator']=='correct':

        return 'history_loader'
    
    return 'new_user_node'    

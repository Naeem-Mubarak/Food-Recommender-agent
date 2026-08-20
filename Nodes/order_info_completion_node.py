from Nodes.state import state_schema
from typing import Literal


def order_info_completion(state : state_schema):

    if state['order_eval'] == 'missing':

        return 'complete_info'

    return 'recommendations'
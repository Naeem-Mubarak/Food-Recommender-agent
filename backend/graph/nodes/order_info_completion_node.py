from graph.agent_schema import state_schema
from typing import Literal


def order_info_completion(state : state_schema) -> Literal['complete_info','recommendations']:

    """
    if order have information which are mandantory to recommend things then the flows go to recommendations node otherwise it will loop to the complete info node untils the order info in not completed
    """

    if state['order_eval'] == 'missing':

        return 'complete_info'

    return 'recommendations'
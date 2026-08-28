from graph.agent_schema import state_schema
from typing import Literal

def liked_or_disliked_recommendation_router(state : state_schema) -> Literal['recommendations','order_confirmation','order_collection','Rejected']:

    if state['iteration'] < 3:

        if (state['recommendation_satisfaction'] == 'yes') and (state['selected_item'] is not None):

            return 'order_confirmation'

        else:
            return 'Rejected'

    else:

        return 'order_collection'
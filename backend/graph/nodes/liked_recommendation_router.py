from graph.agent_schema import state_schema
from typing import Literal

def liked_or_disliked_recommendation_router(state : state_schema) -> Literal['order_confirmation','order_collection','Rejected']:


    """
    A user is allowed to reject item maximum of 3 times after that the user have to give order again and during rejection every rejected item will get stored and the agent will not recommend any thing from that after every rejection and if nothing is rejected then order confirmation step start's
    """

    if state['iteration'] < 3:

        if (state['recommendation_satisfaction'] == 'yes') and (state['selected_item'] is not None):

            return 'order_confirmation'

        else:
            return 'Rejected'

    else:

        return 'order_collection'
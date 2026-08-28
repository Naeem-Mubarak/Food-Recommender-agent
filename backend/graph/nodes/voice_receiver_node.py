from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.voice_receiver_schema import chain



def reciever_node(state : state_schema):

    """
    Receives the name and ID of the user and then update the state for further processing.
    A missing ID is expected and fine for a new user - only a missing
    name triggers a retry, since name is genuinely required.
    """

    retry_note = None

    while True:

        instruction = (
            "[Charming] [Joyful] Hello and welcome to our website. "
            "Wanna use our service? Tell me your name, and your ID if you already have one."
        )
        if retry_note:
            instruction = (
                f"I heard '{retry_note}' but couldn't catch your name clearly. "
                f"Could you please say your name again?"
            )

        start = interrupt({
            'type' : 'Starting agent',
            'instruction' : instruction
        })

        state['text'] = start

        response = chain.invoke({
            'user_input' : state['text']
        })

        response = response.model_dump()

        if response['name'] is None:
            retry_note = state['text']
            continue

        state['user_id'] = response['u_id']
        state['name'] = response['name']

        return state

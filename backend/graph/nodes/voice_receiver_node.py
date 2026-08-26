from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.voice_receiver_schema import chain



def reciever_node(state : state_schema):

    """
    Receives the name and ID of the user and then update the state for further processing.
    """

    start = interrupt({
        'type' : 'Starting agent',
        'instruction' : "[Charming] [Joyful] Hellooo and welcome to our website\n Tell me what can i do for you. "
    })

    state['text'] = start

    response = chain.invoke({
        'user_input' : state['text']
    })

    response = response.model_dump()
    state['user_id'] = response['u_id']
    state['name'] = response['name']

    return state


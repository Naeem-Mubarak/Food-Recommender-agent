from models.speech_to_text import voice_transcript_generator
from models.English_translator import english_translator
from Nodes.state import state_schema





def voice_receiver(state : state_schema):

    transcript=voice_transcript_generator(state['voice'])
    data=english_translator(transcript)

    state['user_id'] = data['id']
    state['name'] = data['name']
    state['order'] = data['order']
    state['order_info'] = data['order_info']

    return state
from models.speech_to_text import voice_transcript_generator
from models.English_translator import english_translator
from Nodes.state import state_schema





def parser(state : state_schema):

    transcript=voice_transcript_generator(state['voice'])
    data=english_translator(transcript)

    state['order'] = data['order']
    state['order_info'] = data['order_info']

    return state
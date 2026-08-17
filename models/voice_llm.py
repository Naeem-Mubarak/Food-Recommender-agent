import os
from groq import Groq
from config import voice_llm_prompt




STT_model=Groq(api_key=os.getenv('GROQ_API_KEY'))


def voice_transcript_generator(path):

    with open(path,'rb') as file:
        data=STT_model.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3",
                prompt=voice_llm_prompt,
                language='ur',
                temperature=0,
            )
    return data.text
path='sample.ogg'



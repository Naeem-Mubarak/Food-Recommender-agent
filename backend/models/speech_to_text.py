from config.system_info import Groq_client_provider
from config.prompts import voice_llm_prompt
from io import BytesIO


groq_client= Groq_client_provider()

async def voice_transcript_generator(voice : bytes):

    audio_file = BytesIO(voice)
    # Groq's API needs a filename hint, even in-memory
    audio_file.name = 'audio.wav'
    
    data = await groq_client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        prompt=voice_llm_prompt,
        language='en',
        temperature=0,
        )
    
    return data.text

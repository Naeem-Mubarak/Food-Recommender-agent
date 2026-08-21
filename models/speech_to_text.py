from config.system_info import groq_client
from config.prompts import voice_llm_prompt
import io



def voice_transcript_generator(audio_bytes):
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # Groq's API needs a filename hint, even in-memory

    data = groq_client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        prompt=voice_llm_prompt,
        language='en',
        temperature=0,
    )
    return data.text



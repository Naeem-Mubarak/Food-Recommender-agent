from config.system_info import groq_client



async def text_to_speech(text: str, voice: str = "hannah") -> bytes:
    """
    Converts text to speech. Returns raw audio bytes - nothing written to disk.
    """
    response = await groq_client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice=voice,
        input=text,
        response_format="wav"
    )
    speech =  await response.read()

    return speech
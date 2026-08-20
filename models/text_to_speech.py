from kokoro import KPipeline
import soundfile as sf
import numpy as np


async def text_to_speech_stream(text, websocket):
    pipeline = KPipeline(lang_code="a")
    generator = pipeline(text, voice="af_heart")

    for graphemes, phonemes, audio in generator:
        audio_bytes = audio.astype(np.float32).tobytes()
        await websocket.send_bytes(audio_bytes) 
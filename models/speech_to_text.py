from config.system_info import groq_client
from config.prompts import voice_llm_prompt
import io

# audio_file = io.BytesIO(audio_bytes)
    # audio_file.name = "audio.wav"  # Groq's API needs a filename hint, even in-memory

def voice_transcript_generator(path):
    
    with open(path,'rb') as f:
        data = groq_client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",
            prompt=voice_llm_prompt,
            language='en',
            temperature=0,
            )
    return data.text

# path = r"/home/naeemmubarak/Desktop/Food Suggestion agent/confirmation.wav"
# text = voice_transcript_generator(path)
# print(text)


# import os
# from groq import Groq

# client = Groq(api_key=os.getenv('GROQ_API_KEY'))


# def text_to_speech(text: str, output_path: str = "output.wav", voice: str = "troy") -> str:
#     """
#     Converts text to speech using Groq's Orpheus model and saves it to a file.

#     Args:
#         text: the text to convert to speech (supports vocal direction tags like [cheerful], [whisper])
#         output_path: where to save the generated .wav file
#         voice: which Orpheus voice to use (e.g. "hannah", "troy")

#     Returns:
#         the output_path, so the caller can immediately use it (e.g. send over a websocket)
#     """
#     response = client.audio.speech.create(
#         model="canopylabs/orpheus-v1-english",
#         voice=voice,
#         input=text,
#         response_format="wav"
#     )
#     response.write_to_file(output_path)
#     return output_path


# path = text_to_speech(
#         "[cheerful] Hi! my name is Naeem and my ID is 2",
#         output_path="test_output2.wav",
#         voice="hannah"
#     )
# print(f"Saved to {path}")
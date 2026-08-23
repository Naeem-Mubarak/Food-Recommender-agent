import os
from config.system_info import groq_client



def text_to_speech(text: str, voice: str = "hannah") -> bytes:
    """
    Converts text to speech. Returns raw audio bytes - nothing written to disk.
    """
    response = groq_client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice=voice,
        input=text,
        response_format="wav"
    )
    return response.read()



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
#         "Hmm ok so select the first one",
#         output_path="dish_selection.wav",
#         voice="hannah"
#     )
# print(f"Saved to {path}")
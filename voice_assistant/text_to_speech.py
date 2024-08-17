# voice_assistant/text_to_speech.py
import logging
import elevenlabs
from openai import OpenAI
from deepgram import DeepgramClient, SpeakOptions
from elevenlabs.client import ElevenLabs
from cartesia import Cartesia
import pyaudio
import soundfile as sf
import json


from voice_assistant.local_tts_generation import generate_audio_file_melotts

def text_to_speech(model, api_key, text, output_file_path, local_model_path=None, selected_voice_id=None):
    """
    Convert text to speech using the specified model.
    
    Args:
    model (str): The model to use for TTS ('openai', 'deepgram', 'elevenlabs', 'local', 'cartesia').
    api_key (str): The API key for the TTS service.
    text (str): The text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    local_model_path (str): The path to the local model (if applicable).
    selected_voice_id (str): The ID of the selected voice for Cartesia (if applicable).
    """
    
    try:
        if model == 'openai':
            client = OpenAI(api_key=api_key)
            speech_response = client.audio.speech.create(
                model="tts-1",
                voice="fable",
                input=text
            )
            speech_response.stream_to_file(output_file_path)

        elif model == 'deepgram':
            client = DeepgramClient(api_key=api_key)
            options = SpeakOptions(
                model="aura-arcas-en",
                encoding="linear16",
                container="wav"
            )
            SPEAK_OPTIONS = {"text": text}
            response = client.speak.v("1").save(output_file_path, SPEAK_OPTIONS, options)

        elif model == 'elevenlabs':
            ELEVENLABS_VOICE_ID = "Paul J."
            client = ElevenLabs(api_key=api_key)
            audio = client.generate(
                text=text, voice=ELEVENLABS_VOICE_ID, output_format="mp3_22050_32", model="eleven_turbo_v2"
            )
            elevenlabs.save(audio, output_file_path)

        elif model == "cartesia":
            client = Cartesia(api_key=api_key)
            
            # Use the selected_voice_id if provided, otherwise use a default
            voice_id = selected_voice_id or "a0e99841-438c-4a64-b679-ae501e7d6091"
            voice = client.voices.get(id=voice_id)

            model_id = "sonic-english"
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

            p = pyaudio.PyAudio()
            rate = 44100
            stream = None

            # Generate and stream audio
            for output in client.tts.sse(
                model_id=model_id,
                transcript=text,
                voice_id=voice_id,  # Use voice_id instead of voice_embedding
                stream=True,
                output_format=output_format,
            ):
                buffer = output["audio"]

                if not stream:
                    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

                # Write the audio data to the stream
                stream.write(buffer)

            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()

        elif model == "melotts":  # this is a local model
            generate_audio_file_melotts(text=text, filename=output_file_path)

        elif model == 'local':
            # Placeholder for local TTS model
            with open(output_file_path, "wb") as f:
                f.write(b"Local TTS audio data")

        else:
            raise ValueError("Unsupported TTS model")

    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")

def get_cartesia_voices(api_key):
    """
    Get the list of available voices from Cartesia.
    
    Args:
    api_key (str): The API key for the Cartesia service.
    
    Returns:
    list: A list of available voices.
    """
    client = Cartesia(api_key=api_key)
    return client.voices.list()

def select_voice(voices):
    """
    Allow the user to select a voice from the list of available voices.
    
    Args:
    voices (list): A list of available voices.
    
    Returns:
    str: The ID of the selected voice.
    """
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice['name']}")
    
    while True:
        try:
            choice = int(input("Select a voice number: ")) - 1
            if 0 <= choice < len(voices):
                return voices[choice]['id']
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
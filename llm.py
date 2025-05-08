import os
import time
import subprocess
import pyaudio
import wave
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Audio recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recording.wav"

# Command dictionary - add your own commands and actions
COMMANDS = {
    "make coffee": "echo 'coffee in the making'",
    "coffee" : "stop",
    "stop recording": "exit"
}

def record_audio():
    """Record audio from microphone"""
    print("Recording...")
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def transcribe_audio():
    """Transcribe audio using OpenAI Whisper API"""
    try:
        with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        return transcription.text.lower()
    except Exception as e:
        print(f"Error in transcription: {e}")
        return ""

def process_command(text):
    """Process transcribed text and execute commands"""
    print(f"Transcribed text: {text}")
    
    for command, action in COMMANDS.items():
        if command in text:
            print(f"Recognized command: {command}")
            
            if action == "stop":
                print("Stopping the program.")
                return False  # This will end the loop in main()
            
            # Execute shell command
            print(f"Executing: {action}")
            result = subprocess.run(action, shell=True, capture_output=True, text=True)
            print(f"Result: {result.stdout}")
            return True

    print("No matching command found")
    return True

def main():
    print("Voice Command System Started")
    print("Available commands:", list(COMMANDS.keys()))
    
    running = True
    while running:
        record_audio()
        text = transcribe_audio()
        if text:
            running = process_command(text)
        time.sleep(1)
    
    print("Program stopped")

if __name__ == "__main__":
    main()
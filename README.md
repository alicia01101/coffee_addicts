# ☕ Voice-Controlled Coffee Machine with Raspberry Pi

This project enables hands-free control of a coffee machine using voice commands. It uses a USB microphone to capture audio, OpenAI's Whisper API for transcription, and predefined actions (e.g., servo motor control) to execute commands such as "make coffee".

---

## 📁 Repository Structure

.
├── llm.py # Main script for audio recording, transcription & command processing
├── test.py # Script for testing and controlling the servo motor
├── recording.wav # Audio file recorded from microphone (overwritten each run)
├── .env # Contains the OpenAI API key (not included in repo)
└── README.md # Project documentation


---

## 🔧 Requirements

Install dependencies with:

```bash
pip install openai pyaudio python-dotenv numpy

Make sure you also have ffmpeg installed (required for audio processing by Whisper):

sudo apt install ffmpeg
``

🔑 Setup

    OpenAI API Key
    Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key_here

Microphone Access
Make sure your USB microphone is recognized by the Raspberry Pi:

    arecord -l

    Servo Setup
    Ensure your servo motor is properly connected to a GPIO pin (used by test.py).

🧠 How It Works
llm.py — Voice Command Processor

This script does the following:

    Records 5 seconds of audio from the microphone.

    Sends the .wav file to OpenAI Whisper for transcription.

    Checks the transcription for predefined keywords.

    If a known command is found, executes the corresponding action (e.g. terminal command or script).

    Repeats until the keyword stop recording is spoken.

Available Commands

You can define commands in the COMMANDS dictionary:

COMMANDS = {
    "make coffee": "echo 'coffee in the making'",
    "coffee": "stop",  # Stops the script
    "stop recording": "exit"
}

test.py — Servo Motor Control

This script is used to test and trigger a servo motor that simulates pressing the button on a coffee machine. Example features:

    Sets the servo angle to press and release.

    Use this as the backend action for the "make coffee" command.

    Replace the echo command in llm.py with something like:

    "make coffee": "python3 test.py"

🚀 Usage

To start the voice control loop:

python3 llm.py

To test the servo motor separately:

python3 test.py

🔍 Notes

    llm.py will keep running until a stop command is recognized.

    You can extend the COMMANDS dictionary to add more smart home actions.

    Make sure your Raspberry Pi has internet access to reach OpenAI's API.

🧩 Future Improvements

    Local model inference (Whisper offline)

    Improved wake-word detection

    MQTT integration for smart home environments

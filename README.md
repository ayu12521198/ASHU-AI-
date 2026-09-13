# ASHU AI

ASHU is a Windows voice assistant that uses a local Ollama model for its AI
brain, SpeechRecognition for microphone input, and Windows SAPI5 for spoken
output. It supports Hindi, Hinglish, and English conversation.

## Requirements

- Windows 10 or newer
- Python 3.10 or newer
- Ollama for Windows
- A working microphone
- Internet access for Google Speech Recognition

Install Ollama from <https://ollama.com/download/windows>, then verify it:

```powershell
ollama --version
ollama pull llama3.2
```

## Installation

Run these commands from the project folder:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On some systems, installing `PyAudio` may require a prebuilt wheel compatible
with the installed Python version. Python 3.12 is recommended on Windows.

## Run

```powershell
python main.py
```

You can also double-click `start.bat`. From Command Prompt, type `start` in
this project folder. From PowerShell, use `.\start.bat` because PowerShell already reserves
`start` as a built-in command.

ASHU checks Ollama, starts its local service when needed, downloads
`llama3.2` if it is missing, calibrates the microphone, selects Microsoft Zira
Desktop when available, and starts continuous voice conversation.

Say **Hey ASHU** to get ASHU's attention, or speak continuously after startup.
Say **stop listening**, **exit ASHU**, or **goodbye** to stop the program.

Supported safe commands include asking who ASHU is, checking its status, opening
YouTube, Google, Chrome, Notepad, Calculator, and VS Code, checking the time or
date, and searching the web. Voice input is never treated as an arbitrary shell
command.

## Troubleshooting

- Allow microphone access in Windows Settings under Privacy and security.
- Check that the correct microphone is selected in Windows sound settings.
- If Ollama is not found, restart PowerShell after installing Ollama so PATH is refreshed.
- If Microsoft Zira is unavailable, ASHU uses the default Windows SAPI5 voice.
- Speech recognition needs an internet connection; Ollama responses remain local.
- Run commands while the `venv` environment is activated.


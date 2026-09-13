"""Configuration for the ASHU voice assistant."""

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "llama3.2"
OLLAMA_REQUEST_TIMEOUT = 120
OLLAMA_START_TIMEOUT = 20

ASSISTANT_NAME = "ASHU"
USER_NAME = "Ayush"
WAKE_WORDS = ("hey ashu", "hey ash", "ashu", "अशु", "आशु", "हे आशु", "हे एशू")

LISTEN_TIMEOUT = 6
PHRASE_TIME_LIMIT = 12
AMBIENT_NOISE_DURATION = 1

SPEECH_RATE = 175
SPEECH_VOLUME = 1.0

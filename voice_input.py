"""Microphone input using SpeechRecognition and Google's speech service."""

from __future__ import annotations

import speech_recognition as sr

from config import AMBIENT_NOISE_DURATION, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT


class VoiceInput:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        print("Microphone ready.")
        with self.microphone as source:
            print("Calibrating microphone for background noise...")
            self.recognizer.adjust_for_ambient_noise(
                source, duration=AMBIENT_NOISE_DURATION
            )

    def listen(self) -> str | None:
        print("\n🎙️ Listening...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT,
                    phrase_time_limit=PHRASE_TIME_LIMIT,
                )
        except sr.WaitTimeoutError:
            return None
        except (OSError, sr.RequestError) as error:
            print(f"Microphone error: {error}")
            return None

        # Hindi handles Hindi, Hinglish, and many English words well. The
        # English fallback helps when Hindi recognition cannot decode a phrase.
        for language in ("hi-IN", "en-IN"):
            try:
                text = self.recognizer.recognize_google(audio, language=language)
                if text.strip():
                    return text.strip()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Speech recognition needs an internet connection.")
                return None
        print("I could not understand that. Please try again.")
        return None

"""Windows SAPI5 speech output through pyttsx3."""

from __future__ import annotations

import re
import subprocess

import pyttsx3

from config import SPEECH_RATE, SPEECH_VOLUME


class VoiceOutput:
    def __init__(self) -> None:
        self.engine = pyttsx3.init("sapi5")
        self.engine.setProperty("rate", SPEECH_RATE)
        self.engine.setProperty("volume", SPEECH_VOLUME)
        self.voice_name = self._select_voice()
        if self.voice_name:
            print(f"Voice ready: {self.voice_name}")
        else:
            print("Microsoft Zira was not found; using the default Windows voice.")

    def _select_voice(self) -> str | None:
        voices = self.engine.getProperty("voices") or []
        fallback_id = voices[0].id if voices else None
        selected_id = fallback_id
        selected_name = voices[0].name if voices else None
        for voice in voices:
            name = str(getattr(voice, "name", ""))
            if "zira" in name.casefold():
                selected_id = voice.id
                selected_name = name
                break
        if selected_id:
            self.engine.setProperty("voice", selected_id)
        return selected_name

    @staticmethod
    def _spoken_text(text: str) -> str:
        text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
        text = re.sub(r"[*_#>`~]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def speak(self, text: str) -> None:
        clean_text = self._spoken_text(text)
        if not clean_text:
            return
        print(f"🤖 ASHU: {clean_text}")
        try:
            self._speak_with_windows_sapi(clean_text)
        except RuntimeError as error:
            print(f"Windows SAPI5 voice output error: {error}")
            try:
                self.engine.say(clean_text)
                self.engine.runAndWait()
            except RuntimeError as fallback_error:
                print(f"pyttsx3 voice output error: {fallback_error}")

    @staticmethod
    def _speak_with_windows_sapi(text: str) -> None:
        escaped_text = text.replace("'", "''")
        command = (
            "Add-Type -AssemblyName System.Speech; "
            "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$speaker.Volume = 100; "
            "$speaker.Rate = 0; "
            f"$speaker.Speak('{escaped_text}'); "
            "$speaker.Dispose()"
        )
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            raise RuntimeError("Windows SAPI5 could not speak the response.") from error

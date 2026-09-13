"""Whitelist-only computer commands for ASHU."""

from __future__ import annotations

import re
import subprocess
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote_plus


@dataclass(frozen=True)
class CommandResult:
    handled: bool = False
    should_exit: bool = False
    response: str = ""


def remove_wake_word(text: str) -> str:
    lowered = text.casefold().strip()
    for wake_word in (
        "hey ashu",
        "hey ash",
        "ashu",
        "अशु",
        "आशु",
        "हे आशु",
        "हे एशू",
    ):
        if lowered.startswith(wake_word):
            return text[len(wake_word) :].strip(" ,.!?")
    return text.strip()


def _open_url(url: str, message: str) -> CommandResult:
    try:
        webbrowser.open(url)
        return CommandResult(handled=True, response=message)
    except OSError:
        return CommandResult(handled=True, response="I could not open that on this computer.")


def _open_program(command: list[str], message: str) -> CommandResult:
    try:
        subprocess.Popen(command)
        return CommandResult(handled=True, response=message)
    except (FileNotFoundError, OSError):
        return CommandResult(handled=True, response="That application is not available in PATH.")


def _is_open_request(text: str, *targets: str) -> bool:
    """Recognize natural open requests without executing arbitrary text."""
    open_words = (
        "open",
        "launch",
        "खोल",
        "खोलो",
        "खोलना",
        "khol",
        "kholna",
    )
    return any(target in text for target in targets) and any(
        word in text for word in open_words
    )


def execute_command(text: str) -> CommandResult:
    """Execute only known, safe commands and return the spoken response."""
    normalized = re.sub(r"\s+", " ", text.casefold()).strip()

    if normalized in {
        "who are you",
        "what is your name",
        "tum kaun ho",
        "tumhara naam kya hai",
        "आप कौन हो",
        "तुम्हारा नाम क्या है",
    }:
        return CommandResult(
            handled=True,
            response="I am Ashu, your personal AI assistant. I am ready to help, Ayush.",
        )

    if normalized in {"hello ashu", "hi ashu", "hello", "hi", "नमस्ते", "हैलो"}:
        return CommandResult(handled=True, response="Hello Ayush. Ashu is online and ready.")

    if normalized in {"are you there", "status", "ashu status", "क्या तुम सुन रहे हो"}:
        return CommandResult(handled=True, response="All systems are ready. I am listening, Ayush.")

    if normalized in {"exit", "quit", "stop ashu", "exit ashu", "goodbye", "bye"}:
        return CommandResult(handled=True, should_exit=True, response="Goodbye Ayush.")

    if normalized in {"stop listening", "pause listening", "bas", "रुक जाओ"}:
        return CommandResult(handled=True, should_exit=True, response="Okay, I will stop listening.")

    if normalized in {"what time is it", "tell me the time", "current time", "समय बताओ"}:
        current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
        return CommandResult(handled=True, response=f"The current time is {current_time}.")

    if normalized in {"what is today's date", "tell me today's date", "today's date", "आज की तारीख"}:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return CommandResult(handled=True, response=f"Today is {today}.")

    if _is_open_request(normalized, "youtube", "यूट्यूब", "यूटुब", "यूट्यूब"):
        return _open_url("https://www.youtube.com", "Opening YouTube.")

    if _is_open_request(normalized, "google", "गूगल"):
        return _open_url("https://www.google.com", "Opening Google.")

    if _is_open_request(normalized, "chrome", "क्रोम"):
        return _open_program(["chrome.exe"], "Opening Chrome.")

    if _is_open_request(normalized, "notepad", "नोटपैड"):
        return _open_program(["notepad.exe"], "Opening Notepad.")

    if _is_open_request(normalized, "calculator", "कैलकुलेटर"):
        return _open_program(["calc.exe"], "Opening Calculator.")

    if _is_open_request(normalized, "vs code", "vscode", "वीएस कोड"):
        return _open_program(["code"], "Opening Visual Studio Code.")

    search_match = re.match(r"(?:search (?:the web )?for|google search|वेब पर खोजो)\s+(.+)", text, re.IGNORECASE)
    if search_match:
        query = search_match.group(1).strip()
        return _open_url(
            f"https://www.google.com/search?q={quote_plus(query)}",
            f"Searching the web for {query}.",
        )

    return CommandResult()

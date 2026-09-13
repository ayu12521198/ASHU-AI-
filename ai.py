from __future__ import annotations

import shutil
import subprocess
import time
from typing import Any

import requests

from config import (
    ASSISTANT_NAME,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_REQUEST_TIMEOUT,
    OLLAMA_START_TIMEOUT,
    USER_NAME,
)

SYSTEM_PROMPT = (
    f"Your name is {ASSISTANT_NAME}, a capable personal AI assistant for {USER_NAME}. "
    "You have the calm, attentive, fast and helpful manner of a futuristic computer assistant. "
    "Act like a polished personal computer companion: acknowledge requests briefly, think clearly, "
    "and offer the next useful action when appropriate. "
    "You are an original assistant and must never claim to be another character. "
    "Understand Hindi, Hinglish, and English. Reply naturally in the same language as the user. "
    "Address the user as Ayush when it feels natural. Be concise for voice conversations, "
    "but give useful steps when the user asks how to do something. "
    "Do not use markdown, bullet points, emojis, or symbols that are awkward to hear aloud. "
    "Remember details from this conversation. If you do not know something, say so clearly "
    "instead of inventing an answer."
)

conversation: list[dict[str, str]] = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def _get_tags() -> dict[str, Any] | None:
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def ensure_ollama() -> None:
    """Ensure Ollama is running and the configured model is installed."""
    if _get_tags() is None:
        ollama_path = shutil.which("ollama")
        if not ollama_path:
            raise RuntimeError(
                "Ollama is not installed or is not available in PATH. "
                "Install it from https://ollama.com/download/windows."
            )

        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen(
            [ollama_path, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )

        deadline = time.monotonic() + OLLAMA_START_TIMEOUT
        while time.monotonic() < deadline:
            if _get_tags() is not None:
                break
            time.sleep(0.5)
        else:
            raise RuntimeError(
                "Ollama could not be started. Please run 'ollama serve' once "
                "and try again."
            )

    tags = _get_tags() or {}
    model_names = {item.get("name", "") for item in tags.get("models", [])}
    model_available = any(
        name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}:")
        for name in model_names
    )
    if not model_available:
        ollama_path = shutil.which("ollama")
        if not ollama_path:
            raise RuntimeError("The Ollama command was not found while installing the model.")
        result = subprocess.run(
            [ollama_path, "pull", OLLAMA_MODEL],
            check=False,
            timeout=900,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Ollama model '{OLLAMA_MODEL}' is missing and could not be downloaded."
            )


def reset_memory() -> None:
    conversation[:] = [{"role": "system", "content": SYSTEM_PROMPT}]


def ask_ashu(question: str) -> str:
    """Ask Ollama a question while retaining current-session context."""
    conversation.append({"role": "user", "content": question})
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": conversation,
                "stream": False,
            },
            timeout=OLLAMA_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        message = response.json().get("message", {})
        answer = str(message.get("content", "")).strip()
        if not answer:
            raise RuntimeError("Ollama returned an empty response.")
        conversation.append({"role": "assistant", "content": answer})
        return answer
    except (requests.RequestException, ValueError, KeyError) as error:
        conversation.pop()
        raise RuntimeError(
            "I could not reach Ollama. Please check that Ollama is running."
        ) from error

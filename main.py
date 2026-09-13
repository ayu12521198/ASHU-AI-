from ai import ask_ashu, ensure_ollama
from commands import execute_command, remove_wake_word
from config import ASSISTANT_NAME, USER_NAME
from voice_input import VoiceInput
from voice_output import VoiceOutput


def main():
    try:
        print(f"Starting {ASSISTANT_NAME}...")
        ensure_ollama()
    except Exception as error:
        print(f"Startup error: {error}")
        return

    try:
        voice_output = VoiceOutput()
        voice_input = VoiceInput()
    except Exception as error:
        print(f"Voice setup error: {error}")
        print("Check that a microphone is connected and Windows speech support is available.")
        return

    voice_output.speak(
        f"Hello {USER_NAME}, I am {ASSISTANT_NAME}. How can I help you?"
    )

    while True:
        try:
            question = voice_input.listen()
            if not question:
                continue
            print(f"👤 You: {question}")

            question = remove_wake_word(question)
            if not question:
                voice_output.speak("Yes Ayush, I am listening.")
                continue

            command = execute_command(question)
            if command.handled:
                if command.response:
                    voice_output.speak(command.response)
                if command.should_exit:
                    break
                continue

            answer = ask_ashu(question)
            voice_output.speak(answer)
        except KeyboardInterrupt:
            print("\nStopping ASHU.")
            break
        except Exception as error:
            print(f"Assistant error: {error}")
            voice_output.speak("I had a temporary problem. Please try again.")


if __name__ == "__main__":
    main()

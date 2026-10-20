"""A small terminal chatbot powered by the Anthropic API.

Features: streaming replies, conversation memory, a configurable persona,
and transcript saving. Run it with:  python chat.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = 1024
TRANSCRIPT_DIR = Path("transcripts")

DEFAULT_SYSTEM_PROMPT = (
    "You are a friendly, patient mentor helping a beginner learn AI engineering. "
    "Explain ideas simply, use short examples, and ask a follow-up question "
    "when it would help the learner go deeper."
)

HELP_TEXT = """Commands:
  /help    show this message
  /reset   clear the conversation and start fresh
  /save    save the conversation to the transcripts/ folder
  /quit    exit (you will be asked whether to save)
"""


def save_transcript(messages: list[dict]) -> Path | None:
    """Write the conversation to a timestamped JSON file."""
    if not messages:
        print("Nothing to save yet.")
        return None
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = TRANSCRIPT_DIR / f"chat-{stamp}.json"
    path.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved to {path}")
    return path


def stream_reply(client: anthropic.Anthropic, messages: list[dict], system: str) -> str:
    """Send the conversation to the model and print the reply as it streams in."""
    reply = ""
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            reply += text
    print()
    return reply


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    client = anthropic.Anthropic()
    system = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
    messages: list[dict] = []

    print(f"Chatting with {MODEL}. Type /help for commands.\n")

    while True:
        try:
            user_input = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            command = user_input.lower()
            if command == "/help":
                print(HELP_TEXT)
            elif command == "/reset":
                messages.clear()
                print("Conversation cleared.\n")
            elif command == "/save":
                save_transcript(messages)
            elif command in ("/quit", "/exit"):
                break
            else:
                print("Unknown command. Type /help.\n")
            continue

        messages.append({"role": "user", "content": user_input})
        print("bot > ", end="", flush=True)

        try:
            reply = stream_reply(client, messages, system)
        except anthropic.APIError as err:
            # Remove the failed turn so the history stays valid, then carry on.
            messages.pop()
            print(f"\n[API error: {err}]\n")
            continue

        messages.append({"role": "assistant", "content": reply})
        print()

    if messages and input("Save this conversation? [y/N] ").strip().lower() == "y":
        save_transcript(messages)
    print("Goodbye!")


if __name__ == "__main__":
    main()
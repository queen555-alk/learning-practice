"""evalkit: a tiny prompt-evaluation harness for LLM apps.

Define test cases (prompt + expected substring), run them against any
model function, and get a pass rate. Stdlib only. Runs offline with the
built-in mock model; set USE_CLAUDE=1 to use the Anthropic API instead.
"""
import os
from dataclasses import dataclass


@dataclass
class Case:
    prompt: str
    expect: str  # substring that must appear in the answer (case-insensitive)


CASES = [
    Case("What is the capital of France? Answer in one word.", "paris"),
    Case("What is 2 + 2? Answer with just the number.", "4"),
    Case("Name the primary colour of the sky on a clear day.", "blue"),
]


def mock_model(prompt: str) -> str:
    """Offline stand-in so the harness runs without an API key."""
    answers = {"france": "Paris", "2 + 2": "4", "sky": "Blue"}
    for key, value in answers.items():
        if key in prompt.lower():
            return value
    return "I don't know"


def claude_model(prompt: str) -> str:
    """Real model adapter. Needs `pip install anthropic` and ANTHROPIC_API_KEY."""
    import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


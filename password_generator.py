"""Simple command-line password generator."""

import argparse
import secrets
import string


def generate_password(length=16, use_digits=True, use_symbols=True):
    """Return a random password of the given length."""
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    return "".join(secrets.choice(characters) for _ in range(length))


    
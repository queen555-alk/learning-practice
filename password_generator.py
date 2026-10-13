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


def main():
    parser = argparse.ArgumentParser(description="Generate a random password.")
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="password length (default: 16)")
    parser.add_argument("--no-digits", action="store_true",
                        help="exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                        help="exclude symbols")
    args = parser.parse_args()

    if args.length < 4:
        parser.error("length must be at least 4")

    print(generate_password(args.length,
                            use_digits=not args.no_digits,
                            use_symbols=not args.no_symbols))


if __name__ == "__main__":
    main()

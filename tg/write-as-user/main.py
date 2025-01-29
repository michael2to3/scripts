#!/usr/bin/env python3
"""
send_telegram_user_message.py

A Python script to send a message as a Telegram user (not a bot) using Telethon.

Usage:
    python send_telegram_user_message.py \
        --api-id 123456 \
        --api-hash abcdef1234567890abcdef1234567890 \
        --phone-number +1234567890 \
        --to @example_username \
        --message "Hello from Telethon!"

Arguments:
    --api-id           Your Telegram API ID (from my.telegram.org)
    --api-hash         Your Telegram API Hash (from my.telegram.org)
    --phone-number     Your Telegram account phone number in international format
    --to               Recipient (username, phone number, user ID, channel/group ID, etc.)
    --message          The message text to send

Exit Codes:
    0 - Success
    1 - Invalid or missing arguments
    2 - Connection or authorization error
    3 - Error sending the message
"""

import argparse
import sys

from telethon import TelegramClient, errors


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Send a Telegram message as a user using Telethon."
    )
    parser.add_argument(
        "--api-id",
        required=True,
        help="Telegram API ID (from my.telegram.org)."
    )
    parser.add_argument(
        "--api-hash",
        required=True,
        help="Telegram API Hash (from my.telegram.org)."
    )
    parser.add_argument(
        "--phone-number",
        required=True,
        help="Telegram phone number in international format (e.g. +1234567890)."
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient (username, phone, user ID, channel/group ID, etc.)."
    )
    parser.add_argument(
        "--message",
        required=True,
        help="Message text to send."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    session_name = f"session_{args.phone_number.replace('+', '')}"

    client = TelegramClient(session_name, int(args.api_id), args.api_hash)

    try:
        client.start(phone=args.phone_number)
    except errors.PhoneNumberInvalidError:
        print("Error: Invalid phone number format.")
        sys.exit(2)
    except Exception as e:
        print(f"Error during connection/authorization: {e}")
        sys.exit(2)

    try:
        client.loop.run_until_complete(
            client.send_message(args.to, args.message)
        )
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error while sending message: {e}")
        sys.exit(3)
    finally:
        client.disconnect()

    sys.exit(0)

if __name__ == "__main__":
    main()

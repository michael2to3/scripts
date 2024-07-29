#!/usr/bin/env python3.12
import asyncio
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
bot_username = os.getenv("BOT_USERNAME")
user_id = int(os.getenv("USER_ID"))
wordlist = open("./wordlist.txt").read().split("\n")


client = TelegramClient("session_name", api_id, api_hash)

results = []


@client.on(events.NewMessage(from_users=user_id))
async def handler(event):
    global results, current_word, start_time
    response_time = datetime.now() - start_time
    results.append(
        {
            "request": current_word,
            "response": event.message.message,
            "response_length": len(event.message.message),
            "response_type": "message",
            "response_time": response_time.total_seconds(),
        }
    )
    print(f"Received response for word: {event.message.message}")


async def main():
    await client.start(phone_number)
    print("Client Created")

    global current_word, start_time
    try:
        for word in wordlist:
            current_word = word
            start_time = datetime.now()
            print(f"Sending word: {word}")
            try:
                await client.send_message(bot_username, word)
            except ValueError as e:
                print(f"Failed to send message: {e}")
                continue

            await asyncio.sleep(0.5)

            if not any(result["request"] == word for result in results):
                response_time = datetime.now() - start_time
                results.append(
                    {
                        "request": word,
                        "response": None,
                        "response_length": None,
                        "response_type": "timeout",
                        "response_time": response_time.total_seconds(),
                    }
                )
                print(f"Timeout for word: {word}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        with open("./fuzzing.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print("Fuzzing complete and results saved to fuzzing.json")


if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        with open("./fuzzing.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print("Fuzzing complete and results saved to fuzzing.json")

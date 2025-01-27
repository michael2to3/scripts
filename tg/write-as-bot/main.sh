#!/usr/bin/env bash

while [[ $# -gt 0 ]]; do
    case "$1" in
    --token)
        BOT_TOKEN="$2"
        shift 2
        ;;
    --chat-id)
        CHAT_ID="$2"
        shift 2
        ;;
    --message)
        MESSAGE="$2"
        shift 2
        ;;
    *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" || -z "$MESSAGE" ]]; then
    echo "Usage: $0 --token <TOKEN> --chat-id <CHAT_ID> --message <MESSAGE>"
    exit 1
fi

API_URL="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

RESPONSE=$(curl -s -X POST "$API_URL" \
    -d chat_id="$CHAT_ID" \
    --data-urlencode text="$MESSAGE")

if [[ "$RESPONSE" == *'"ok":true'* ]]; then
    echo "Message sent successfully to chat ${CHAT_ID}."
else
    echo "Failed to send message. Response from Telegram API:"
    echo "$RESPONSE"
    exit 1
fi

import requests
import os

webhook_url = os.environ["DISCORD_WEBHOOK"]

message = {
    "content": "✅今天系統運作正常，時間是 XXX"
}

response = requests.post(webhook_url, json=message)

print("Discord notification sent.")

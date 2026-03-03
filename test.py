import requests
import os

webhook_url = os.environ["DISCORD_WEBHOOK"]

message = {
    "content": "✅ RAM Monitor 雲端測試成功！"
}

response = requests.post(webhook_url, json=message)

print("Discord notification sent.")

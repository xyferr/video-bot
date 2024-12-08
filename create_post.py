import aiohttp
import os

FLIC_TOKEN = os.environ.get("FLIC_TOKEN")

async def create_post(session, title, video_hash, category_id=25):
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    data = {
        "title": "Motivation",
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    async with session.post("https://api.socialverseapp.com/posts", json=data, headers=headers) as response:
        if response.status == 200:
            print("Post created successfully!")
        else:
            print("Failed to create post")

import aiohttp
import os

FLIC_TOKEN = os.environ.get("FLIC_TOKEN")

async def get_upload_url(session):
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    async with session.get("https://api.socialverseapp.com/posts/generate-upload-url", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            print("Failed to fetch upload URL")
            return None


async def upload_video(session, file_path, upload_url):
    with open(file_path, "rb") as file:
        async with session.put(upload_url, data=file) as response:
            if response.status == 200:
                print(f"Uploaded: {file_path}")
                return True
            else:
                print(f"Failed to upload: {file_path}")
                return False

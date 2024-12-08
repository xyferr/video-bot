import aiohttp
import os
import tqdm

FLIC_TOKEN = os.getenv("FLIC_TOKEN")

async def get_upload_url(session):
    """Fetches a pre-signed upload URL."""
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    async with session.get("https://api.socialverseapp.com/posts/generate-upload-url", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to fetch upload URL: {response.status}")
            return None


async def upload_video(session, file_path, upload_url):
    """Uploads the video to the server."""
    file_size = os.path.getsize(file_path)
    headers = {"Content-Type": "application/octet-stream"}

    with open(file_path, "rb") as file:
        with tqdm.tqdm(
            total=file_size, unit="B", unit_scale=True, desc=f"Uploading {file_path}"
        ) as pbar:
            chunk = file.read(1024)
            while chunk:
                pbar.update(len(chunk))
                chunk = file.read(1024)

            file.seek(0)  # Reset file pointer to the beginning for aiohttp
            async with session.put(upload_url, data=file, headers=headers) as response:
                if response.status == 200:
                    print(f"Upload successful: {file_path}")
                    return True
                else:
                    print(f"Upload failed: {response.status}")
                    return False

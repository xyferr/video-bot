import asyncio
import aiohttp
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm

FLIC_TOKEN=os.environ.get("FLIC_TOKEN")
UPLOAD_URL_API = "https://api.socialverseapp.com/posts/generate-upload-url"
CREATE_POST_API = "https://api.socialverseapp.com/posts"


class DirectoryMonitor(FileSystemEventHandler):
    def __init__(self, upload_func):
        self.upload_func = upload_func

    def on_created(self, event):
        if event.src_path.endswith(".mp4"):
            print(f"New file detected: {event.src_path}")
            asyncio.run(self.upload_func(event.src_path))


async def get_upload_url(session):
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    async with session.get(UPLOAD_URL_API, headers=headers) as response:
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


async def create_post(session, title, video_hash, category_id=1):
    headers = {"Flic-Token": FLIC_TOKEN, "Content-Type": "application/json"}
    data = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    async with session.post(CREATE_POST_API, json=data, headers=headers) as response:
        if response.status == 200:
            print("Post created successfully!")
        else:
            print("Failed to create post")


async def upload_process(file_path):
    async with aiohttp.ClientSession() as session:
        upload_data = await get_upload_url(session)
        if upload_data:
            upload_url = upload_data["url"]
            video_hash = upload_data["hash"]
            if await upload_video(session, file_path, upload_url):
                await create_post(session, os.path.basename(file_path), video_hash)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


def main():
    path_to_watch = "videos"
    monitor = DirectoryMonitor(upload_process)
    observer = Observer()
    observer.schedule(monitor, path_to_watch, recursive=False)
    observer.start()

    print("Monitoring directory...")
    try:
        while True:
            asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()

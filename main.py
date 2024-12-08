import aiohttp
import asyncio
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from upload import get_upload_url, upload_video
from create_post import create_post

async def upload_process(file_path):
    """Handles the upload process for a new video file."""
    async with aiohttp.ClientSession() as session:
        upload_data = await get_upload_url(session)
        if upload_data:
            upload_url = upload_data["url"]
            video_hash = upload_data["hash"]
            success = await upload_video(session , file_path, upload_url)
            if success:
                await create_post(session, os.path.basename(file_path), video_hash)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        else:
            print("Failed to get upload URL")

class DirectoryMonitor(FileSystemEventHandler):
    """Monitors directory for new files and triggers upload."""
    def __init__(self, upload_func):
        self.upload_func = upload_func

    def on_created(self, event):
        if event.src_path.endswith(".mp4"):
            print(f"New file detected: {event.src_path}")
            asyncio.run(self.upload_func(event.src_path))

def main():
    path_to_watch = "videos"
    if not os.path.exists(path_to_watch):
        os.makedirs(path_to_watch)

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

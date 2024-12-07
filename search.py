from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

def setup_driver():
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

def search_videos(keyword, driver):
    try:
        """Search videos on Instagram with a given keyword."""
        base_url = f"https://www.instagram.com/explore/tags/{keyword}/"
        driver.get(base_url)
        time.sleep(3)

        # Find video posts
        video_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/reel/')]")
        video_links = [el.get_attribute("href") for el in video_elements[:5]]  # Limit to 5 videos for simplicity
        print(video_links)
        return video_links
    except Exception as e:
        print(f"An error occurred: {e}")

def download_video(video_url):
    try:
        # Implement the logic to download the video from the video_url
        print(f"Downloading video from: {video_url}")
        # Use requests or another library to download the video
        response = requests.get(video_url)
        if response.status_code == 200:
            video_file = f"{os.path.basename(video_url)}.mp4"
            with open(video_file, "wb") as file:
                file.write(response.content)
            print(f"Video downloaded: {video_file}")
        else:
            print("Failed to download video")
        
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")

def instagram_login(driver, username, password):
    """Log in to Instagram using Selenium."""
    if username is None or password is None:
        raise ValueError("Username and password must not be None")

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(5)  # Wait for login to complete

def fetch_instagram_videos_with_login(keyword, username, password):
    if username is None or password is None:
        raise ValueError("Username and password must not be None")

    driver = setup_driver()
    try:
        instagram_login(driver, username, password)
        video_links = search_videos(keyword, driver)
        for video_url in video_links:
            download_video(video_url)
    finally:
        driver.quit()

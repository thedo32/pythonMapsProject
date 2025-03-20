from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os



# Configuration
MAP_URL = "https://www.google.com/maps/@-0.3935379,100.4571598,15z"  # Replace with desired location
SCREENSHOT_PATH = "screenshots/"
OUTPUT_IMAGE = "stitched_map.png"
GRID_SIZE = (3, 3)  # Number of rows and columns for screenshots

# Setup ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening browser
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-gpu")

service = Service("chromedriver")  # Update path if necessary
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create folder for screenshots
if not os.path.exists(SCREENSHOT_PATH):
    os.makedirs(SCREENSHOT_PATH)

# Open Google Maps
driver.get(MAP_URL)
time.sleep(5)  # Wait for map to load

# Function to capture screenshots
def capture_screenshots():
    images = []
    for row in range(GRID_SIZE[0]):
        for col in range(GRID_SIZE[1]):
            file_name = f"{SCREENSHOT_PATH}map_{row}_{col}.png"
            driver.save_screenshot(file_name)
            images.append(file_name)
            driver.execute_script(f"window.scrollBy({col * 400}, {row * 400})")
            time.sleep(2)  # Allow scrolling effect
    return images

# Capture grid of images
screenshot_files = capture_screenshots()
driver.quit()

# Function to stitch images together
def stitch_images(files):
    imgs = [Image.open(f) for f in files]
    width, height = imgs[0].size
    stitched_img = Image.new("RGB", (width * GRID_SIZE[1], height * GRID_SIZE[0]))

    for index, img in enumerate(imgs):
        row = index // GRID_SIZE[1]
        col = index % GRID_SIZE[1]
        stitched_img.paste(img, (col * width, row * height))

    stitched_img.save(OUTPUT_IMAGE)
    print(f"High-resolution map saved as {OUTPUT_IMAGE}")

# Stitch images together
stitch_images(screenshot_files)

import os
import requests
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

# Get website URL
url = input("Enter the website URL: ").strip()
if not url:
    print("❌ Error: No URL provided. Exiting.")
    exit(1)

# Create output directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"website_clone_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def download_file(file_url, folder):
    """Download a file and return the local filename"""
    parsed_url = urlparse(file_url)
    filename = os.path.basename(parsed_url.path) or "unknown_file"
    folder_path = os.path.join(output_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        print(f"Skipping (exists): {file_url}")
        return os.path.join(folder, filename)
    
    try:
        file_response = requests.get(file_url, headers=headers, timeout=10)
        file_response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(file_response.content)
        print(f"Downloaded: {file_url} -> {file_path}")
        return os.path.join(folder, filename)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_url}: {e}")
        return None

# Use Playwright to render the page dynamically
def get_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="networkidle")
        time.sleep(3)  # Allow time for JS to execute
        html = page.content()
        browser.close()
    return html

html_content = get_rendered_html(url)
soup = BeautifulSoup(html_content, "html.parser")

# Download CSS
for link in soup.find_all("link", {"rel": "stylesheet"}):
    if link.get("href"):
        css_url = urljoin(url, link["href"])
        local_css_path = download_file(css_url, "css")
        if local_css_path:
            link["href"] = local_css_path

# Download images
for img in soup.find_all("img"):
    if img.get("src"):
        img_url = urljoin(url, img["src"])
        local_img_path = download_file(img_url, "images")
        if local_img_path:
            img["src"] = local_img_path

# Download JavaScript
for script in soup.find_all("script", src=True):
    js_url = urljoin(url, script["src"])
    local_js_path = download_file(js_url, "js")
    if local_js_path:
        script["src"] = local_js_path

# Save modified HTML file
html_filename = f"index_{timestamp}.html"
html_path = os.path.join(output_dir, html_filename)
with open(html_path, "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print(f"✅ Website clone saved successfully in '{output_dir}'! Open '{html_filename}' in your browser.")

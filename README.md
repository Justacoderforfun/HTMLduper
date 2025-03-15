# Website Cloner

This is a basic website cloning script that downloads a webpage, including dynamically loaded content, using Playwright and BeautifulSoup. It attempts to save the HTML, CSS, images, and JavaScript files locally.

## Features
- Captures dynamically rendered content using Playwright.
- Downloads and saves images, CSS, and JavaScript files.
- Modifies the local HTML file to reference downloaded assets.

## Requirements
Ensure you have Python installed along with the necessary dependencies:

```sh
pip install requests playwright beautifulsoup4
playwright install
```

## Usage
Run the script and enter the URL when prompted:

```sh
python website_cloner.py
```

The cloned website will be saved in a timestamped directory, with assets organized into `css/`, `images/`, and `js/` folders.

## Limitations
- This is a basic cloner and may not work on all websites.
- Some websites use anti-scraping techniques that may prevent cloning.
- Dynamically loaded content may not always be captured accurately.
- Some images or other resources may be missing from the cloned version.

## Disclaimer
Use this script responsibly. Cloning websites without permission may violate terms of service or copyright laws.

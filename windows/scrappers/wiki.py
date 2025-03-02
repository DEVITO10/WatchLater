from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import traceback

import config

def scrape_wikipedia(wiki_url):
    if not wiki_url:
        config.RESULT['wiki'] = {"error": "Wikipedia URL not found"}

    title = None
    image_url = None
    summary = None

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    bypass_csp=True,
                    user_agent="Mozilla/5.0"
                )
                page = context.new_page()

                try:
                    page.goto(wiki_url, timeout=60000)
                except PlaywrightTimeoutError:
                    config.RESULT['wiki'] = {"error": "Page load timeout exceeded (60 seconds)"}

                title = page.title().split(' - ')[0] if page.title() else "Title not found"

                try:
                    image_url = page.locator("td.infobox-image > span > a > img").get_attribute("src")
                    if not image_url:
                        raise ValueError("Image URL not found")
                except Exception as e:
                    image_url = None
                    print(f"Error extracting image URL: {e}")

                try:
                    summary = page.locator("p").first.inner_text() if title in page.locator("p").first.inner_text() else page.locator("p").nth(1).inner_text()
                    if not summary:
                        raise ValueError("Summary not found")
                except Exception as e:
                    summary = "Summary not available"
                    print(f"Error extracting summary: {e}")

                browser.close()

            except Exception as e:
                print(f"Playwright error: {e}")
                config.RESULT['wiki'] = {"error": f"Playwright error: {str(e)}"}

        image_path = None
        if image_url:
            try:
                response = requests.get('https:'+image_url, timeout=10)
                response.raise_for_status()

                image = Image.open(BytesIO(response.content))
                if image.mode == "P":
                    image = image.convert("RGB")

                image_path = "wiki_image.png"
                image.save(image_path, "PNG")
                print(f"Image downloaded and saved as '{image_path}'")

            except requests.RequestException as e:
                print(f"Image download failed: {e}")
                image_path = None
            except UnidentifiedImageError as e:
                print(f"Invalid image format: {e}")
                image_path = None

        config.RESULT['wiki'] = {
            "Title": title,
            "Image": image_url if image_path else "Image not available",
            "Summary": summary,
            "Link" : wiki_url
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        config.RESULT['wiki'] = {"error": f"Unexpected error: {str(e)}"}
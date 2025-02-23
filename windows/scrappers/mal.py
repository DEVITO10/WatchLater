from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import traceback

def scrape_myanimelist(anime_url):
    if not anime_url:
        return {"error": "MyAnimeList URL not found"}

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
                    page.goto(anime_url, timeout=60000)
                except PlaywrightTimeoutError:
                    return {"error": "Page load timeout exceeded (60 seconds)"}

                title = page.title().split(' - ')[0] if page.title() else "Title not found"

                try:
                    image_url = page.locator("img.lazyloaded").first.get_attribute("src")
                    if not image_url:
                        raise ValueError("Image URL not found")
                except Exception as e:
                    image_url = None
                    print(f"Error extracting image URL: {e}")

                try:
                    summary = page.locator("meta[property='og:description']").get_attribute("content")
                    if not summary:
                        raise ValueError("Summary not found")
                except Exception as e:
                    summary = "Summary not available"
                    print(f"Error extracting summary: {e}")

                browser.close()

            except Exception as e:
                print(f"Playwright error: {e}")
                return {"error": f"Playwright error: {str(e)}"}

        image_path = None
        if image_url:
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()

                image = Image.open(BytesIO(response.content))
                if image.mode == "P":
                    image = image.convert("RGB")

                image_path = "mal_image.png"
                image.save(image_path, "PNG")
                print(f"Image downloaded and saved as '{image_path}'")

            except requests.RequestException as e:
                print(f"Image download failed: {e}")
                image_path = None
            except UnidentifiedImageError as e:
                print(f"Invalid image format: {e}")
                image_path = None

        return {
            "Title": title,
            "Image": image_url if image_path else "Image not available",
            "Summary": summary,
            "Link" : anime_url
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return {"error": f"Unexpected error: {str(e)}"}
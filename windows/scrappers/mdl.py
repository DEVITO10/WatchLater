from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import traceback

def scrape_mydramalist(drama_url):
    if not drama_url:
        return {"error": "MyDramaList URL not provided"}

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    bypass_csp=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                stealth.stealth_sync(page)

                try:
                    page.goto(drama_url, timeout=60000)
                except PlaywrightTimeoutError:
                    return {"error": "Page load timeout exceeded (60 seconds)"}

                title = page.title().split(' - ')[0] if page.title() else "Title not found"

                try:
                    image_url = page.locator("img.img-responsive").nth(1).get_attribute("src")
                    if not image_url:
                        raise ValueError("Image URL not found")
                except Exception as e:
                    image_url = None
                    print(f"Error extracting image URL: {e}")

                try:
                    summary = page.locator("div.show-synopsis > p > span").inner_text()
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
                if image.mode == "P":  # Convert from Palette mode if necessary
                    image = image.convert("RGB")

                image_path = "mdl_image.png"
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
            "Image": image_path if image_path else "Image not available",
            "Summary": summary
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return {"error": f"Unexpected error: {str(e)}"}
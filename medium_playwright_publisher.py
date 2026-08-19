import asyncio
import os
from playwright.async_api import async_playwright

async def publish_to_medium_browser(email, password, title, content_markdown):
    """
    Automates publishing a draft / post on Medium using Playwright browser automation.
    """
    async with async_playwright() as p:
        # Launch browser (set headless=False if you want to watch it run live)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("[*] Navigating to Medium login...")
            await page.goto("https://medium.com/m/signin")
            
            # Note: Medium sign-in often uses Google / Email OTP. 
            # If using email link or Google SSO, pause here for manual completion or handle selectors.
            print("[*] Please complete login in the browser window if prompted...")
            await page.wait_for_url("https://medium.com/", timeout=60000)
            
            print("[*] Navigating to new story page...")
            await page.goto("https://medium.com/new-story")
            await page.wait_for_load_state("networkidle")
            
            # Type Title
            print("[*] Entering title...")
            await page.keyboard.type(title)
            await page.keyboard.press("Enter")
            
            # Type Content
            print("[*] Entering story content...")
            await page.keyboard.type(content_markdown)
            
            print("[+] Content entered successfully. Ready to publish!")
            # Uncomment below to auto-click publish if desired:
            # await page.click("button:has-text('Publish')")
            
        except Exception as e:
            print(f"[!] Playwright automation error: {e}")
        finally:
            # Keep browser open briefly or close
            await browser.close()

if __name__ == "__main__":
    print("Playwright Medium Automation script ready.")

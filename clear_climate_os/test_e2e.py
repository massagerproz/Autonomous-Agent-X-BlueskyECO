import pytest
from playwright.sync_api import sync_playwright, expect
import re
import subprocess
import time
import os

def test_streamlit_app_e2e():
    """
    End-to-end test to verify the Streamlit application workflow.
    """
    os.makedirs("verification/screenshots", exist_ok=True)
    os.makedirs("verification/videos", exist_ok=True)

    process = subprocess.Popen(
        ["streamlit", "run", "clear_climate_os/app.py", "--server.port", "8502", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(record_video_dir="verification/videos/", viewport={'width': 1280, 'height': 800})
            page = context.new_page()

            page.goto("http://localhost:8502", timeout=15000)

            # Wait for main UI to load
            expect(page).to_have_title(re.compile("CLEAR Climate", re.IGNORECASE))

            # Step 1: Input text
            textarea = page.locator("textarea[aria-label='Paste meeting notes, activity updates, or stakeholder inputs here:']")
            textarea.fill("We installed 50 solar panels today. There was a delay due to weather. The stakeholder requested more info.")

            # Step 2: Process notes
            page.get_by_role("button", name="Process Notes").click()
            expect(page.get_by_text("Notes processed! See extracted evidence below.")).to_be_visible(timeout=10000)

            # Wait for Streamlit to render the form and checkboxes
            time.sleep(2)

            # Step 3: Approve evidence (check all checkboxes)
            checkboxes = page.get_by_role("checkbox").all()
            num_checkboxes = len(checkboxes)
            for checkbox in checkboxes:
                checkbox.scroll_into_view_if_needed()
                checkbox.locator("..").click(force=True)

            page.get_by_role("button", name="Save Approved Evidence to Tracker").scroll_into_view_if_needed()
            page.get_by_role("button", name="Save Approved Evidence to Tracker").click()

            # Use dynamic text matching based on number of extracted items
            success_message = re.compile(f"Saved {num_checkboxes} items to Evidence Tracker!", re.IGNORECASE)
            expect(page.get_by_text(success_message)).to_be_visible(timeout=10000)

            # Step 4: Generate Report
            page.get_by_role("button", name="Generate Donor Report Draft").scroll_into_view_if_needed()
            page.get_by_role("button", name="Generate Donor Report Draft").click()
            expect(page.get_by_text("QA Review Alerts")).to_be_visible(timeout=10000)

            # Verify RAG context was injected (use .first to bypass strict mode violation if multiple are rendered)
            expect(page.get_by_text(re.compile("Historical Context")).first).to_be_visible(timeout=10000)

            # Take final screenshot
            page.screenshot(path="verification/screenshots/playwright_screenshot.png", full_page=True)

            context.close()
            browser.close()
    finally:
        process.terminate()
        process.wait()

import pytest
from playwright.sync_api import sync_playwright, expect
import re
import subprocess
import time
import os

def test_streamlit_app_e2e_playwright():
    """
    End-to-end test to verify the Streamlit application loads successfully,
    using Playwright.
    """
    process = subprocess.Popen(
        ["streamlit", "run", "clear_climate_os/app.py", "--server.port", "8502", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto("http://localhost:8502", timeout=15000)

            expect(page).to_have_title(re.compile("CLEAR Climate", re.IGNORECASE))
            expect(page.locator("h1").filter(has_text="CLEAR Climate Copilot")).to_be_visible(timeout=15000)

            context.close()
            browser.close()
    finally:
        process.terminate()
        process.wait()

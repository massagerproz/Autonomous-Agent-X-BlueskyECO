import pytest
from playwright.sync_api import Page, expect
import re
import subprocess
import time

@pytest.fixture(scope="module", autouse=True)
def start_streamlit():
    # Start Streamlit server in the background
    process = subprocess.Popen(
        ["streamlit", "run", "clear_climate_os/app.py", "--server.port", "8502", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Wait for the server to start
    time.sleep(3)
    yield
    # Terminate the server after tests
    process.terminate()
    process.wait()

def test_streamlit_app_loads(page: Page):
    """
    End-to-end test to verify the Streamlit application loads successfully.
    Requires the Streamlit server to be running on localhost:8502.
    """
    page.goto("http://localhost:8502", timeout=10000)

    # Check that the title is correct
    expect(page).to_have_title(re.compile("CLEAR Climate", re.IGNORECASE))

    # Wait for the main header to appear indicating app loaded
    expect(page.locator("h1").filter(has_text="CLEAR Climate Copilot")).to_be_visible(timeout=10000)

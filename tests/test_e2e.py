import threading
import time
import pytest
import uvicorn
from playwright.sync_api import sync_playwright
from main import app

@pytest.fixture(scope="session", autouse=True)
def run_server():
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(1.5)
    yield

def test_calculator_web_e2e():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")
        assert "FastAPI Calculator" in page.title()

        page.fill("#num1", "25")
        page.fill("#num2", "15")
        page.select_option("#operation", "add")
        page.click("#calc-btn")

        page.wait_for_selector("#result:has-text('Result: 40')")
        assert "Result: 40" in page.inner_text("#result")
        browser.close()

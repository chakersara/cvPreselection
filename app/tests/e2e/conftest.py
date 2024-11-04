# tests/e2e/conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """
    Fixture to initialize and quit the Selenium WebDriver.
    Runs once per test module.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Optional: Uncomment the next line to run in headless mode
    # chrome_options.add_argument("--headless")

    # Enable logging for JavaScript errors
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # Initialize WebDriver without 'desired_capabilities'
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()

@pytest.fixture(scope="module")
def app_base_url():
    """
    Fixture to provide the base URL of the Flask application.
    """
    return "http://localhost:7008"

@pytest.fixture(scope="module")
def test_user_credentials():
    """
    Fixture to provide test user credentials.
    Replace with actual test user details.
    """
    return {
        "email": "test2@gmail.com",
        "password": "sarratest"
    }

@pytest.fixture(scope="module")
def login(driver, app_base_url, test_user_credentials):
    """
    Fixture to log in the test user before running tests.
    """
    # Navigate to the Login Page
    login_url = f"{app_base_url}/admin/login/"
    driver.get(login_url)

    # Locate email and password fields
    try:
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
    except Exception as e:
        pytest.fail(f"Login form fields not found: {e}")

    # Enter credentials
    email_input.send_keys(test_user_credentials["email"])
    password_input.send_keys(test_user_credentials["password"])

    # Locate and click the login button
    try:
        login_button = driver.find_element(By.ID, "submit")  # Using ID for precise selection
        driver.execute_script("arguments[0].style.border='3px solid red'", login_button)
        login_button.click()
    except Exception as e:
        pytest.fail(f"Login button not found: {e}")

    # Wait until login is successful, e.g., sidebar is visible
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "sidebar"))  # Adjust selector based on your sidebar ID
        )
        print("Sidebar is visible.")
    except Exception as e:
        pytest.fail(f"Login failed or sidebar not loaded: {e}")

    try:
        profile_name = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "profile-name"))
        )
        print(f"Profile name found: '{profile_name.text}'")
        assert profile_name.text.strip() == "Test2", "Logged in user profile name does not match."
    except AssertionError as ae:
        driver.save_screenshot("profile_verification_failure.png")
        pytest.fail(f"User profile not found or incorrect: {ae}")
    except Exception as e:
        driver.save_screenshot("profile_verification_exception.png")
        pytest.fail(f"User profile element not found: {e}")

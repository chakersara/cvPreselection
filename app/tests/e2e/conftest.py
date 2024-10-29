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
    
    # Initialize WebDriver
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
        "username": "test2@gmail.com",  
        "password": "sarratest"      
    }

@pytest.fixture(scope="module")
def login(driver, app_base_url, test_user_credentials):
    """
    Fixture to log in the test user before running tests.
    Uses 'app_base_url' to avoid conflicts with pytest-base-url plugin.
    """
    # Navigate to the Login Page
    login_url = f"{app_base_url}/admin/login/" 
    driver.get(login_url)

    # Locate email and password fields
    try:
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
    except:
        pytest.fail("Login form fields not found")

    # Enter credentials
    email_input.send_keys(test_user_credentials["username"])
    password_input.send_keys(test_user_credentials["password"])

    # Locate and click the login button
    try:
        # Updated selector to locate the <input> element with type="submit"
        login_button = driver.find_element(By.ID, "submit")  # Using ID for precise selection
       
        driver.execute_script("arguments[0].style.border='3px solid red'", login_button)
        
        login_button.click()
    except:
        pytest.fail("Login button not found")

    # Wait until login is successful, e.g., dashboard is visible
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "dashboard"))  # Adjust selector based on your dashboard element
        )
    except:
        pytest.fail("Login failed or dashboard not loaded")

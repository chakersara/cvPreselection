# tests/e2e/test_resume_operations.py

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def highlight(element, driver, duration=0.5):
    """
    Highlights (blinks) a Selenium WebDriver element for visual debugging.
    """
    driver.execute_script("arguments[0].style.border='3px solid red'", element)
    import time
    time.sleep(duration)
    driver.execute_script("arguments[0].style.border=''", element)

@pytest.mark.usefixtures("login")
def test_upload_and_delete_resume(driver, app_base_url):
    """
    E2E test for uploading and deleting a resume within an authenticated session.
    """
    # Navigate to Resume Upload Page
    upload_url = f"{app_base_url}/resume/"  
    driver.get(upload_url)

    # Locate the file input element
    try:
        upload_input = driver.find_element(By.NAME, "files")  #
        highlight(upload_input, driver) 
    except:
        pytest.fail("File input field not found")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    resume_file_path = os.path.join(current_dir, '../test_resume.pdf')  

    # Verify that the resume file exists
    assert os.path.exists(resume_file_path), f"Test resume file not found at {resume_file_path}"

    # Upload the resume
    upload_input.send_keys(resume_file_path)
    highlight(upload_input, driver)  # Highlight after uploading

    # Submit the upload form
    try:
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
        highlight(submit_button, driver)  # Highlight before clicking
        submit_button.click()
    except:
        pytest.fail("Submit button not found")

    # Wait for success message
    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))  # Adjust selector based on your application
        )
        assert "uploaded successfully" in success_message.text.lower(), "Upload success message not found or incorrect"
    except:
        pytest.fail("Upload success message not found")

    # Verify the resume appears in the list
    try:
        resume_card = driver.find_element(By.XPATH, "//div[@class='card' and contains(text(), 'test_resume.pdf')]")
        highlight(resume_card, driver)  # Highlight the resume card
        assert resume_card is not None, "Uploaded resume card not found in the list"
    except:
        pytest.fail("Uploaded resume not found in the list")

   
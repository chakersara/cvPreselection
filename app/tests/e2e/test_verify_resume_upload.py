# tests/e2e/test_verify_resume_upload.py

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
def test_verify_resume_upload(driver, app_base_url):
    """
    E2E test to verify that an uploaded resume appears in the resume list.
    """
    # Navigate to the Resume Page via Sidebar
    try:
        # Locate the 'circualem vitae' link in the sidebar
        circualem_vitae_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/resume/') and contains(., 'circualem vitae')]"))
        )
        highlight(circualem_vitae_link, driver)
        circualem_vitae_link.click()
        print("Navigated to 'circualem vitae' page via sidebar.")
    except Exception as e:
        pytest.fail(f"Failed to navigate to 'circualem vitae' page: {e}")

    # Wait until the Resume List is visible
    try:
        # Since there's no element with id="resume_list", adjust the selector
        # For example, wait for the first resume card to be visible
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "card"))
        )
        print("Resume list is visible.")
    except Exception as e:
        driver.save_screenshot("resume_list_visibility_failure.png")
        pytest.fail(f"Resume list did not load properly: {e}")

    # Define the path to the test resume file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Correct the path to point to tests/test_resume2.pdf
    resume_file_path = os.path.abspath(os.path.join(current_dir, '../test_resume2.pdf'))
    resume_filename = os.path.basename(resume_file_path)

    # Verify the uploaded resume appears in the list
    try:
        # Define a unique identifier for the resume, such as the image source
        resume_image_src = "/static/resumes/img/test_resume2.jpeg"

        # Wait until the resume card with the specific image appears
        resume_image = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//img[@src='{resume_image_src}']")
            )
        )
        highlight(resume_image, driver)
        assert resume_image is not None, "Uploaded resume image not found in the list."
        print("Uploaded resume image is present in the resume list.")
    except Exception as e:
        driver.save_screenshot("verify_resume_upload_failure.png")
        pytest.fail(f"Uploaded resume not found in the list: {e}")

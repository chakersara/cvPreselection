# tests/e2e/test_upload_resume.py

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

@pytest.mark.run(order=1)
@pytest.mark.usefixtures("login")
def test_upload_resume(driver, app_base_url):
    """
    E2E test for uploading a resume within an authenticated session.
    """
    # Navigate to the Resume Page via Sidebar
    try:
        # Locate the 'circualem vitae' link in the sidebar
        circualem_vitae_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '/resume/') and contains(., 'circualem vitae')]")
            )
        )
        highlight(circualem_vitae_link, driver)
        circualem_vitae_link.click()
        print("Navigated to 'circualem vitae' page via sidebar.")
    except Exception as e:
        pytest.fail(f"Failed to navigate to 'circualem vitae' page: {e}")

    # Wait until the 'Ajouter cv(s)' button is visible and clickable
    try:
        add_cv_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Ajouter cv(s)')]")
            )
        )
        highlight(add_cv_button, driver)
        add_cv_button.click()
        print("Clicked on 'Ajouter cv(s)' button to open the resume upload form.")

    except Exception as e:
        pytest.fail(f"'Ajouter cv(s)' button not found or not clickable: {e}")

    # Wait until the Resume Upload Form is visible
    try:
        resume_form = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "add_me_res"))
        )
        print("Resume upload form is visible.")
        highlight(resume_form, driver)
    except Exception as e:
        driver.save_screenshot("resume_upload_form_failure.png")
        pytest.fail(f"Resume upload form did not become visible: {e}")

    # Locate the file input element
    try:
        upload_input = resume_form.find_element(By.ID, "files")
        highlight(upload_input, driver)
        print("Located the file input element.")
    except Exception as e:
        driver.save_screenshot("file_input_failure.png")
        pytest.fail(f"File input field not found: {e}")

    # Define the path to the test resume file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Correct the path to point to tests/test_resume2.pdf
    resume_file_path = os.path.abspath(os.path.join(current_dir, '../test_resume2.pdf'))

    # Verify that the resume file exists
    print(f"Resolved resume file path: {resume_file_path}")
    assert os.path.exists(resume_file_path), f"Test resume file not found at {resume_file_path}"
    print(f"Uploading resume file from: {resume_file_path}")

    # Upload the resume
    try:
        upload_input.send_keys(resume_file_path)
        highlight(upload_input, driver)  # Highlight after uploading
        print("Resume file selected for upload.")
    except Exception as e:
        driver.save_screenshot("upload_resume_failure.png")
        pytest.fail(f"Failed to upload resume file: {e}")

    # Submit the upload form
    try:
        submit_button = resume_form.find_element(By.ID, "submit")
        highlight(submit_button, driver)  # Highlight before clicking
        submit_button.click()
        print("Clicked the submit button to upload the resume.")
    except Exception as e:
        driver.save_screenshot("submit_button_failure.png")
        pytest.fail(f"Submit button not found or could not be clicked: {e}")

    # Wait until the resume appears in the resume list using partial matching
    try:
        resume_image_partial_src = "test_resume2"

        # Wait until the resume card with the specific image appears
        resume_image = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//img[contains(@src, '{resume_image_partial_src}')]")
            )
        )
        highlight(resume_image, driver)
        assert resume_image is not None, "Uploaded resume image not found in the list."
        print("Resume uploaded successfully and found in the resume list.")
    except Exception as e:
        driver.save_screenshot("upload_success_failure.png")
        pytest.fail(f"Resume did not appear in the resume list after upload: {e}")

# tests/e2e/test_delete_resume.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.action_chains import ActionChains

def highlight(element, driver, duration=0.5):
    """
    Highlights (blinks) a Selenium WebDriver element for visual debugging.
    """
    driver.execute_script("arguments[0].style.border='3px solid red'", element)
    import time
    time.sleep(duration)
    driver.execute_script("arguments[0].style.border=''", element)

@pytest.mark.usefixtures("login")
@pytest.mark.run(order=3)  # Ensures this test runs last
def test_delete_resume(driver, app_base_url):
    """
    E2E test to delete a specific resume and verify its removal from the resume list.
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
        driver.save_screenshot("navigate_to_resume_page_failure.png")
        pytest.fail(f"Failed to navigate to 'circualem vitae' page: {e}")

    # Wait until the Resume List is visible
    try:
        # Wait for any resume container to be visible
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "col-lg-3"))
        )
        print("Resume list is visible.")
    except Exception as e:
        driver.save_screenshot("resume_list_visibility_failure.png")
        pytest.fail(f"Resume list did not load properly: {e}")


    resume_image_src_partial = "test_resume2.jpeg" 

    # Locate the resume image to ensure interacting with the correct resume
    try:
        resume_image = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//img[contains(@src, '{resume_image_src_partial}')]")
            )
        )
        highlight(resume_image, driver)
        print("Located the resume image in the resume list.")
    except Exception as e:
        driver.save_screenshot("locate_resume_image_failure.png")
        pytest.fail(f"Resume image not found in the list: {e}")

    # Locate the parent resume container (col-lg-3 div)
    try:
        # Traverse up the DOM to find the ancestor div with class 'col-lg-3'
        resume_container = resume_image.find_element(By.XPATH, "./ancestor::div[contains(@class, 'col-lg-3')]")
        highlight(resume_container, driver)
        print("Located the main resume container containing the image and delete button.")
    except Exception as e:
        driver.save_screenshot("locate_resume_container_failure.png")
        pytest.fail(f"Resume container not found: {e}")

    # Within the resume container, find and click the delete button
    try:
        # Find the delete button within the resume container
        delete_button = WebDriverWait(resume_container, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, ".//button[contains(@data-target, '#delete_confirm')]")
            )
        )
        highlight(delete_button, driver)
        delete_button.click()
        print("Clicked the delete button for the specified resume.")
    except Exception as e:
        driver.save_screenshot("click_delete_button_failure.png")
        pytest.fail(f"Delete button not found or could not be clicked: {e}")

    # Handle the delete confirmation modal
    try:
        # Wait for the delete confirmation modal to appear by locating the modal with specific text
        delete_modal = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'modal-content') and contains(., 'Etes-vous sûr de vouloir supprimer ce cv')]",
                )
            )
        )
        highlight(delete_modal, driver)
        print("Delete confirmation modal is visible.")

        # Click the 'Oui' (Yes) button to confirm deletion
        try:
            confirm_button = WebDriverWait(delete_modal, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//button[@type='submit' and normalize-space(text())='Oui']")
                )
            )
            highlight(confirm_button, driver)
            confirm_button.click()
            print("Clicked the 'Oui' button to confirm deletion.")
        except (TimeoutException, ElementClickInterceptedException) as e:
            driver.save_screenshot("click_oui_button_failure.png")
            print(f"Attempting JavaScript click for the 'Oui' button due to: {e}")
            # Fallback to JavaScript click
            driver.execute_script("arguments[0].click();", confirm_button)
            print("Clicked the 'Oui' button using JavaScript.")
    except TimeoutException:
        driver.save_screenshot("delete_confirmation_timeout.png")
        pytest.fail("Timed out waiting for the delete confirmation modal to appear.")
    except Exception as e:
        driver.save_screenshot("delete_confirmation_failure.png")
        pytest.fail(f"Failed to interact with the delete confirmation modal: {e}")

    # Verify that the delete confirmation modal is no longer present
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'modal-content') and contains(., 'Etes-vous sûr de vouloir supprimer ce cv')]",
                )
            )
        )
        print("Delete confirmation modal is no longer visible.")
    except Exception as e:
        driver.save_screenshot("delete_modal_invisibility_failure.png")
        pytest.fail("Delete confirmation modal did not disappear after confirming deletion.")

    # Verify that the resume is no longer in the resume list
    try:
        # Attempt to locate the resume container again; it should not be found
        driver.find_element(By.XPATH, f"//img[contains(@src, '{resume_image_src_partial}')]/ancestor::div[contains(@class, 'col-lg-3')]")
        pytest.fail("Resume was not deleted successfully: Resume card still exists.")
    except NoSuchElementException:
        # If NoSuchElementException is raised, it means the resume card is no longer present, which is expected
        print("Resume has been successfully deleted and is no longer present in the list.")
    except Exception as e:
        driver.save_screenshot("verify_resume_deletion_failure.png")
        pytest.fail(f"An unexpected error occurred while verifying resume deletion: {e}")

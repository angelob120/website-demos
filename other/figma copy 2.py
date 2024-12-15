import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def go_to_drafts_sort_and_duplicate_file():
    # Define the user data directory to persist session
    user_data_dir = os.path.expanduser("~/.figma_selenium")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--start-maximized")  # Open browser in maximized mode

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Navigate to the Figma homepage
        driver.get("https://www.figma.com/")
        time.sleep(5)  # Wait for the page to load

        # Check if logged in
        if "login" in driver.current_url:
            print("Not logged in. Please log in to your Figma account.")
            return

        # Step 2: Click the "Drafts" button
        try:
            drafts_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-onboarding-key='DRAFT_FOLDER_LINK_ONBOARDING_KEY']"))
            )
            drafts_button.click()
            print("Navigating to Drafts page...")
            time.sleep(5)  # Wait for the Drafts page to load
        except Exception as e:
            print(f"Failed to click the Drafts button: {e}")
            return

        # Step 3: Locate and click the "Last modified" dropdown
        try:
            # Locate the dropdown and open it
            last_modified_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'tile_sort_filter--dropdownContainer--443h-') and .//i18n-text[text()='Last modified']]"))
            )
            last_modified_dropdown.click()
            print("Opened 'Last modified' dropdown.")
            time.sleep(2)  # Allow time for dropdown content to load

            # Locate the "Alphabetical" option within the dropdown
            alphabetical_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i18n-text[text()='Alphabetical']"))
            )
            alphabetical_option.click()
            print("Selected 'Alphabetical' sorting.")
            time.sleep(3)  # Wait for sorting to apply
        except Exception as e:
            print(f"Failed to interact with sorting dropdown: {e}")
            return

        # Step 4: Search for the file "1 A Plumbing Template"
        search_term = "1 A Plumbing Template"
        print(f"Searching for '{search_term}' by scrolling the page.")
        file_element = None

        for _ in range(20):  # Try scrolling 20 times (adjust if needed)
            try:
                file_element = driver.find_element(By.XPATH, f"//span[text()='{search_term}']")
                if file_element:
                    print(f"File '{search_term}' found.")
                    break
            except Exception:
                driver.execute_script("window.scrollBy(0, 300);")  # Scroll down
                time.sleep(1)  # Allow time for loading

        if not file_element:
            print(f"File '{search_term}' not found after scrolling.")
            return

        # Step 5: Right-click the file to open the context menu
        print(f"Right-clicking the file '{search_term}'.")
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(driver)
        action.context_click(file_element).perform()
        time.sleep(2)  # Wait for the context menu to appear

        # Step 6: Select "Duplicate" from the context menu
        try:
            duplicate_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Duplicate')]"))
            )
            duplicate_option.click()
            print(f"File '{search_term}' duplicated successfully.")
        except Exception as e:
            print(f"Failed to locate 'Duplicate' option: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    go_to_drafts_sort_and_duplicate_file()
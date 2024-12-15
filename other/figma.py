import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def find_and_edit_text():
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

        # Step 2: Search for the file "1 A Plumbing Template"
        search_term = "1 A Plumbing Template"
        print(f"Searching for '{search_term}' by scrolling the page.")
        file_element = None

        for _ in range(20):  # Try scrolling 20 times (adjust if needed)
            try:
                # Locate the file element by its name
                file_element = driver.find_element(By.XPATH, f"//span[text()='{search_term}']")
                if file_element:
                    print(f"File '{search_term}' found.")
                    # Perform a double-click action to open the file
                    actions = ActionChains(driver)
                    actions.double_click(file_element).perform()
                    print(f"Opened file '{search_term}' with a double-click.")
                    time.sleep(10)  # Wait for the file to load
                    break
            except Exception:
                driver.execute_script("window.scrollBy(0, 300);")  # Scroll down
                time.sleep(1)  # Allow time for loading

        if not file_element:
            print(f"File '{search_term}' not found after scrolling.")
            return

        # Step 3: Search for all occurrences of 'A1234B' or 'A12B' and update them
        print("Checking for all instances of 'A1234B' or 'A12B' to update content.")
        updated_count = 0
        for _ in range(20):  # Scroll and search through the content
            try:
                # Find all instances of the text dynamically
                elements = driver.find_elements(By.XPATH, "//*[text()='A1234B' or text()='A12B']")
                for element in elements:
                    # Re-locate the element to avoid stale element references
                    element_text = element.text
                    if element_text == "A1234B":
                        print("Found 'A1234B', updating to 'A12B'.")
                        actions = ActionChains(driver)
                        actions.double_click(element).perform()
                        time.sleep(1)
                        element.clear()
                        element.send_keys("A12B")  # Update to 'A12B'
                    elif element_text == "A12B":
                        print("Found 'A12B', updating to 'A1234B'.")
                        actions = ActionChains(driver)
                        actions.double_click(element).perform()
                        time.sleep(1)
                        element.clear()
                        element.send_keys("A1234B")  # Update to 'A1234B'
                    updated_count += 1
                break  # Exit loop after updating all visible elements
            except Exception as e:
                print(f"Error during content update: {e}")
                driver.execute_script("window.scrollBy(0, 300);")  # Scroll down
                time.sleep(1)

        print(f"Updated {updated_count} instances.")

        # Step 4: Save the changes
        try:
            actions = ActionChains(driver)
            actions.key_down(u'\ue009').send_keys('s').key_up(u'\ue009').perform()  # Ctrl+S or Command+S
            print("Changes saved successfully.")
            time.sleep(3)  # Wait for saving to complete
        except Exception as e:
            print(f"Failed to save the file: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    find_and_edit_text()
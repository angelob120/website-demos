# import subprocess
# import platform
# import time
# import pyautogui

# def open_figma_and_duplicate_file():
#     system = platform.system()

#     try:
#         # Step 1: Open Figma application
#         if system == "Windows":
#             # Replace the path with the actual path to your Figma.exe file
#             subprocess.Popen(r"C:\Users\<YourUsername>\AppData\Local\Figma\Figma.exe")
#         elif system == "Darwin":  # macOS
#             subprocess.run(["open", "-a", "Figma"])
#         elif system == "Linux":
#             subprocess.Popen(["figma"])
#         else:
#             print("Unsupported operating system.")
#             return

#         # Wait for Figma to open
#         time.sleep(5)

#         # Step 2: Navigate to Drafts
#         pyautogui.hotkey('shift', 'd')  # Shortcut for Drafts
#         time.sleep(3)

#         # Step 3: Find and duplicate the file
#         # Adjust (x, y) coordinates based on where "1 A Plumbing Template" appears on your screen
#         file_position = (500, 500)  # Replace with actual coordinates of the file
#         pyautogui.rightClick(file_position)  # Simulate right-click on the file
#         time.sleep(1)

#         # Navigate the context menu to select "Duplicate"
#         # Adjust the (x, y) offset or menu navigation as necessary
#         pyautogui.move(0, 50)  # Move down to "Duplicate" option
#         pyautogui.click()      # Select the "Duplicate" option

#         print("File duplicated successfully.")

#     except FileNotFoundError:
#         print("Figma is not installed or the path is incorrect.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     open_figma_and_duplicate_file()




from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def duplicate_file_in_figma():
    # Set up the Selenium WebDriver (using Chrome in this example)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Open the Figma drafts page
        driver.get("https://www.figma.com/files/drafts")
        time.sleep(5)  # Wait for the page to load

        # Step 2: Locate the file called "1 A Plumbing Template"
        file_element = driver.find_element(By.XPATH, "//span[text()='1 A Plumbing Template']")
        
        # Step 3: Right-click the file
        actions = ActionChains(driver)
        actions.context_click(file_element).perform()
        time.sleep(2)  # Allow context menu to appear

        # Step 4: Click on "Duplicate" in the context menu
        duplicate_option = driver.find_element(By.XPATH, "//div[text()='Duplicate']")
        duplicate_option.click()
        time.sleep(2)  # Wait for the duplication to complete

        print("File duplicated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    duplicate_file_in_figma()
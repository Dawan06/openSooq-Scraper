from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://iq.opensooq.com/ar/find?search=true&term=الطاقة%20الشمسية")

wait = WebDriverWait(driver, 300)  # Wait up to 5 mins for manual login

try:
    # Step 1: Click first phone reveal button (this triggers login)
    phone_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.blueBtn")))
    phone_btn.click()

    print("✅ Clicked phone button, please complete login manually in the browser...")

    # Step 2: Wait until "إلغاء" button appears (login page)
    cancel_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'إلغاء')]")))
    print("🔵 Login in progress... waiting for you to finish")

    # Wait for "إلغاء" button to disappear (means login done, back to listing)
    wait.until(EC.invisibility_of_element(cancel_btn))
    print("✅ Login complete and back on listing page!")

    time.sleep(2)  # small wait for page update

    # Step 3: Scrape all visible phone numbers
    phone_buttons = driver.find_elements(By.CSS_SELECTOR, "div.blueBtn")

    with open("phone_numbers.txt", "w", encoding="utf-8") as f:  # open file once, overwrite if exists
        for i, btn in enumerate(phone_buttons, 1):
            try:
                btn.click()
                time.sleep(1)  # wait for number reveal
                number_text = btn.text.strip()
                print(f"📞 Number {i}: {number_text}")

                # Save number to file
                f.write(number_text + "\n")
            except Exception as e:
                print(f"❌ Failed to get number {i}: {e}")

except Exception as e:
    print("❌ Error during automation:", e)

driver.quit()

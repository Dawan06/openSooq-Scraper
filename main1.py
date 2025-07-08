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
wait = WebDriverWait(driver, 300)  # wait up to 5 mins for login on first page

base_term = "الطاقة الشمسية"
max_pages = 3

phone_numbers = []

for page_num in range(1, max_pages + 1):
    # Build URL
    if page_num == 1:
        url = f"https://iq.opensooq.com/ar/find?search=true&term={base_term.replace(' ', '%20')}"
    else:
        url = f"https://iq.opensooq.com/ar/find?page={page_num}&term={base_term.replace(' ', '+')}"

    print(f"➡️ Loading page {page_num}: {url}")
    driver.get(url)

    if page_num == 1:
        # Step 1: click first phone button to trigger login
        try:
            phone_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.blueBtn")))
            phone_btn.click()
            print("✅ Clicked phone button, please complete login manually...")

            # Wait for "إلغاء" button (cancel) during login
            cancel_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'إلغاء')]")))
            print("🔵 Waiting for login to complete...")

            # Wait until cancel button disappears (means login done)
            wait.until(EC.invisibility_of_element(cancel_btn))
            print("✅ Login complete, back to listing page!")

            time.sleep(2)
        except Exception as e:
            print("❌ Error during login process:", e)
            driver.quit()
            exit(1)

    else:
        # For pages >1, just wait for the numbers to load
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.blueBtn")))
            time.sleep(2)  # small wait for page fully loaded
        except Exception as e:
            print(f"❌ Failed to load numbers on page {page_num}: {e}")
            continue

    # Scrape all phone numbers on the current page
    phone_buttons = driver.find_elements(By.CSS_SELECTOR, "div.blueBtn")

    print(f"🔍 Found {len(phone_buttons)} phone buttons on page {page_num}")

    for i, btn in enumerate(phone_buttons, 1):
        try:
            btn.click()
            time.sleep(1)
            number_text = btn.text.strip()
            print(f"📞 Page {page_num} - Number {i}: {number_text}")
            phone_numbers.append(number_text)
        except Exception as e:
            print(f"❌ Failed to get number {i} on page {page_num}: {e}")

# Save all numbers to file
with open("all_phone_numbers.txt", "w", encoding="utf-8") as f:
    for num in phone_numbers:
        f.write(num + "\n")

print(f"✅ Saved {len(phone_numbers)} phone numbers from {max_pages} pages.")

driver.quit()

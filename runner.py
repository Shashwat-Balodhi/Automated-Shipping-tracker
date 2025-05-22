import json
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def extract_booking_id(prompt):
    match = re.search(r"SINI\d{8}", prompt)
    return match.group(0) if match else None

def run_replay(prompt):
    booking_id = extract_booking_id(prompt)
    if not booking_id:
        return {"error": "Booking ID not found."}

    # Load stored interaction steps
    with open("steps.json", "r") as f:
        steps = json.load(f)

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do")
        time.sleep(5)
        result = {}

        for step in steps:
            action = step["action"]
            selector = step["selector"]
            value = step.get("value")

            # 🛡 Auto-detect or fallback to XPath
            if selector.startswith("By.NAME:"):
                by, key = By.NAME, selector.partition(":")[2].strip()
            elif selector.startswith("By.ID:"):
                by, key = By.ID, selector.partition(":")[2].strip()
            elif selector.startswith("By.XPATH:"):
                by, key = By.XPATH, selector.partition(":")[2].strip()
            else:
                # fallback if no By prefix is present
                by, key = By.XPATH, selector.strip()

            print(f"[DEBUG] {action.upper()} using: {key}")

            if action == "type":
                el = driver.find_element(by, key)
                el.clear()
                el.send_keys(booking_id)

            elif action == "click":
                driver.find_element(by, key).click()

            elif action == "read":
                text = driver.find_element(by, key).text.strip()
                # Try to label cleanly
                if "Voyage" in key:
                    result["voyage"] = text
                elif "Arrival" in key:
                    result["arrival"] = text
                else:
                    result[key] = text

            time.sleep(2)

        result["booking_id"] = booking_id
        return result

    finally:
        driver.quit()

if __name__ == "__main__":
    prompt = input("Enter your prompt with a new booking ID: ")
    result = run_replay(prompt)
    print("\n✅ Replayed Result:")
    print(result)

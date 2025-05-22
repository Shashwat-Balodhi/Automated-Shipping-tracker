# tracker.py
import re
import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

recorded_steps = []

def log_step(action, selector, value=None):
    step = {"action": action, "selector": selector}
    if value:
        step["value"] = value
    recorded_steps.append(step)

def save_steps():
    with open("steps.json", "w") as f:
        json.dump(recorded_steps, f, indent=2)

def extract_booking_id(prompt):
    match = re.search(r"SINI\d{8}", prompt)
    return match.group(0) if match else None

def get_hmm_info(prompt):
    booking_id = extract_booking_id(prompt)
    if not booking_id:
        return {"error": "Booking ID not found in prompt."}

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do")
        time.sleep(5)

        # Step 1: Input B/L No.
        bl_input = driver.find_element(By.NAME, "srchBlNo1")
        bl_input.clear()
        bl_input.send_keys(booking_id)
        log_step("type", "By.NAME:srchBlNo1", booking_id)
        time.sleep(1)

        # Step 2: Click Retrieve
        retrieve_button = driver.find_element(By.XPATH, '//button[text()="Retrieve"]')
        retrieve_button.click()
        log_step("click", 'By.XPATH://button[text()="Retrieve"]')
        time.sleep(5)

        # Step 3: Extract Voyage and Arrival
        voyage_xpath = '(//div[normalize-space()="Vessel / Voyage"]/ancestor::table//tbody/tr/td[1]/div)[1]'
        arrival_xpath = '(//div[normalize-space()="Arrival"]/ancestor::table//tbody/tr/td[last()]/div)[1]'

        voyage = driver.find_element(By.XPATH, voyage_xpath).text.strip()
        arrival = driver.find_element(By.XPATH, arrival_xpath).text.strip()
        log_step("read", voyage_xpath)
        log_step("read", arrival_xpath)

        save_steps()

        return {
            "booking_id": booking_id,
            "voyage": voyage,
            "arrival": arrival
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

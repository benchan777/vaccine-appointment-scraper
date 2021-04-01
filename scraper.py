from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time

load_dotenv()

# Configure options for Chrome webdriver
options = webdriver.ChromeOptions()
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument("--window-size=1690,1000")

def walgreens_scraper(location):
    driver = webdriver.Chrome(executable_path = os.getenv('webdriver_path'), options = options)
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19")
    schedule_new_appointment = driver.find_element_by_xpath("//span[@class='btn btn__blue']")
    # schedule_new_appointment = driver.find_element_by_css_selector('span.btn.btn__blue')
    schedule_new_appointment.click()
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19/location-screening")

    if alert_element(driver) == False:
        location_input = driver.find_element_by_id("inputLocation")
        search_button = driver.find_element_by_xpath("//button[@class='btn' and @data-reactid='16']")

        # Clear the input field, then input location
        location_input.clear()
        location_input.send_keys(location)

        # Click search button. Delay 1 second to account for delay it takes for alert element to appear.
        search_button.click()
        time.sleep(1)
        
        alert = alert_element(driver)
        print(alert.text)
        driver.close()
        time.sleep(10)

def alert_element(driver):
    ''' Check if the alert element exists '''
    try:
        alert = driver.find_element_by_xpath("//div[@class='alert alert__red mt25']")
    except Exception as e:
        try:
            alert = driver.find_element_by_xpath("//div[@class='alert alert__green']")
        except Exception as e:
            return False

    if alert:
        return alert
    
if __name__ == "__main__":
    while True:
        walgreens_scraper("90014")
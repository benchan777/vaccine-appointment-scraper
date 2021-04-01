from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, smtplib

load_dotenv()

# Configure options for Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1720,1176")

availability = ''
proxy_index = 0

def walgreens_scraper(location):
    driver = webdriver.Chrome(executable_path = os.getenv('webdriver_path'), options = options)
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19")
    driver.find_element_by_xpath("//span[@class='btn btn__blue']").click() # Click "Schedule new appointment" button
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19/location-screening")

    if alert_element(driver) == False:
        try:
            location_input = driver.find_element_by_id("inputLocation")
        except:
            print("Unable to find input element. Probably received access denied error.")
            driver.close()
            proxy_rotator(driver)
            return

        try:
            search_button = driver.find_element_by_xpath("//button[@class='btn' and @data-reactid='16']")
        except:
            print("Unable to find search button. Probably received access denied error.")
            driver.close()
            proxy_rotator(driver)
            return

        # Clear the input field, then input location
        location_input.clear()
        location_input.send_keys(location)

        # Click search button. Wait 1.5 seconds before checking for alert element to account for delay it takes for alert element to appear.
        search_button.click()
        time.sleep(1.5)
        
        alert = alert_element(driver)
        try:
            status = alert.text
        except:
            status = "N/A"

        print(status)

        global availability
        if status != availability:
            if status == 'Appointments available!':
                pass

            elif status == 'Appointments unavailable':
                pass

            else:
                print("Availability N/A. Maybe scraping failed?")

        driver.close()
        time.sleep(60)

def alert_element(driver):
    ''' Check if the alert element exists '''
    try:
        # Checks for element that appears when appointments are shown as unavailable
        alert = driver.find_element_by_xpath("//div[@class='alert alert__red mt25']")
    except Exception as e:
        try:
            # Checks for element that appears when appointments are shown as available
            alert = driver.find_element_by_xpath("//div[@class='alert alert__green']")
        except Exception as e:
            return False

    if alert:
        return alert

def proxy_rotator(driver):
    ''' Proxy rotator to deal with bot detection '''
    global proxy_index
    global options
    proxy_list = ['165.225.77.46:80', '168.119.137.56:3128', '173.249.13.171:3128']

    if proxy_index <= len(proxy_list) - 1:
        print(f"Attempting again with {proxy_list[proxy_index]}.")

        # Re-instantiate ChromeOptions to use a new ip address
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1280,720")
        options.add_argument('--proxy-server=%s' % proxy_list[proxy_index])
        proxy_index += 1
        return

    else:
        print(f"Reached end of proxy list. Resetting back to default ip.")

        # Re-instantiate ChromeOptions to use user's ip address after we have exhausted the list of proxies
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        proxy_index = 0
        return

def send_text(availability):
    pass
    
if __name__ == "__main__":
    zip_code = input("Enter zip code to check for: ")
    while True:
        walgreens_scraper(zip_code)
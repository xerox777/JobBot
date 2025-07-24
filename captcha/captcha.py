import logging
import random
import string
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import os
import whisper
import warnings

warnings.filterwarnings("ignore")

model = whisper.load_model("base")
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='../captcha_automation.log',  # Specify the log file name here
                    filemode='w')
logger = logging.getLogger()

# Log the start of the process
logger.info("Starting the login automation script...")

def transcribe(url):
    with open('../.temp', 'wb') as f:
        f.write(requests.get(url).content)
        print(f"url:{url}, f:{f}")
    result = model.transcribe('../.temp')
    return result["text"].strip()


def enter_fname(driver, fname):
    driver.find_element(By.ID, "firstName").click()
    driver.find_element(By.ID, "firstName").send_keys(fname)

def enter_lname(driver, lname):
    driver.find_element(By.ID, "lastName").click()
    driver.find_element(By.ID, "lastName").send_keys(lname)

def set_bday(driver):
    month = driver.find_element(By.ID, "month")
    month.click()
    month.send_keys("J")
    month.send_keys(Keys.RETURN)
    day = driver.find_element(By.ID, "day")
    day.send_keys("11")
    year = driver.find_element(By.ID, "year")
    year.send_keys("1989")
    gender = driver.find_element(By.ID, "gender")
    gender.click()
    gender.send_keys("M")
    gender.send_keys(Keys.RETURN)

def click_checkbox(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()

def generate_random_string(length=9):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def enter_password(driver):
    pswd = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Password")]')
    password_value = generate_random_string(length=12)
    pswd.send_keys(password_value)
    confirm_pswd = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Confirm")]')
    confirm_pswd.send_keys(password_value)
    logging.info(f"Password:{password_value}")


def find_all_buttons_and_click_first(driver):
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    fbutton = buttons[0]
    fbutton.click()

def find_input_and_enter_random_value(driver):
    input = driver.find_elements(By.TAG_NAME, 'input')
    finput = input[0]
    usrname = generate_random_string()
    finput.send_keys(generate_random_string())
    logging.info(f"Username:{usrname}@gmail.com")

def request_audio_version(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(
        driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()


def solve_audio_captcha(driver):
    text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
    driver.find_element(By.ID, "audio-response").send_keys(text)
    driver.find_element(By.ID, "recaptcha-verify-button").click()

def find_radio(driver):
    radio_div = driver.find_elements(By.XPATH, '//div[@role="radio"]')
    for radio in radio_div:
        if 'create' in radio.accessible_name.lower():
            radio.click()

if __name__ == "__main__":
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    chromedriver_path = "C:\\Users\\E08802\\Downloads\\chromedriver-win64_latest\\chromedriver-win64\\chromedriver.exe"
    chrome_service = ChromeService(executable_path=chromedriver_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    demo_url = "https://www.google.com/recaptcha/api2/demo"
    g_create_acc_url = "https://accounts.google.com/lifecycle/steps/signup/name?ddm=1&dsh=S1896790409:1734551319670186&flowEntry=SignUp&flowName=GlifWebSignIn&ifkv=AeZLP9-K5nYI-uKt0PVFX61z8FjPgMhc6Xl6PYlFpPQkaIH1Ps7PvGbRFjAovguXbGB55Jk0gTckIg&TL=AE--LlxqpFpm-KGR485U7t1ZPZ1Fcm-YulCFntxCtrjJ_WKhOHePdf2FJeh7n_vO&continue=https://accounts.google.com/ManageAccount?nc%3D1"
    driver.get(demo_url)
    # time.sleep(2.5)
    # find_all_buttons_and_click_first(driver)
    # time.sleep(2.5)
    # enter_fname(driver, "Bryan")
    # time.sleep(2.5)
    # enter_lname(driver, "Langlan")
    # find_all_buttons_and_click_first(driver)
    # time.sleep(1)
    # set_bday(driver)
    # find_all_buttons_and_click_first(driver)
    # time.sleep(2)
    # find_radio(driver)
    # find_input_and_enter_random_value(driver)
    # find_all_buttons_and_click_first(driver)
    # time.sleep(4)
    # enter_password(driver)
    # find_all_buttons_and_click_first(driver)
    click_checkbox(driver)
    time.sleep(1)
    request_audio_version(driver)
    time.sleep(1)
    for _ in range(0, 3):
        solve_audio_captcha(driver)
        time.sleep(10)
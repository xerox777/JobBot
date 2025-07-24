import re
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# MostRecentChromeDriver=ChromeDriverManager().install()
import os
import datetime
import sys
import time

# install with pip install openai-whisper, pip install ffmpeg (may need tpio modify audio.py file)
from captcha import click_checkbox, request_audio_version, solve_audio_captcha
from dotenv import load_dotenv

load_dotenv()


class dataParser:
    targetUrl = "https://www.linkedin.com/jobs/search/?currentJobId=4137578675&keywords=software%20engineer&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

    def __init__(self, buffer=None):
        self.__buffer = buffer
        self.jobs = []

    def printAllJobs(self):
        for job in self.jobs:
            print(job)
            print("-" * 175)

    def parseOutJobListings(self):
        usr = getpass.getuser()
        chromedriver_path = (
            f"C:\\Users\\{usr}\\Downloads\\chromedriver-win64\\chromedriver.exe"
        )
        print(f"chromedriver_path:{chromedriver_path}")
        chrome_service = ChromeService(executable_path=chromedriver_path)
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        # chrome_options.add_argument("--headless=new")
        html = None
        with webdriver.Chrome(service=chrome_service, options=chrome_options) as driver:
            driver.get(dataParser.targetUrl)
            main_window = driver.current_window_handle
            html = driver.page_source
            time.sleep(3)
            wait = WebDriverWait(driver, 10)
            modalSection = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "section.max-h-full.modal__wrapper")
                )
            )
            # Add tabindex attribute to make section focusable
            driver.execute_script(
                "arguments[0].setAttribute('tabindex', '-1');", modalSection
            )
            driver.execute_script("arguments[0].focus();", modalSection)
            modalWait = WebDriverWait(modalSection, 10)
            time.sleep(5)
            # signInBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sign-in-modal__outlet-btn")))
            signInBtn = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.sign-in-modal__outlet-btn")
                )
            )
            if signInBtn.is_displayed() and signInBtn.is_enabled():
                signInBtn.click()
            else:
                driver.execute_script(
                    "arguments[0].removeAttribute('disabled');", signInBtn
                )
                print("Sign-In Button disabled...")
                driver.execute_script("arguments[0].click();", signInBtn)
            usrInput = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[name='session_key']")
                )
            )
            pswdInput = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[name='session_password']")
                )
            )
            driver.execute_script(
                f"""
                       var inputField = arguments[0];
                       inputField.removeAttribute('disabled');
                       inputField.value = '{os.getenv("GOOG_USER")}';  // You can replace with any text you need
                   """,
                usrInput,
            )
            driver.execute_script(
                f"""
                                   var inputField = arguments[0];
                                   inputField.removeAttribute('disabled');
                                   inputField.value = '{os.getenv("GOOG_PSWD")}';  // You can replace with any text you need
                               """,
                pswdInput,
            )
            # usrInput.send_keys(os.getenv('GOOG_USER'))
            # pswdInput.send_keys(os.getenv('GOOG_PSWD'))

            signInBtn = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.sign-in-form__submit-btn--full-width")
                )
            )
            driver.execute_script(
                "arguments[0].removeAttribute('disabled');", signInBtn
            )
            driver.execute_script("arguments[0].click();", signInBtn)
            # signInBtn.click()
            driver.get(dataParser.targetUrl)

            JobListings = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-job-id]"))
            )
            jobSet = set()
            for job in JobListings:
                jobSet.add(job.text)
            curSetLength = len(jobSet)
            difference = -1
            offset = 0
            time.sleep(2.5)
            while difference != 0:
                divJobs = driver.find_element(
                    By.CSS_SELECTOR, "div.CDuvtdIUsnyiYbKhsOagsZhjikjIYEhIUU"
                )
                # actions = ActionChains(driver)
                # actions.move_to_element(divJobs).scroll_by_amount(offset, 500+offset).perform()
                driver.execute_script(
                    "arguments[0].scrollBy(arguments[1], arguments[2]);",
                    divJobs,
                    offset,
                    500 + offset,
                )
                time.sleep(0.33)
                newJobs = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "[data-job-id]")
                    )
                )
                for job in newJobs:
                    jobSet.add(job.text)
                offset += 500
                newSetLength = len(jobSet)
                difference = newSetLength - curSetLength
                curSetLength = newSetLength
                time.sleep(2)
            wait = WebDriverWait(driver, 10)
            for jobListing in jobSet:
                try:
                    driver.execute_script(
                        "arguments[0].removeAttribute('disabled');", jobListing
                    )
                    driver.execute_script("arguments[0].click();", jobListing)
                    # grab job info
                    jobInfo = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.jobs-box__html-content")
                        )
                    )
                    # print(jobInfo.text)
                    self.jobs.append(jobInfo.text)
                except Exception as e:
                    print(e)
                # jobListing.click()
                time.sleep(3)

            print(len(jobSet))
            for job in jobSet:
                print(job)
            # session_key & session_password
            # searchBox.send_keys("Cute Cat Memes")
            input("Press Enter to exit or CTRL+C to terminate the Script.")
            driver.quit()
            return

    def parseOutCompanyName(self):
        pass

    def parseOutRequiredExperience(self):
        pass

    def parseOutRequiredSkills(self):
        pass

    def parseOutOtherKeywords(self):
        pass


class job:
    def __init__(self, url):
        self.targetUrl = url
        self.description = None
        self.keywords = []  # word list
        self.qualifications = []  # word list
        self.experience = []  # word list

    def parseMetaData(self):
        pass
        searchButton = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "btnK"))
        )
        time.sleep(1)
        searchButton.click()
        time.sleep(4)
        click_checkbox(driver)
        time.sleep(1)
        request_audio_version(driver)
        time.sleep(1)
        for _ in range(0, 3):
            solve_audio_captcha(driver)
            time.sleep(10)
        print(html)
        _metaData = metaData(html)  # revisit this, may need to authenticate to LinkedId
        print(_metaData.test())
        # (TODO: parse relevant keywords, skills, experience mentioned in job listing)


class programmerLookingForWork:
    targetUrl = "https://chatgpt.com/"

    def __init__(self, pathToResume=None, pathToCV=None, pathToRecommendation=None):
        if pathToResume == None or pathToCV == None or pathToRecommendation == None:
            return
        with open(pathToResume, "r") as f:
            self.resume = f.read()
        with open(pathToCV, "r") as f:
            self.cover_letter = f.read()
        with open(pathToRecommendation, "r") as f:
            self.recommendation = f.read()

    def craftPerfectResume(self):
        chromedriver_path = "C:\\Users\\E08802\\Downloads\\chromedriver-win64_latest\\chromedriver-win64\\chromedriver.exe"
        chrome_service = ChromeService(executable_path=chromedriver_path)
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        # chrome_options.add_argument("--headless=new")
        html = None
        with webdriver.Chrome(service=chrome_service, options=chrome_options) as driver:
            driver.get(programmerLookingForWork.targetUrl)
            main_window = driver.current_window_handle
            html = driver.page_source
            time.sleep(3)
            wait = WebDriverWait(driver, 10)
            # format -> input[name='session_password']
            prompt = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[id='prompt-textarea']")
                )
            )
            driver.execute_script(
                f"""
                                              var inputField = arguments[0];
                                              inputField.removeAttribute('disabled');
                                              inputField.value = 'hello there.';  // You can replace with any text you need
                                          """,
                prompt,
            )
            prompt.send_keys("hello there.")

            sendBtn = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[data-testid='send-button']")
                )
            )
            driver.execute_script("arguments[0].removeAttribute('disabled');", sendBtn)
            driver.execute_script("arguments[0].click();", sendBtn)
            # text_input = div['id']="prompt-textarea", button['data-tesid'] = "send-button"
        input("Press Enter to exit or CTRL+C to terminate the Script.")
        driver.quit()
        return

    def craftPerfectCV(self, parsedData):
        pass

    def useAppropriateRecommendations(self, parsedData):
        pass

    def applytoJob(self, job):
        job.parseMetaData()
        self.craftPerfectCV()
        self.craftPerfectResume()
        self.useAppropriateRecommendations()
        pass


if __name__ == "__main__":
    # person = programmerLookingForWork()
    # person.craftPerfectResume()
    # pass
    myParser = dataParser()
    myParser.parseOutJobListings()
    myParser.printAllJobs()

    # _job = job()
    # _job.parseMetaData()
    pass
    # testProcess()

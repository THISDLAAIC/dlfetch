import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from sys import exit



def sign_in(cookie_path: str):
    user_name = os.environ.get('THISDL_USERNAME')
    password = os.environ.get('THISDL_PASSWORD')

    if not user_name or not password:
        print('Please set environment variables THISDL_USERNAME and THISDL_PASSWORD')
        exit(1)

    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Firefox(options=options)
    driver.get('https://thisdlstu.schoolis.cn/')
    account_container = driver.find_element(By.XPATH, "//div[@ng-class='$ctrl.styles.accountContainer']")
    inputs = account_container.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(user_name)
    inputs[1].send_keys(password)
    account_container.find_element(By.TAG_NAME, "button").click()

    try:
        WebDriverWait(driver, 1).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//div[@ng-class='$ctrl.styles.navBar']"))
        )
    except TimeoutException:
        error_message = account_container.find_element(By.XPATH, "//p[@ng-class='$ctrl.styles.inputError']")
        print(error_message.text)
        exit(1)
    print("Sign in successfully.")
    print("Saving cookies to file...")
    with open(cookie_path, 'w') as cookie_file:
        cookie_file.write(str(driver.get_cookies()))
    print("Cookies saved.")
    cookies = driver.get_cookies()
    driver.quit()
    return cookies
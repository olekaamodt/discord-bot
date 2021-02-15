from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def login_and_pay(url, cookies):
    jsonData = open("token.json")
    tokenObj = json.load(jsonData)
    jsonData.close()
    user_email = tokenObj["EMAIL"]
    user_password = tokenObj["PASSWORD"]

    driver = webdriver.Chrome("chromedriver.exe")


    driver.get(url)

    for cookie in cookies:
        driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'path': cookie.path, 'expire': cookie.expires})

    current_url = driver.current_url

    cookie_button = driver.find_elements_by_xpath('//button[@class="cpBanner-button cpBanner-button--accept"]')[0]
    cookie_button.click()

    email = driver.find_elements_by_xpath('//input[@id="Email"]')[0]
    password = driver.find_elements_by_xpath('//input[@id="Password"]')[0]

    email.send_keys(user_email)
    password.send_keys(user_password)

    login_button = driver.find_elements_by_xpath('//button[@class="btn btn--primary btn--block submit"]')[0]
    login_button.click()


    try:
        WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        check_info = driver.find_elements_by_xpath('//button[@class="btn btn--primary btn--block"]')[0]
        check_info.click() 

        #WebDriverWait(driver, 15).until(EC.url_changes(current_url))
        driver.close()

    except:
        assert "No results found." not in driver.page_source
        driver.close()

#login_and_pay("https://www.just-eat.no/account/login?returnurl=%2Forder%2Fdelivery-address%2F%3Fmenu%3D746%26basket%3DgkFQOeJXY0ysUY2t1xhDsQ%26collection%3DFalse")
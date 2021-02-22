from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def login_and_pay(url, items):
    jsonData = open("token.json")
    tokenObj = json.load(jsonData)
    jsonData.close()
    user_email = tokenObj["EMAIL"]
    user_password = tokenObj["PASSWORD"]

    driver = webdriver.Chrome("chromedriver.exe")
    print(url)

    driver.get(url)

    current_url = driver.current_url
    time.sleep(2)

    #cookie_button = driver.find_elements_by_xpath('//button[@class="cpBanner-button cpBanner-button--accept"]')[0]
    #cookie_button.click()
    

    """for item in items:
        add_to_cart_button = driver.find_elements_by_xpath('//div[@data-product-id=' + "\"" + str(item[1]) + "\"" + ']//button')[0]
        add_to_cart_button.click()
        time.sleep(2)
        if driver.find_elements_by_xpath('//button[@id="collectiononly-collection-action"]') != []:
            order_button = driver.find_elements_by_xpath('//button[@id="collectiononly-collection-action"]')[0]
            order_button.click()"""

    cookie_button = driver.find_elements_by_xpath('//button[@class="cpBanner-button cpBanner-button--accept"]')[0]
    cookie_button.click()

    email = driver.find_elements_by_xpath('//input[@id="Email"]')[0]
    password = driver.find_elements_by_xpath('//input[@id="Password"]')[0]

    email.send_keys(user_email)
    password.send_keys(user_password)

    login_button = driver.find_elements_by_xpath('//button[@class="btn btn--primary btn--block submit"]')[0]
    login_button.click()


    
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    phone_input = driver.find_elements_by_xpath('//input[@id="Phone"]')[0]
    phone_input.send_keys("")
    phone_input.send_keys(tokenObj["phoneNR"])

    address = driver.find_elements_by_xpath('//input[@id="Address_Lines_Line1"]')[0]
    address.send_keys("")
    address.send_keys(tokenObj["address"])

    addressNR = driver.find_elements_by_xpath('//input[@id="Address_Lines_Line2"]')[0]
    addressNR.send_keys("")
    addressNR.send_keys(tokenObj["addressNR"])

    place = driver.find_elements_by_xpath('//input[@id="Address_Lines_Line3"]')[0]
    place.send_keys("")
    place.send_keys(tokenObj["place"])

    addressPlace = driver.find_elements_by_xpath('//input[@id="Address_City"]')[0]
    addressPlace.send_keys("")
    addressPlace.send_keys(tokenObj["place"])

    postal_code = driver.find_elements_by_xpath('//input[@id="Address_Postcode"]')[0]
    postal_code.send_keys("")
    postal_code.send_keys(tokenObj["postNR"])



    check_info = driver.find_elements_by_xpath('//button[@class="btn btn--primary btn--block"]')[0]
    check_info.click() 

    time.sleep(10)

    driver.close()

    

#login_and_pay("https://www.just-eat.no/restaurants-mathus-chicken/menu", [('Mathus Special Box ', 445559),('Bucket Mix ', 352966), ('Chicken Duo Box ', 352965)])
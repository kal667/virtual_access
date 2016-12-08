from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
import urllib2

refreshrate=int(10)
driver = webdriver.Chrome()
driver.get("http://umd-openxc.azurewebsites.net/devices/352682050225977/data")

username = driver.find_element_by_id("UserName")
password = driver.find_element_by_id("Password")

username.send_keys("OpenXCAdmin")
password.send_keys("VXdDaBvdDU29rofs4Bmg")

xpath = '//input[@type="submit"]'
driver.find_element_by_xpath(xpath).click()

raw_input("Select date. Then press 'enter' to continue ...")

xpath = '//button[@type="submit"]'
driver.find_element_by_xpath(xpath).click()

while True:
    time.sleep(refreshrate)
    print('Refresh')
    driver.refresh()
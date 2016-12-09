#!/usr/local/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
import urllib2
import json

refreshrate=int(30)
driver = webdriver.Chrome()
driver.get("http://umd-openxc.azurewebsites.net/devices/352682050225977/data")

username = driver.find_element_by_id("UserName")
password = driver.find_element_by_id("Password")

username.send_keys("OpenXCAdmin")
password.send_keys("VXdDaBvdDU29rofs4Bmg")

#Clicks Login
xpath = '//input[@type="submit"]'
driver.find_element_by_xpath(xpath).click()

#User sets date in browser for data to simulate
raw_input("Select date. Then press 'enter' to continue ...")

#Query data at that date
xpath = '//button[@type="submit"]'
driver.find_element_by_xpath(xpath).click()

#Display 100 elements
xpath = '//select[@name="loggedDataTable_length"]//option[@value="100"]'
driver.find_element_by_xpath(xpath).click()

#Sort newest first
xpath = '//th[@class="sorting_asc"]'
driver.find_element_by_xpath(xpath).click()

#Create array to hold CAN messages: timestamp / bus / id / data
CAN_data = []
CAN_data.append([])
CAN_data.append([])
CAN_data.append([])
CAN_data.append([])

while True:
	#Get table rows
	xpath = '//table[@id="loggedDataTable"]/tbody/tr'
	rows = driver.find_elements_by_xpath(xpath)
	rowCount = len(rows)
	print 'Row count = ', rowCount

	#Reading from bottom to top because new data loads to top
	datum = 0
	for i in reversed(range(rowCount)):
		#print rows[i].text
		header, data = rows[i].text.split("M",1)
		#print header
		#print data
		parsed = json.loads(data)
		#Reads timestamp for every record in the row
		for each in parsed['records']:
			CAN_data[0].append(each['timestamp'])
			print(each['timestamp'])
			datum += 1
	print 'Datum = ', datum
	print CAN_data


	#Refresh
	time.sleep(refreshrate)
	print 'Refresh'
	driver.refresh()
#!/usr/local/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
import urllib2
import json
from datetime import datetime
import calendar

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

#Initialize 
base_timestamp = 0;
last_timestamp = 0
message_count = 0
#Gets current UTC time and converts to timestamp
base_time = datetime.utcnow()
base_time = calendar.timegm(base_time.utctimetuple())

while True:
	#Get table rows
	xpath = '//table[@id="loggedDataTable"]/tbody/tr'
	rows = driver.find_elements_by_xpath(xpath)
	rowCount = len(rows)

	#Reading from bottom to top because new data loads at top
	for row in reversed(range(rowCount)):
		header, data = rows[row].text.split("M",1)
		parsed = json.loads(data)
		#Reads timestamp for every record in the row
		for each in parsed['records']:
			#Assigns base timestamp
			if base_timestamp == 0:
				base_timestamp = int(each['timestamp'])
			#Reads
			if int(each['timestamp']) > last_timestamp:
				CAN_data[0].append(each['timestamp'])
				last_timestamp = int(each['timestamp'])
				message_count += 1
	
	print 'Message Count = ', message_count
	
	#Prints timestamp if time is greater than relative time 
	while len(CAN_data[0]) != 0:
		current_time = datetime.utcnow()
		current_time = calendar.timegm(current_time.utctimetuple())
		if (current_time - base_time) > ((CAN_data[0][0] - base_timestamp)/1000):
			print CAN_data[0][0]
			CAN_data[0].pop(0)
			message_count -= 1

	#Refresh
	print 'Sleep'
	time.sleep(refreshrate)
	print 'Refresh'
	driver.refresh()
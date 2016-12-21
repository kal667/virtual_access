#!/usr/local/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openxc_script import write_CAN_message
from datetime import datetime
import time
import urllib
import urllib2
import json
import calendar

def navigate_to_data(driver):
	#Opens browser and queries data on server

	#Chrome browser navigates to azure site
	driver.get("http://umd-openxc.azurewebsites.net/devices/352682050225977/data")

	username = driver.find_element_by_id("UserName")
	password = driver.find_element_by_id("Password")

	#Enters username and password
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

	return;

def get_messages(driver, CAN_data, base_timestamp, last_timestamp, message_count):
	#Read all CAN messages into the CAN_data array
	
	#Get message table rows
	xpath = '//table[@id="loggedDataTable"]/tbody/tr'
	rows = driver.find_elements_by_xpath(xpath)
	rowCount = len(rows)

	#Reading from bottom to top because new data loads at top
	for row in reversed(range(rowCount)):
		header, data = rows[row].text.split("M",1)
		#This is the length of an empty record
		if len(data) > 15:
			#Reformat JSON to remove partial data at beginning and end of string
			records, data = data.split("[",1)
			trash, data = data.split("{",1)
			data = data[::-1]
			trash, data = data.split("]",1)
			trash,data = data.split("}",1)
			data = data[::-1]
			#Recreate poperly formatted JSON
			data = records + '[{' + data + '}]}'
			parsed = json.loads(data)
			#Reads timestamp for every record in the row
			for each in parsed['records']:
				#Assigns base timestamp
				if base_timestamp == 0:
					base_timestamp = int(each['timestamp'])
#
#TODO: Must sort entries in each row by time...
#
				#Reads
				if int(each['timestamp']) > last_timestamp:
					CAN_data[0].append(each['timestamp'])
					CAN_data[1].append(each['bus'])
					CAN_data[2].append(each['id'])
					CAN_data[3].append(each['data'])
					last_timestamp = int(each['timestamp'])
					message_count += 1

	return base_timestamp, last_timestamp, message_count;


def main():

	#Create array to hold CAN messages: timestamp / bus / id / data
	CAN_data = []
	for i in range(4):
		CAN_data.append([])

	#Initialize 
	driver = webdriver.Chrome()
	base_timestamp = 0;
	last_timestamp = 0
	message_count = 0

	#set refreshrate if applicable
	refreshrate = int(5)
    
	navigate_to_data(driver)
	while True:
		base_timestamp, last_timestamp, message_count = get_messages(driver, CAN_data, base_timestamp, last_timestamp, message_count)
		print 'Message Count = ', message_count
		print 'Basetimestamp = ', base_timestamp
		print 'Lasttimestamp = ', last_timestamp
		write_CAN_message(CAN_data, base_timestamp)
		#Refresh
		print 'Sleep'
		time.sleep(refreshrate)
		print 'Refresh'
		driver.refresh()

if __name__ == "__main__":
    main()

#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import urllib
import urllib2
from openxc.interface import UsbVehicleInterface
from openxc.formats.base import VehicleMessageStreamer
from openxc.formats.binary import ProtobufStreamer, ProtobufFormatter
from openxc.formats.json import JsonStreamer, JsonFormatter
import calendar
import json

def write_CAN_message(CAN_data, base_CAN_timestamp, start_program_timestamp):
	#This writes a low-level CAN message to the bus

	print 'Setting VI'
	vi = UsbVehicleInterface()

	print 'Setting Payload Format'
	vi.set_payload_format(json)

	print 'Writing to CAN'
	#vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0])
	vi.write(bus=1, id=42, data="0x1234567812345678")

	return;

def main():

	#Create array to hold CAN messages: timestamp / bus / id / data
	CAN_data = []
	for i in range(4):
		CAN_data.append([])

	CAN_data[1].append(1)
	CAN_data[2].append(42)
	CAN_data[3].append("0x1234567812345678")

	refreshrate = 2

	print 'Calling write_CAN_message'
	write_CAN_message(CAN_data, 0, 0)
	
	#Refresh
	print 'Sleep'
	time.sleep(refreshrate)
	
	print 'Refresh'
	driver.refresh()

if __name__ == "__main__":
    main()
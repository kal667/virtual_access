#!/usr/local/bin/python

"""This is a test program for write functionality"""

from openxc.interface import UsbVehicleInterface
import time

def init_VI():
	"""Initializes VI with JSON formatting"""

	print 'Setting VI'
	vi = UsbVehicleInterface(payload_format="json")

	return vi

def write_CAN_message(vi):
	#This writes a low-level CAN message to the bus

	print 'Writing to CAN'
	vi.write(bus=1, id=0x201, data="0x0000000080100000")

	return

def main():

	refreshrate = 2

	vi = init_VI()

	while True:

		print 'Calling write_CAN_message'
		write_CAN_message(vi)
		
		#Refresh
		print 'Sleep'
		time.sleep(refreshrate)
	

if __name__ == "__main__":
   	main()
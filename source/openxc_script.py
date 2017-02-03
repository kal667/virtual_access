from openxc.interface import UsbVehicleInterface
from datetime import datetime
from openxc.formats.base import VehicleMessageStreamer
from openxc.formats.binary import ProtobufStreamer, ProtobufFormatter
from openxc.formats.json import JsonStreamer, JsonFormatter
import calendar
import json

def write_CAN_message(CAN_data, base_CAN_timestamp, start_program_timestamp):
    """This writes a low-level CAN message to the bus"""
    
    vi = UsbVehicleInterface()

	#Set passthrough and format parameters
    '''vi.set_passthrough(1, True)
    vi.set_passthrough(2, True)'''

    while len(CAN_data[0]) != 0:
		
		#Get current timestamp for comparison
		current_timestamp = datetime.utcnow()
		current_timestamp = calendar.timegm(current_timestamp.utctimetuple())
		
		print 'Current Program Timestamp = ', current_timestamp
		
		#Note: must divide OpenXC timestamp by 1000 because it includes ms
		#Note: May have to switch data from unicode to string
		if (current_timestamp - start_program_timestamp) > ((CAN_data[0][0] - base_CAN_timestamp)/1000):
			#TODO: Continue trying to write until successful 
			vi.set_payload_format(json)
			vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0], frame_format = 'standard')
			CAN_data[0].pop(0)
			CAN_data[1].pop(0)
			CAN_data[2].pop(0)
			CAN_data[3].pop(0)
			
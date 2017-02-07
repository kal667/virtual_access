from openxc.interface import UsbVehicleInterface
from datetime import datetime
import calendar

def init_VI():
	"""Initializes VI with JSON formatting"""

	print 'Setting VI'
	vi = UsbVehicleInterface(payload_format="json")

	return vi


def write_CAN_message(vi, CAN_data, base_CAN_timestamp, start_program_timestamp):
    """This writes a low-level CAN message to the bus"""

    while len(CAN_data[0]) != 0:
		
		#Get current timestamp for comparison
		current_timestamp = datetime.utcnow()
		current_timestamp = calendar.timegm(current_timestamp.utctimetuple())
				
		#Note: must divide OpenXC timestamp by 1000 because it includes ms
		#Note: May have to switch data from unicode to string
		if (current_timestamp - start_program_timestamp) > ((CAN_data[0][0] - base_CAN_timestamp)/1000):
			#TODO: Continue trying to write until successful 
			vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0])
			CAN_data[0].pop(0)
			CAN_data[1].pop(0)
			CAN_data[2].pop(0)
			CAN_data[3].pop(0)
			
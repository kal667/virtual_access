from openxc.interface import UsbVehicleInterface
from datetime import datetime
import calendar

def write_CAN_message(CAN_data, base_CAN_timestamp, start_program_timestamp):
    # this writes a low-level CAN message to the bus
    
    vi = UsbVehicleInterface()

    while len(CAN_data[0]) != 0:
		#Get current timestamp for comparison
		current_timestamp = datetime.utcnow()
		current_timestamp = calendar.timegm(current_timestamp.utctimetuple())
		print 'Current Program Timestamp = ', current_timestamp
		#Note: must divide OpenXC timestamp by 1000 because it includes ms
		#
		#TODO: Fix the left side of the inequality. Basetimestamp should be replaced by a timestamp taken at the start of the program
		#
		if (current_timestamp - start_program_timestamp) > ((CAN_data[0][0] - base_CAN_timestamp)/1000):
			#TODO: Continue trying to write until successful 
			vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0])
			CAN_data[0].pop(0)
			CAN_data[1].pop(0)
			CAN_data[2].pop(0)
			CAN_data[3].pop(0)
			
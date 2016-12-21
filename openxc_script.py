from openxc.interface import UsbVehicleInterface
from datetime import datetime
import calendar

def write_CAN_message(CAN_data, base_timestamp):
    # this writes a low-level CAN message to the bus
    
    vi = UsbVehicleInterface()

    while len(CAN_data[0]) != 0:
		#Get current timestamp for comparison
		current_timestamp = datetime.utcnow()
		current_timestamp = calendar.timegm(current_timestamp.utctimetuple())
		#Note: must divide OpenXC timestamp by 1000 because it includes ms
		if (current_timestamp - base_timestamp/1000) > ((CAN_data[0][0] - base_timestamp)/1000):
			vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0])
			CAN_data[0].pop(0)
			CAN_data[1].pop(0)
			CAN_data[2].pop(0)
			CAN_data[3].pop(0)
			
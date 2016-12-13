from openxc.interface import UsbVehicleInterface

def write_CAN_message(CAN_data, base_timestamp):
    # this writes a low-level CAN message to the bus
    while len(CAN_data[0]) != 0:
		current_time = datetime.utcnow()
		current_time = calendar.timegm(current_time.utctimetuple())
		#Note: must divide OpenXC timestamp by 1000 because it includes ms
		if (current_time - base_time) > ((CAN_data[0][0] - base_timestamp)/1000):
			vi.write(bus=CAN_data[1][0], id=CAN_data[2][0], data=CAN_data[3][0])
			CAN_data[0].pop(0)
			CAN_data[1].pop(0)
			CAN_data[2].pop(0)
			CAN_data[3].pop(0)
			
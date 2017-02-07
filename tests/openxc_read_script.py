from openxc.interface import UsbVehicleInterface

def receive(message, **kwargs):
    # this callback will receive each message received as a dict
    print(message['data'])

vi = UsbVehicleInterface(callback=receive)
print "start"
vi.start()
# This will block until the connection dies or you exit the program
print "join"
vi.join()
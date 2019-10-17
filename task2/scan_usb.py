import serial

port_name = "/dev/ttyUSB0"
buffer_ = b""


def check_buffer(byte_data):
    searching = "www.google.com"
    if len(byte_data) < len(searching):
        return byte_data
    if searching in byte_data.decode("UTF-8"):
        print(searching)
        byte_data = b""
    return byte_data


try:
    print(f"Start scanning {port_name}")
    usb2serial_port = serial.Serial(port_name)
    while True:
        new_byte = usb2serial_port.read()
        buffer_ += new_byte
        buffer_ = check_buffer(buffer_)
except KeyboardInterrupt as e:
    print("Ctrl-C pressed")
    print("Bye!")
#except Exception as e:
#    print(e)
#finally:
#    print("Bye!")

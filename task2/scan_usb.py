import serial
import re
import traceback

port_name = "/dev/ttyUSB0"
buffer_ = b""
usb2serial_port = None


def check_buffer(byte_data):
    searching = r"www\.google\.com\/v2\/[a-zA-Z0-9]+\/w\?d=(-?[0-9]+,){10}(-?[0-9]+)"
    if len(byte_data) < len(searching):
        return byte_data
    m = re.search(searching, byte_data.decode("UTF-8"))
    if m:
        print(m.group())    # bingo!
        return b""
    if len(byte_data) >= 200:
        return b""
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
except Exception as e:
    traceback.print_exc()
finally:
    if usb2serial_port is not None:
        usb2serial_port.close()
    print("Bye!")

import serial

port_name = "/dev/ttyUSB0"

try:
    print(f"Start scanning {port_name}")
    usb2serial_port = serial.Serial(port_name)
    while True:
        raw = usb2serial_port.read()
        print(raw)
except KeyboardInterrupt as e:
    print("Ctrl-C pressed")
except Exception as e:
    print(e)
finally:
    print("Bye!")

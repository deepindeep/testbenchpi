import serial


try:
    usb2serial_port = serial.Serial('/dev/ttyUSB0')
    while True:
        raw = usb2serial_port.read()
        print(raw)
except KeyboardInterrupt as e:
    print("Ctrl-C pressed")
except Exception as e:
    print(e)
finally:
    print("Bye!")

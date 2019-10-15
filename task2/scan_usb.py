import pyshark

capture = pyshark.LiveCapture(interface='/dev/usbmon2')
capture.sniff(timeout=50)

print(capture)

for packet in capture.sniff_continuously(packet_count=5):
    print(packet)

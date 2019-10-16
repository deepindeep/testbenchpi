import nmap
from pprint import pprint
import time

try:
    nm = nmap.PortScanner()
    result = None
    while True:
        tmp = nm.scan(hosts='192.168.4.0/24', arguments='--exclude 192.168.4.1')
        # print(tmp)
        if result == tmp['scan']:
            print("Nothing new")
            continue
        print("Network changed!")
        result = tmp['scan']
        pprint(result)
        time.sleep(1)
except KeyboardInterrupt as c:
    print("Ctrl-C pressed")
except Exception as e:
    print(e)
finally:
    print("Bye!")

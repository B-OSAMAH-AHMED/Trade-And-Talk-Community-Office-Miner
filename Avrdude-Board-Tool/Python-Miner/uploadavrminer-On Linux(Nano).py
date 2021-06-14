import os
import sys
port = input("Enter The Port Where The Arduino Nano Board Is: ")
def linux():
    os.system(f"avrdude -c arduino -P {port} -p m328p -b 57600 -U flash:w:avrdude-Algorithm-sha256-nano.hex")
    print("Done!")
    exit()
linux()

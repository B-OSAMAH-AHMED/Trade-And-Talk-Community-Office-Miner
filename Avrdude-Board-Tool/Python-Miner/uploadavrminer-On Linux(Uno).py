import os
import sys
port = input("Enter The Port Where The Arduino Uno Board Is: ")
def linux():
    os.system(f"avrdude -c arduino -P {port} -p m328p -b 115200 flash:w:avrdude-Algorithm-sha256-uno.hex")
    print("Done!")
    exit()
linux()

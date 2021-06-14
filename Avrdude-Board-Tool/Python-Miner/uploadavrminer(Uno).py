import os
import sys
port = input("Enter The Port Where The Arduino Uno Board Is: ")
def windows():
        os.system(f".\\avrdude\\avrdude.exe -c arduino -P {port} -p m328p -b 115200 -U flash:w:avrdude-Algorithm-sha256-uno.hex")
        print("Done!")
        exit()
if sys.platform == "win32":
    windows()

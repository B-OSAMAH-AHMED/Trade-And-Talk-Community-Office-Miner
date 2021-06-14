import os
import sys
port = input("Enter the port where the Arduino Nano board is: ")
def windows():
    os.system(f".\\avrdude\\avrdude.exe -c arduino -P {port} -p m328p -b 57600 -U flash:w:avrdude-Algorithm-sha256-nano.hex")
    print("Done!")
    exit()
windows()


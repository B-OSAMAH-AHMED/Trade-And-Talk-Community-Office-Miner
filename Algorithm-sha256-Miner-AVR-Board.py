#!/usr/bin/env python3
##########################################
# Algorithm-sha256-Miner-AVR-Board (v0.0.1)
# https://github.com/thecode3/Algorithm-sha256-Miner-AVR-Board
# Distributed BSD 3-Clause LicenseSourcegraph version: 89375_2021-03-05_d646a50
# Office Trade And Talk Community 2021.
##########################################
import socket, threading, time, re, subprocess, configparser, sys, datetime, os  # Import libraries
from pathlib import Path
from signal import signal, SIGINT
import locale, json


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    os.execl(sys.executable, sys.executable, *sys.argv)
    
    
def now():
  return datetime.datetime.now()
  
  
  try:  # Check if pyserial is installed
    import serial
    import serial.tools.list_ports
    except:
      print(
        now().strftime("%H:%M:%S ")
      + 'Pyserial is not installed. Miner will try to install it. If it fails, please manually install "pyserial" python3 package.\nIf you can\'t install it, use the Minimal-PC_Miner.'
    )
    install("pyserial")
    
try:  # Check if colorama is installed
      from colorama import init, Fore, Back, Style
except:
    print(
        now().strftime("%H:%M:%S ")
        + 'Colorama is not installed. Miner will try to install it. If it fails, please manually install "colorama" python3 package.\nIf you can\'t install it, use the Minimal-PC_Miner.'
    )
    install("colorama")

try:  # Check if requests is installed
    import requests
except:
    print(
        now().strftime("%H:%M:%S ")
        + 'Requests is not installed. Miner will try to install it. If it fails, please manually install "requests" python3 package.\nIf you can\'t install it, use the Minimal-PC_Miner.'
    )
    install("requests")

try:
    from pypresence import Presence
except:
    print(
        'Pypresence is not installed. Wallet will try to install it. If it fails, please manually install "pypresence" python3 package.'
    )
    install("pypresence")

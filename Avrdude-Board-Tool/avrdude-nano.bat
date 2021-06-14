avrdude -p m328p -C avrdude.conf -c arduino -b 57600 -P com6 -U flash:r:avrdude-database-Files.hex:i

pause
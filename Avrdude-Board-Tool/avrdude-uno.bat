avrdude -p m328p -C avrdude.conf -c arduino -b 115200 -P com9 -U flash:r:avrdude-database-Files.hex:i

pause
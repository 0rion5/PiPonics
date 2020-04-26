#!/usr/bin/env python 3

# Copyright (c) 2020 PiPonics, Inc.
# Author: 0rion5 B3lt

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime as dt
import logging
import logging.handlers
from time import sleep
from os import system
import serial

class PiPonics:

    def __init__(self, log_file, max_bytes, backup_count, valve_one_time, valve_two_time, wait_time, cycle_count, pins):

        self.log_file = log_file                                            # set log file attribute
        self.max_bytes = max_bytes                                          # set max bytes attribute
        self.backup_count = backup_count                                    # set backup count attribute
        self.valve_one_time = valve_one_time                                # set valve one attribute
        self.valve_two_time = valve_two_time                                # set valve two attribute
        self.wait_time = wait_time                                          # set wait time attribute
        self.cycle_count = cycle_count                                      # set cycle count attribute
        self.pins = pins                                                    # set the pins to be used

        for i in self.pins:
            system('gpio -1 mode '+str(i)+' out')                           # Execute the command (a string) in a subshell

    @property
    def time(self):
        return dt.datetime.now().strftime(' %Y-%m-%d %I:%M:%S %p ')         # a string representing the date and time
    
    @property
    def soil_moisture_sensor(self):
        #ser = serial.Serial('/dev/ttyACM0', 9600)
        serial_read = str(serial.Serial('/dev/ttyACM0', 9600).readline()).replace("b'","").replace("\\r\\n'","")
        return serial_read
    
    def start_logger(self, file_name, max_bytes, backup_count):                                                                        
        logger = logging.getLogger(__name__)                                # return logger of the current module
        logger.setLevel(logging.INFO)                                       # set the logging level of this logger                                                                            
        handler = logging.handlers.RotatingFileHandler(
            file_name, 'w', max_bytes, backup_count)                        # The specified file is opened and used as the stream for logging.
        handler.setLevel(logging.INFO)                                      # set the logging level for this handler                                                                         
        formatter = logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s')                       # create formatter and add it to the handlers
        handler.setFormatter(formatter)                                     # set the Formatter for this handler                                                                  
        logger.addHandler(handler)                                          # adds the Specified handler to this logger

        return logger                                                       # return logger

    def valve_one_open(self):                                               # valve one open
        for i in self.pins[0::2]:                                           # for pins[0] and pins[2]
            system('gpio -1 write '+str(i)+' 1')                            # write gpio pins[i] on
            print('Valve one opened')                                       # print to terminal

    def valve_one_closed(self):                                             # valve one closed                                                         
        for i in self.pins[0::2]:                                           # for pins[0] and pins[2]
            system('gpio -1 write '+str(i)+' 0')                            # write gpio pins[i] off 
            print('Valve one closed')                                       # print to terminal

    def valve_two_open(self):                                               # valve two open
        for i in self.pins[1::1]:                                           # for pins[0] and pins[1]   
            system('gpio -1 write '+str(i)+' 1')                            # write gpio pins[i] on
            print('Valve two opened')                                       # print to terminal

    def valve_two_closed(self):                                             # valve two closed
        for i in self.pins[1::1]:                                           # for pins[0] and pins[1]
            system('gpio -1 write '+str(i)+' 0')                            # write gpio pins[i] off
            print('Valve two closed')                                       # print to terminal

    def watering_cycle(self):
        logger = self.start_logger(
            self.log_file, self.max_bytes, self.backup_count)               # Create logging instance

        for i in range(1, self.cycle_count+1):
                                                                            # Cycle Start
            print('Cycle: '+str(i))                                         # Print Cycle Count
            logger.info(self.time + ' Starting Cycle ' + str(i))            # Log Cycle Count
            
            logger.info(self.time + ' Valve One Opened')
            logger.info(self.time + ' ' + self.soil_moisture_sensor)                   # Log Valve One Opened
            self.valve_one_open()                                           # OPEN VALVE ONE HERE
            
            sleep(self.valve_one_time*60)                                   # Valve One Timer
            
            logger.info(self.time + ' Valve One Closed')                    # Log Valve One Closed
            self.valve_one_closed()                                         # CLOSE VALVE ONE HERE
            
            sleep(self.wait_time*60)                                        # Wait For Growbed to Drain
            
            logger.info(self.time + ' Valve Two Opened')                    # Log Valve Two Opened
            self.valve_two_open()                                           # OPEN VALVE TWO HERE
            
            sleep(self.valve_two_time*60)                                   # Valve Two Timer
            
            logger.info(self.time + ' Valve Two Closed')                    # Log Valve Two Closed
            self.valve_two_closed()                                         # CLOSE VALVE TWO HERE
            
            sleep(self.wait_time*60)                                        # Wait For Growbed To Drain
            
            print("Done\n")                                                 # Print Cycle Is Done
            logger.info(self.time + ' Cycle ' + str(i) + ' Complete\n')     # Log Cycle Complete


if __name__ == "__main__":
    log_file       = '/home/pi/Documents/projects/PiPonics/logs/PiPonics.log'                                   # log file directory
    max_bytes      = 500000                                                 # max bytes
    backup_count   = 5                                                      # backup count
    valve_one_time = 0.05                                                    # valve one minutes
    valve_two_time = 0.05                                                    # valve two minutes
    wait_time      = 0.05                                                    # wait time minutes
    cycle_count    = 9999                                                   # cycle count 
    pins           = [36, 38, 40]                                           # gpio pins physical pin numbering
    
    ponics         = PiPonics(log_file, max_bytes, backup_count,
                      valve_one_time, valve_two_time, wait_time, cycle_count,
                              pins)
    try:                          
        #ponics.watering_cycle()
        soil_data_list = []
        print(ponics.time)
        for i in range(0,1000):
            soil_data_list.append(ponics.soil_moisture_sensor)
            print(ponics.soil_moisture_sensor)
            sleep(0.1)
    except KeyboardInterrupt:
        for i in ponics.pins:
            system('gpio -1 write '+str(i)+' 0')
            print('not water cycling')

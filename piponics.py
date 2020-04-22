
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


class PiPonics:

    def __init__(self, log_file, max_bytes, backup_count, valve_one_time, valve_two_time, wait_time, cycle_count, pins):

        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.valve_one_time = valve_one_time
        self.valve_two_time = valve_two_time
        self.wait_time = wait_time
        self.cycle_count = cycle_count
        self.pins = pins

        for i in self.pins:
            system('gpio -1 mode '+str(i)+' out')

    @property
    def time(self):
        return dt.datetime.now().strftime(' %Y-%m-%d %I:%M:%S %p ')

    def start_logger(self, file_name, max_bytes, backup_count):

        # Create instance logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # create file handler which logs even debug messages
        handler = logging.handlers.RotatingFileHandler(
            file_name, 'w', max_bytes, backup_count)
        handler.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(handler)

        return logger

    def valve_one_open(self):
        for i in self.pins[0::2]:
            system('gpio -1 write '+str(i)+' 1')
            print('Valve one opened')

    def valve_one_closed(self):
        for i in self.pins[0::2]:
            system('gpio -1 write '+str(i)+' 0')
            print('Valve one closed')

    def valve_two_open(self):
        for i in self.pins[1::1]:
            system('gpio -1 write '+str(i)+' 1')
            print('Valve two opened')

    def valve_two_closed(self):
        for i in self.pins[1::1]:
            system('gpio -1 write '+str(i)+' 0')
            print('Valve two closed')

    def watering_cycle(self):

        logger = self.start_logger(
            self.log_file, self.max_bytes, self.backup_count)

        for i in range(1, self.cycle_count+1):
                                                                            # Cycle Start
            print('Cycle: '+str(i))                                         # Print Cycle Count
            logger.info(self.time + ' Starting Cycle ' + str(i))            # Log Cycle Count

                                                                            # Valve One Cycle Start
            logger.info(self.time + ' Valve One Opened')                    # Log Valve One Opened
            self.valve_one_open()                                           # OPEN VALVE ONE HERE            

                                                                            # Hold Valve One Open
            sleep(self.valve_one_time*60)                                   # Valve One Timer
                                                                            # Valve One Cycle End

            logger.info(self.time + ' Valve One Closed')                    # Log Valve One Closed
            self.valve_one_closed()                                         # CLOSE VALVE ONE HERE

                                                                            # Wait Period
            sleep(self.wait_time*60)                                        # Wait For Growbed to Drain

                                                                            # Valve Two Cycle
            logger.info(self.time + ' Valve Two Open')                      # Log Valve Two Opened
            self.valve_two_open()                                           # OPEN VALVE TWO HERE            

                                                                            # Hold Valve Two Open
            sleep(self.valve_two_time*60)                                   # Valve Two Timer

                                                                            # Valve Two Cycle End
            logger.info(self.time + ' Valve Two Closed')                    # Log Valve Two Closed
            self.valve_two_closed()                                         # CLOSE VALVE TWO HERE            

                                                                            # Wait Period
            sleep(self.wait_time*60)                                        # Wait For Growbed To Drain
            
                                                                            # Cycle End
            print("Done\n")                                                 # Print Cycle Is Done
            logger.info(self.time + ' Cycle ' + str(i) + ' Complete\n')     # Log Cycle Complete


if __name__ == "__main__":
    log_file       = '/home/pi/PiPonics/logs/PiPonics.log'  # log file directory
    max_bytes      = 500000                                 # max bytes
    backup_count   = 50                                     # backup count
    valve_one_time = 0.01                                    # valve one minutes
    valve_two_time = 0.01                                    # valve two minutes
    wait_time      = 0.01                                    # wait time minutes
    cycle_count    = 5                                  # cycle count 
    pins           = [36, 38, 40]                           # gpio pins physical pin numbering
    
    ponics         = PiPonics(log_file, max_bytes, backup_count,
                      valve_one_time, valve_two_time, wait_time, cycle_count, pins)
    ponics.watering_cycle()

#!/usr/bin/env python 3

# Copyright (c) 2019 PiPonics, Inc.
# Author: Dallas Kappel

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

import RPi.GPIO as GPIO
import datetime, time, math, logging
import logging.handlers
from time import sleep


class PiPonics():

    '''

    DOCSTRING: Makes ease of some simple tasks. Watering plants can be tedious and often a forgotten task. With PiPonics you set it and forget it.
    Automating the task of watering your plants.
    The commands are simple and as follows;

    1. PiPonics.default_pin_setup() " Uses predetermined pins.
    Physiscal pin numbering scheme and sets up the RPi.GPIO library to work."

    2. PiPonics.default_timing_setup() " Uses predetermined timing and near infinite cycles.
    Great for after your set up is dialed in and you know the timing for your pump and watering setup."

    3. PiPonics.default_setup() " Uses PiPonics.default_pin_setup(), and PiPonics.default_timing_setup().
    Used primarily when importing main_piponics.py into another module.

    4. PiPonics.custom_pin_setup() " Uses a custom number of pins.
    Be careful here, I haven't coded any protections in to only choose available pins.Great for testing and modifying if the need arises.

    5. PiPonics.custom_timing_setup() - " Uses custom timing set by the user.
    Generally used for testing.
    Once the system is dialed in then the PiPonics.default_timing_setup() can be modified for the users particular use case.
    This function only needs to be ran at the beggining or each time program runs."

    6. PiPonics.custom_setup() - "Mainly for testing.
    Combines PiPonics.custom_pin_setup(), and PiPonics.custom_timing_setup().
    This only needs to be run at startup or eachtime the program is run."

    7. PiPonics.main() - " Runs the watering_cycle(*args).
    Mainly used when importing the module into another module.
    Uses parameters speciefied when the first six functions run.
    If the watering_cycle function is called by another module the paramerters must be met.
    Running PiPonics.main() without first running the pin setup or timing set up will break it and it will not work."

    8. PiPonics.destroy() - " Kills the GPIO and cleans up.
    Allthough I have found while the program sleeps the KeyboardInterrupt does not respond.
    Perhaps a bug that I will work out later.
    If you have an idea fork this repository and share the proposed change with me!!"

    9. watering_cycle(valveone_time,wait_time,valvetwo_time,pause_time,cycle_count) - " Loops through the cycle_count.
    This is not my own code.
    Credits Matthew Hajda, original code @ https://github.com/mhajda/PiPonics."

    10. start_logger(filename, maxBytes, backupCount) - " Creates a logger to record the watering_cycle(*args) events.
    This could be used later on to update a web app of the Aquaponics status."
    
    11. PiPonics.pump_on() - "Turns the pump on. Sets the GPIO.output(PINS[0], True)"
    
    12. PiPonics.pump_off() - "Turns the pump on. Sets the GPIO.output(PINS[0], False)"

    13. PiPonics.open_valve_one() - "Opens the Valve. Sets the GPIO.output(PINS[1], True)"

    14. PiPonics.close_valve_one() - "Closes the Valve. Sets the GPIO.output(PINS[1], False)"

    15. PiPonics.open_valve_two() - "Opens the Valve. Sets the GPIO.output(PINS[2], True)"

    16. PiPonics.close_valve_two() - "Closes the Valve. Sets the GPIO.output(PINS[2], False)"
    
    '''
    

    def __init__(self):
        
        self.PiPonics = PiPonics

#*********************************************************************************************************************************************************
# //\\//ONLY EDIT THE SECTION BELOW\\//\\//\\//ONLY EDIT THE SECTION BELOW\\//\\//\\//ONLY EDIT THE SECTION BELOW\\//\\//\\//ONLY EDIT THE SECTION BELOW       
#*********************************************************************************************************************************************************

    def default_pin_setup():

        '''

    1. PiPonics.default_pin_setup() " Uses predetermined pins.
    Physiscal pin numbering scheme and sets up the RPi.GPIO library to work."
    
        **ONLY EDIT PINS LIST VALUES**
        CHANGING ANY OTHER CODE MIGHT BREAK IT

        PINS = [pump,valveone,valvetwo]

        PINS[0] = pump
        PINS[1] = valveone
        PINS[2] = valvetwo

        '''

        global PINS

        PINS = [36,38,40] # CHANGE [#,#,#] IF NEEDED

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PINS, GPIO.OUT)
        GPIO.output(PINS, False)

        return PINS


    def default_timing_setup():
        
        '''

    2. PiPonics.default_timing_setup() " Uses predetermined timing and near infinite cycles.
    Great for after your set up is dialed in and you know the timing for your pump and watering setup."

    
        **ONLY EDIT THE FUNCTION VARIABLE NUMBERS.
        CHANGING A VARIABLE NAME WILL BREAK THE CODE

        TIMING_INPUT = [valve_one_time, wait_time, valve_two_time, pause_time, cycle_count]
        
        TIMING_INPUT[0] = valve_one_time
        TIMING_INPUT[1] = valve_two_time
        TIMING_INPUT[2] = wait_time
        TIMING_INPUT[3] = pause_time
        TIMING_INPUT[4] = cycle_count        

        '''

        global TIMING_INPUT

        valve_one_time = .5
        valve_two_time = .5
        wait_time = .5
        pause_time = .5
        cycle_count = 99999999

        TIMING_INPUT = [valve_one_time, wait_time, valve_two_time, pause_time, cycle_count]

        return TIMING_INPUT


#*********************************************************************************************************************************************************
# //\\//ONLY EDIT THE SECTION ABOVE\\//\\//\\//ONLY EDIT THE SECTION ABOVE\\//\\//\\//ONLY EDIT THE SECTION ABOVE\\//\\//\\//ONLY EDIT THE SECTION ABOVE       
#*********************************************************************************************************************************************************


    def default_setup():

        '''

    3. PiPonics.default_setup() " Uses PiPonics.default_pin_setup(), and PiPonics.default_timing_setup().
    Used primarily when importing main_piponics.py into another module.
    
        '''

        PiPonics.default_pin_setup()
        PiPonics.default_timing_setup()
        logger = PiPonics.start_logger('/home/pi/Aquaponics/PiPonics/logs/PiPonics.log', 5000000, 5)
        logger.info(' Logger Started...')
        logger.info(datetime.datetime.now().strftime(' %Y-%m-%d %I:%M:%S %p') + ' Script Started with default settings.' )
        sleep(1)


    def custom_pin_setup():

        '''

    4. PiPonics.custom_pin_setup() " Uses a custom number of pins.
    Be careful here, I haven't coded any protections in to only choose available pins.Great for testing and modifying if the need arises.

        '''
        
        global PINS
        print('GPIO.BOARD mode is used for this project.\nUse a Physical pin number.\n')
        pump = int(input('Choose a pin for the pump:'))
        valve_one = int(input('Choose a pin for valve one: '))
        valve_two = int(input('Choose a pin for valve two: '))
        PINS = [pump, valve_one, valve_two]                        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PINS, GPIO.OUT)
        GPIO.output(PINS, False)
        return PINS


    def custom_timing_setup():

        '''

    5. PiPonics.custom_timing_setup() - " Uses custom timing set by the user.
    Generally used for testing.
    Once the system is dialed in then the PiPonics.default_timing_setup() can be modified for the users particular use case.
    This function only needs to be ran at the beggining or each time program runs."

 
        ''' 

        global TIMING_INPUT

        valve_one_time = float ( input ( 'Minutes to hold valve one open: ') ) 
        wait_time = float ( input ( 'Mintues to wait between cycles: ') )
        valve_two_time = float ( input ( 'Minutes to hold valve two open: ') ) 
        pause_time = float ( input ( 'Mintues to wait between cycles: ') )
        cycle_count = int ( input ( 'How many cycles?: ' ) )

        TIMING_INPUT = [valve_one_time, wait_time, valve_two_time, pause_time, cycle_count]

        return TIMING_INPUT


    def custom_setup():

        '''

    6. PiPonics.custom_setup() - "Mainly for testing.
    Combines PiPonics.custom_pin_setup(), and PiPonics.custom_timing_setup().
    This only needs to be run at startup or eachtime the program is run."

        '''

        PiPonics.custom_pin_setup()
        PiPonics.custom_timing_setup()
        logger = PiPonics.start_logger('/home/pi/Aquaponics/PiPonics/logs/PiPonics.log', 5000, 5)
        logger.info(' Logger Started...')
        logger.info(datetime.datetime.now().strftime(' %Y-%m-%d %I:%M:%S %p') + ' Script Started with custom settings.' )
        sleep(1)


    def main():

        '''

    7. PiPonics.main() - " Runs the watering_cycle(*args).
    Mainly used when importing the module into another module.
    Uses parameters speciefied when the first six functions run.
    If the watering_cycle function is called by another module the paramerters must be met.
    Running PiPonics.main() without first running the pin setup or timing set up will break it and it will not work."

        '''

        PiPonics.watering_cycle(TIMING_INPUT[0],TIMING_INPUT[1],TIMING_INPUT[2],TIMING_INPUT[3],TIMING_INPUT[4]) 


    def destroy():

        '''

    8. PiPonics.destroy() - " Kills the GPIO and cleans up.
    Allthough I have found while the program sleeps the KeyboardInterrupt does not respond.
    Perhaps a bug that I will work out later.
    If you have an idea fork this repository and share the proposed change with me!!"

        '''

        GPIO.output(PINS, False)
        GPIO.cleanup()

    def watering_cycle(valveone_time,wait_time,valvetwo_time,pause_time,cycle_count):

        '''

    9. watering_cycle(valveone_time,wait_time,valvetwo_time,pause_time,cycle_count) - " Loops through the cycle_count.
    This is not my own code.
    Credits Matthew Hajda, original code @ https://github.com/mhajda/PiPonics."

        '''

        if cycle_count == 0:
            cycle_count=999
        
        for i in range(1,cycle_count): ## Run loop numTimes
            
            print('Cycle: ',i)
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Cycle ' + str(i) + ' Initiated ' )
            ## Valve One Cycle
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Valve One Open ' )
            print('Valve One Cycle Begin')
            PiPonics.open_valve_one()#opens valve
            PiPonics.pump_on()#Turns pump on

            #Hold Valve Open
            sleep(valveone_time*60) ## valve  timer

            print('Valve One Cycle End')
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Valve One Closed ' )
            PiPonics.pump_off()#Turns pump off
            PiPonics.close_valve_one() #Closes Valve

            ## Wait Period
            sleep(wait_time*60) # Wait For Growbed to Drain

            ## Valve Two Cycle
            print('Valve Two Cycle Begin')
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Valve Two Open ' )
            PiPonics.open_valve_two()
            PiPonics.pump_on()#Turns pump on  #Opens Valve
            
            #Hold Valve Two open
            sleep(valvetwo_time*60) ## Valve Two Timer

            print( 'Valve Two Cycle End' )
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Valve Two Closed ' )
            PiPonics.close_valve_two() #Closes Valve
            PiPonics.pump_off()#Turns pump off

            sleep(pause_time*60) ## Wait Cycle to start again
            print( "Done" ) ## When loop is complete, print "Done"
            logger.info(datetime.datetime.now().strftime( ' %Y-%m-%d %I:%M:%S %p ' ) + ' Cycle ' + str(i) + ' Completed ' )


    def start_logger(filename, maxBytes, backupCount):

        '''

    10. start_logger(filename, maxBytes, backupCount) - " Creates a logger to record the watering_cycle(*args) events.
    This could be used later on to update a web app of the Aquaponics status."

        '''

        global logger

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # create file handler which logs even debug messages
        handler = logging.handlers.RotatingFileHandler(filename, 'w', maxBytes, backupCount)
        handler.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter( '%(levelname)s - %(name)s - %(message)s' )
        handler.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(handler)
        logger.info(' Starting Logger....')

        return logger

    def pump_on():

        '''

    11. PiPonics.pump_on() - "Turns the pump on. Sets the GPIO.output(PINS[0], True)"

        '''

        GPIO.output(PINS[0], True)


    def pump_off():

        '''
    
    12. PiPonics.pump_off() - "Turns the pump on. Sets the GPIO.output(PINS[0], False)"

        '''

        GPIO.output(PINS[0], False)


    def open_valve_one():

        '''

    13. PiPonics.open_valve_one() - "Opens the Valve. Sets the GPIO.output(PINS[1], True)"

        '''

        GPIO.output(PINS[1], True)


    def close_valve_one():

        '''

    14. PiPonics.close_valve_one() - "Closes the Valve. Sets the GPIO.output(PINS[1], False)"

        '''

        GPIO.output(PINS[1], False)


    def open_valve_two():

        '''

    15. PiPonics.open_valve_two() - "Opens the Valve. Sets the GPIO.output(PINS[2], True)"

        ''' 

        GPIO.output(PINS[2], True)

    def close_valve_two():

        '''

    16. PiPonics.close_valve_two() - "Closes the Valve. Sets the GPIO.output(PINS[2], False)"

        '''

        GPIO.output(PINS[2], False)
    





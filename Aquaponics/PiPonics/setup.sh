#!/bin/bash


if [ -d "/home/pi/Documents/testfolder/" ] 
then
    cd /home/pi/Documents/testfolder
    echo "Directory /path/to/dir exists."
     
else
    echo "Error: Directory /home/pi/Documents/testfolder does not exists."
    sleep 1
    echo "Correcting Error...."
    mkdir /home/pi/Documents/testfolder
    sleep 1
    echo "Growing Solution"
    . . cd /home/pi/Documents/testfolder
    sleep 1
    echo "Error Corrected"
fi


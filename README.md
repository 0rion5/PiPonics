# PiPonics
<!DOCTYPE html>
<html>
    <head>
        <h1>Aquaponics W/ Raspberry Pi 3/4</h1>
    </head>
    <body>
        <h2>Table of Contents</h2>
        <ul>
            <li><a href="#section1">Installation</a></h2>
            <li><a href="#section2">Usage</a></h2>
            <li><a href="#section3">Hardware Setup</a></h2>
        </ul>
        <h2 id="Section1">Installation</h2>
        <p>
            <ul>
                <li>open terminal and navigate to /home/pi/</li>
                <li>git clone https://github.com/0rion5/PiPonics.git</li>
            </ul>
        </p>
        <h2 id="Section2">Usage</h2>
        <p>
           <ul>
               <li>sudo nano /etc/rc.local</li>
               <li>add this line above exit 0 "python3 /home/pi/PiPonics/piponics.py"</li>
               <li>ctrl-x and yes then enter</li>
               <li>sudo reboot</li>     
               <li>Your Done!!</li>
           </ul>
        </p>
        <h2 id="Hardware Setup">Section 3</h2>
        <p>
            Coming Soon!
        </p>
    </body>
</html>

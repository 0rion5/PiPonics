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
                <li>sudo apt-get update && sudo apt-get -y upgrade</li>
                <li>git clone https://github.com/0rion5/PiPonics.git</li>
            </ul>
        </p>
        <h2 id="Section2">Usage</h2>
        <p>
           <ul>
               <li>sudo nano /etc/rc.local</li>
               <li>add this line above exit 0 "python3 /home/pi/PiPonics/piponics.py"</li>
               <li>sudo reboot</li>     
               <li>Your Done!!</li>
           </ul>
        </p>
        <h2 id="Section3">Hardware Setup</h2>
        <p>
            For this project I used a raspberry pi 3b. However, any pi should work the same. I also used a saintsmart 8 channel relay.               Connect the relay to the gpio headers using physical pin numbering as follows;
            <table>
                <tr>
                    <th>VCC</th>
                    <th>in1</th>
                    <th>in2</th>
                    <th>in3</th>
                    <th>GND</th>
                </tr>
                <tr>
                    <td>5v</td>
                    <td>36</td>
                    <td>38</td>
                    <td>40</td>
                    <td>GN</td>
                </tr>
            </table>
            <p>
                <h3>Raspberry Pi 3b pinout</h3>
                <img src="https://i.pinimg.com/originals/84/46/ec/8446eca5728ebbfa85882e8e16af8507.png" width = "50%">
            </p>
            <p>
                <h3>Sainsmart 8 Channel Relay<h3/>
                    <img src = "https://cdn.shopify.com/s/files/1/1978/9859/products/09_12_1024x1024.jpg?v=1502520966" width = "50%">
            </p>
        </p>
    </body>
</html>

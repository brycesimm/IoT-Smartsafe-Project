# IoT-Smartsafe-Project

This repository holds all of the documentation of my final project for Introduction to Internet of Things in which I and my partner developed a "Smartsafe" using a Raspberry Pi 4B 8GB, various sensors, a breadboard, Twilio, a cardboard box, and various Python libraries. Included are: a report explaining the project in greater detail, pictures of the project lifecycle, and a video demonstration using the Smartsafe.

Obviously, this Smartsafe wouldn't keep any real intruder out; the objective was to use a variety of sensors and actuators to create a multi-functional IoT device with all of the knowledge gained throughout the course. 

This project includes: HC-SR501 Motion Sensor, Keypad, Photoresistor Light Sensor, SG90 Servo Motor, and a I2C LCD 1602 screen. 
Each of these items were connected to the GPIO pins on the Raspberry Pi and controlled via the 3 Python files found in this repository.

This project demonstrates the lifecycle of creating an IoT device from scratch, which requires basic electrical engineering knowledge (such as Ohm's Law) to connect components correctly with the correct voltage and resistance. Additionally, it requires knowledge to control each part of the device simultaneously through code with limited computational resources. Lastly, this project demonstrates resourcefulness and creativity in carrying out a project from concept to fruition using only what was immediately available. 

The device has multiple functions including the ability to sense light, detect motion, receive/display input in the form of numbers, open/close a door, and send SMS messages when these events occur. 

When either light or motion is detected while the device is on and running, a text alert using the Twilio service will be sent to a mobile device of our choosing. Light being detected would signal that the safe has been opened, either intentionally or during a "break-in", due to the photoresistor being placed inside the safe. Motion is detectable up to 9 feet away, signaling that something is in the vicinity of the safe. 

My partner and I hardcoded a code to open and close the safe because this project was intended to show proof-of-concept and not intended to serve as a real security device. When this code is entered on the keypad, the input is shown on the LCD screen until the full code is entered. The actuator connected to the door is then activated which opens it. After the code is entered a second time, the actuator is activated again to close the safe door. If an incorrect code is entered, it is rejected and refreshes for a new attempt. 

Each of these functions are simple conceptually, but combining them to work simultaneously with little to no delay was the real task at hand. Each sensor has its own expected electrical input from GPIO pins, some require constant power supply to continuously run, and others only require attention at specific times. Therefore, we included a class that imports a timer for both the motion and light sensors so that these sensors can run on their own threads; unimpeded by the actions of the keypad, LCD screen, or actuator. 

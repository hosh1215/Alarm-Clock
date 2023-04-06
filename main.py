# Project TeLED:
# I needed to make an alarm clock that would turn on my TeLED (TV without display panel)
# Most of this is just UI, but the main jist of things is that at a certain time, 
# This script is run on a Raspberry Pi Pico W using MycroPython in the Thonny IDE.
# My OLED Screen was this one --> SparkFun Qwiic OLED Display (0.91 in, 128x32) https://www.sparkfun.com/products/17153

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import ntp_client as ntp
import time

WIDTH =128 
HEIGHT= 32
i2c=I2C(0,scl=Pin(9),sda=Pin(8),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

mosfet = Pin(2, Pin.OUT) # pin 4 = GPIO 2
mosfet.low()
            
button_hrs = Pin(13, Pin.IN, Pin.PULL_UP) # pin 17 = GPIO 13
button_SET = Pin(14, Pin.IN, Pin.PULL_UP) # pin 18 = GPIO 14
button_mins = Pin(15, Pin.IN, Pin.PULL_UP) # pin 19 = GPIO 15

CurrentState = 0 # 0 for default menu, 1 for edit mode

Alarm = [7,0] # Default alarm [Hours, Minutes]

# I don't think I need either of these...
curTime = 0
CurTime= 0

# For printing the default screen
def menu(curTime, alarm):
    oled.fill(0)
    oled.text("TeLED by hosh", 0, 0)
    oled.text("Time= ", 0, 15)
    if curTime[1] < 10:
        oled.text(str(curTime[0])+":0"+str(curTime[1]), 48, 15)
    else:
        oled.text(str(curTime[0])+":"+str(curTime[1]), 48, 15)
    oled.text("Alarm= ", 0, 25)
    if alarm[1] < 10:
        oled.text(str(alarm[0])+":0"+str(alarm[1]), 56, 25)
    else:
        oled.text(str(alarm[0])+":"+str(alarm[1]), 56, 25)
    oled.show()

# For printing the Edit Mode screen
def printEdit(alarm):
    oled.fill(0)
    oled.text("TeLED by hosh", 0, 0)
    oled.text("Edit= ", 0, 25)
    if alarm[1] < 10:
        oled.text(str(alarm[0])+":0"+str(alarm[1]), 48, 25)
    else:
        oled.text(str(alarm[0])+":"+str(alarm[1]), 48, 25)
    oled.show()

# For entering the new time
def editMode(alarm):
    newAlarm = alarm
    while True:
        if(button_SET.value() == 1):
            break
        elif(button_hrs.value() == 1):
            newAlarm[0] = (newAlarm[0] + 1) % 24
        elif(button_mins.value() == 1):
            newAlarm[1] = (newAlarm[1] + 1) % 60
        printEdit(newAlarm)
        time.sleep(0.2)
    return newAlarm

# Main loop
while True:
    CurTime = ntp.get_time()
    menu(CurTime, Alarm)
    if (CurTime[1] == Alarm [1] and CurTime[0] == Alarm [0]):
            mosfet.high()
            time.sleep(5)
            mosfet.low()
            time.sleep(55)
            # This will prevent edit mode from taking place, but let's assume your desired time is far off from the current time
    if(button_SET.value() == 1):
        CurrentState = 1
    if(button_SET.value() == 0 and CurrentState == 1):
        Alarm = editMode(Alarm)
        CurrentState = 0
        time.sleep(0.4)

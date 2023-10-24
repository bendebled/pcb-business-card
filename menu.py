from machine import Pin, PWM, I2C, ADC, Timer
import machine
import mysh1106
import time

i2c = I2C(scl=Pin(6), sda=Pin(7), freq=400000)
oled = mysh1106.MY_SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)

left_btn = Pin(0, Pin.IN, Pin.PULL_UP)
right_btn = Pin(1, Pin.IN, Pin.PULL_UP)

oled.fill(0) 
oled.text(str("Benoit DEBLED"), 0, 0)
oled.printtext(str("www.debled.com"), 0, 10,1,1)
oled.printtext("benoit@debled.com",0,19,1,1)
oled.printtext("0487/52.44.31",0,28,1,1)

def print_display():
    oled.fill(0)
    oled.fill_rect(0,0,128,9,1)

    t = (int(time.time()/5)) % 4
    if t == 0:
        oled.printtext(str("Benoit DEBLED"), 1, 1, 1, 0)
    elif t == 1:
        oled.printtext(str("www.debled.com"), 1, 1,1,0)
    elif t == 2:
        oled.printtext("benoit@debled.com",1,1,1,0)
    else:
        oled.printtext("0487/52.44.31",1,1,1,0)
    
    oled.printtext("22",128-4*6+2,1,1,0)
    oled.printtext("°C",128-2*6,1,1,0)
    
    oled.text(str("> My Resume <"), 10, 15)
    oled.text(str(" Web server"), 10, 25)
    oled.text(str(" Temp logger"), 10, 35)
    oled.text(str("    Music"), 10, 45)
    oled.text(str("     Fun"), 10, 55)
    
    oled.show()
    
while True:
    print_display()
    time.sleep(1)

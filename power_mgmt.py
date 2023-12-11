from machine import Pin, ADC, deepsleep
import esp32
import time
import led_effect

R5_VALUE = 4.7
R6_VALUE = 1

def read_battery_voltage():
    p = Pin(5, Pin.IN)
    adc = ADC(p)
    v = int(adc.read_uv()/1000)
    return v if v > 25 else 0

def read_battery_voltage_in_mv():
    return int(read_battery_voltage()/(1/(R5_VALUE+R6_VALUE)))

class PowerMgmt: 

    def __init__(self, buttons):
        self.buttons = buttons
        self.allow_inactivity = False

    def enable_peripherals(self, enabled):
        """This function allows one to enable power to the screen, 
        temperature sensors, WS2812B and battery percentage sensor"""
        p = Pin(4, Pin.OUT)
        p.value(1 if enabled else 0)

    def enter_deep_sleep(self):
        ipin0 = Pin(0, Pin.IN, Pin.PULL_UP, hold=True)
        ipin1 = Pin(1, Pin.IN, Pin.PULL_UP, hold=True)
        ipin2 = Pin(2, Pin.IN, Pin.PULL_UP, hold=True)
        ipin3 = Pin(3, Pin.IN, Pin.PULL_UP, hold=True)
        esp32.wake_on_ext1(pins=(ipin0,ipin1,ipin2,ipin3), level=esp32.WAKEUP_ALL_LOW)
        led_effect.cancel()
        self.enable_peripherals(False)
        deepsleep()

    def go_to_sleep_if_needed(self):
        inactivity_time = time.time() - self.buttons.last_pressed
        allowed_inactivity_time = 300 if self.allow_inactivity else 15
        if read_battery_voltage() == 0:
            allowed_inactivity_time = 3600
        if(inactivity_time > allowed_inactivity_time):
            self.enter_deep_sleep()

#if wake_reason() == 7:
#    oled.fill(0)
#    oled.display_menu_entry("Low Battery", 1, 0)
#    oled.display_menu_entry("Please recharge", 2, 0)
#    oled.show()
#    time.sleep(2)
#    enter_deep_sleep()
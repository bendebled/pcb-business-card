from machine import Pin
import time

LEFT_BTN_GPIO = 1
RIGHT_BTN_GPIO = 2
UP_BTN_GPIO = 3
DOWN_BTN_GPIO = 0

class Buttons:

    def __init__(self):
        self.down_btn = Pin(DOWN_BTN_GPIO, Pin.IN, Pin.PULL_UP)
        self.up_btn = Pin(UP_BTN_GPIO, Pin.IN, Pin.PULL_UP)
        self.left_btn = Pin(LEFT_BTN_GPIO, Pin.IN, Pin.PULL_UP)
        self.right_btn = Pin(RIGHT_BTN_GPIO, Pin.IN, Pin.PULL_UP)
        self.last_pressed = time.time()

    def manage_up_down_values(self, value, min_value, max_value):
        if self.is_down_pressed():
            value += 1
        if self.is_up_pressed():
            value -= 1
        return max(min_value, min(max_value, value))
    
    def is_pressed(self, btn):
        if btn.value() == 0:
            self.last_pressed = time.time()
            return True
        return False

    def is_right_pressed(self):
        return self.is_pressed(self.right_btn)
    
    def is_left_pressed(self):
        return self.is_pressed(self.left_btn)
    
    def is_up_pressed(self):
        return self.is_pressed(self.up_btn)
    
    def is_down_pressed(self):
        return self.is_pressed(self.down_btn)
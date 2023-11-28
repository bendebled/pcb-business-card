from machine import Pin

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

    def manage_up_down_values(self, value, min_value, max_value):
        if self.down_btn.value() == 0:
            value += 1
        if self.up_btn.value() == 0:
            value -= 1
        return max(min_value, min(max_value, value))
    
    def is_right_pressed(self):
        return self.right_btn.value() == 0
    
    def is_left_pressed(self):
        return self.left_btn.value() == 0
    
    def is_up_pressed(self):
        return self.up_btn.value() == 0
    
    def is_down_pressed(self):
        return self.down_btn.value() == 0
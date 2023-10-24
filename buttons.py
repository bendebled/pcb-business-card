from machine import Pin
UP_BTN_GPIO = 3
DOWN_BTN_GPIO = 4

class Buttons:

    def __init__(self):
        self.down_btn = Pin(DOWN_BTN_GPIO, Pin.IN, Pin.PULL_UP)
        self.up_btn = Pin(UP_BTN_GPIO, Pin.IN, Pin.PULL_UP)

    def manage_up_down_values(self, value, min_value, max_value):
        if self.down_btn.value() == 0:
            value -= 1
        if self.up_btn.value() == 0:
            value += 1
        return max(min_value, min(max_value, value))
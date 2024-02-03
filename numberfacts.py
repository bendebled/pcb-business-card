import asyncio
import time
from config import conf
from app_secrets import app_secrets
import network
import urequests
import random

NUMBER_OF_CHARS_PER_LINES = int(128/6)

class NumberFacts: 

    def __init__(self, display, buttons):
        self.display = display
        self.buttons = buttons
        self.menu_pos = 0
        self.wlan = None
        self.running =False
   
    def stop(self):
        self.running = False
        self.wlan.active(False)

    def display_scrollable_text(self, text, line):
        self.display.fill(0)
        for i in range(5):
            lineno = line + i
            if lineno < len(text):
                self.display.print_small_text(text[lineno], 0, 10*i, 1, 1, centered=True)
        self.display.show()

    async def run(self):
        self.running = True
        time.sleep(0.1) # avoid entering in the next menu because the right click is still detected

        self.display.fill(0)
        self.display.print_small_text("Connecting to AP...", 0, 15, 1, 1, centered=True)
        self.display.show()

        self.wlan = network.WLAN(network.STA_IF)
        #number_of_tries = 0
        #while not self.wlan.isconnected() and number_of_tries < 5:
        self.wlan.active(True)
        self.wlan.connect(app_secrets['ssid'], app_secrets['psk'])
        #number_of_tries += 1

        cnt = 0
        while not self.wlan.isconnected() and cnt < 50:
            time.sleep(0.1)
            cnt += 1
        time.sleep(0.1)

        self.display.fill(0)
        if self.wlan.isconnected():
            self.display.print_small_text("Connected!", 0, 15, 1, 1, centered=True)
            self.display.print_small_text("IP: {}".format(self.wlan.ifconfig()[0]), 0, 25, 1, 1, centered=True)
        else:
            self.display.print_small_text("Failed to connect!", 0, 15, 1, 1, centered=True)
        self.display.show()

        while self.running:
            self.display.fill(0)
            self.display.print_small_text("loading", 0, 15, 1, 1, centered=True)
            self.display.print_small_text("a new number fact", 0, 25, 1, 1, centered=True)
            self.display.show()

            byte_text = None
            text = None
            lined_text = []
            current_line = ""
            url = "http://numbersapi.com/random/{}".format(random.choice(["trivia","math","date","year"]))
            try:
                response = urequests.get(url)
            except OSError as e:
                self.display.fill(0)
                self.display.print_small_text("Exception occured:", 0, 15, 1, 1, centered=True)
                self.display.print_small_text(str(e), 0, 25, 1, 1, centered=True)
                self.display.print_small_text("Exiting...", 0, 35, 1, 1, centered=True)
                self.display.show()
                print(e)
                time.sleep(2)
                self.running = False
                self.wlan.active(False)
                break
            byte_text = response.content
            response.close()
            if byte_text:
                text = byte_text.decode('ascii')
                for word in text.split(' '):
                    if len(word) < NUMBER_OF_CHARS_PER_LINES - len(current_line):
                        current_line += word + " "
                    else:
                        lined_text.append(current_line)
                        current_line = word + " "
                lined_text.append(current_line)
                lineno = 0
                self.display_scrollable_text(lined_text, lineno)
                while(self.running):
                    oldlineno = lineno
                    if self.buttons.is_up_pressed():
                        lineno = max(lineno-1, 0)
                    if self.buttons.is_down_pressed():
                        lineno = min(lineno+1, len(lined_text))
                    if oldlineno != lineno:
                        self.display_scrollable_text(lined_text, lineno)
                    if self.buttons.is_right_pressed():
                        break
                    await asyncio.sleep(0)
import asyncio
import time
from config import conf

class Settings: 

    def __init__(self, display, buttons, temp):
        self.display = display
        self.buttons = buttons
        self.temp = temp
        self.menu_pos = 0
        self.running = False
   
    def stop(self):
        self.running = False

    def __save_conf_to_flash(self):
        f = open("config.py", "w")
        f.write("conf={}".format(str(conf)))
        f.close()   

    async def run(self):
        self.running = True
        time.sleep(0.1) # avoid entering in the next menu because the right click is still detected

        while self.running:
            self.display.fill(0)
            self.display.display_menu_header()
            self.display.display_menu_entry("Brightness", 0, self.menu_pos)
            self.display.display_menu_entry("Buzzer", 1, self.menu_pos)
            self.display.show()

            self.menu_pos = self.buttons.manage_up_down_values(self.menu_pos, 0, 1)
            if self.menu_pos == 0 and self.buttons.is_right_pressed():
                while True:
                    self.display.fill(0)
                    self.display.rect(59,0,10,64,1)
                    size = int((conf["brightness"]/100)*62)
                    self.display.fill_rect(60,63-size,8,size,1)
                    self.display.text(str(conf["brightness"])+"%",75,28,1)
                    self.display.show()
                    old_brightness = conf["brightness"]
                    if self.buttons.is_up_pressed():
                        conf["brightness"] = min(conf["brightness"] + 1, 100)
                    elif self.buttons.is_down_pressed():
                        conf["brightness"] = max(conf["brightness"] - 1, 0)
                    if old_brightness != conf["brightness"]:
                        self.display.contrast(int(conf["brightness"]*2.55))
                    if self.buttons.is_left_pressed():
                        self.__save_conf_to_flash()
                        time.sleep(0.1) # avoid entering in the previous menu because the left click is still detected
                        break
            if self.menu_pos == 1 and self.buttons.is_right_pressed():
                buzzer_menu_pos = 0
                if conf["buzzer"] == "Low":
                    buzzer_menu_pos = 1
                elif conf["buzzer"] == "High":
                    buzzer_menu_pos = 2
                while True:
                    self.display.fill(0)
                    self.display.display_menu_header()
                    self.display.display_menu_entry("Off", 0, buzzer_menu_pos)
                    self.display.display_menu_entry("Low", 1, buzzer_menu_pos)
                    self.display.display_menu_entry("High", 2, buzzer_menu_pos)
                    self.display.show()
                    buzzer_menu_pos = self.buttons.manage_up_down_values(buzzer_menu_pos, 0, 2)
                    if self.buttons.is_left_pressed():
                        if buzzer_menu_pos == 0:
                            conf["buzzer"] = "Off"
                        elif buzzer_menu_pos == 1:
                            conf["buzzer"] = "Low"
                        elif buzzer_menu_pos == 2:
                            conf["buzzer"] = "High"
                        self.__save_conf_to_flash()
                        time.sleep(0.1) # avoid entering in the previous menu because the left click is still detected
                        break

            self.menu_pos = self.buttons.manage_up_down_values(self.menu_pos, 0, 8)
            await asyncio.sleep(0)
import asyncio
import time

class Resume: 

    def __init__(self, display, buttons):
        self.display = display
        self.buttons = buttons
        self.menu_pos = 0
        self.running = False
   
    def stop(self):
        self.running = False

    async def run(self):
        self.running = True

        while self.running:
            self.display.fill(0)
            if self.menu_pos == 0:
                self.display.text(str("Contacts"), 0, 0)
                self.display.print_small_text(str("Benoit Debled"), 0, 15,1, 1)
                self.display.print_small_text(str("Embedded Engineer"), 0, 25,1, 1)
                self.display.print_small_text(str("www.debled.com"), 0, 35, 1, 1)
                self.display.print_small_text(str("benoit@debled.com"), 0, 45, 1, 1)
                self.display.print_small_text(str("0487/52.44.31"), 0, 55, 1, 1)
            elif self.menu_pos == 1:
                self.display.text(str("Experiences"), 0, 0)
                self.display.print_small_text(str("HMS - Jun 2018 - now"), 0, 15,1, 1)
                self.display.print_small_text(str("Developing embedded"), 0, 25,1, 1)
                self.display.print_small_text(str("industrial routers"), 0, 35,1, 1)
                self.display.print_small_text(str("Tech: C, Rust, Yocto,"), 0, 45, 1, 1)
                self.display.print_small_text(str("u-boot, kernel,"), 0, 55,1, 1)
            elif self.menu_pos == 2:
                self.display.print_small_text(str("drivers, docker,"), 0, 0,1, 1)
                self.display.print_small_text(str("modem-manager,"), 0, 10,1, 1)
                self.display.print_small_text(str("UTF-8, UCS-2"), 0, 20,1, 1)
                self.display.print_small_text(str(""), 0, 55, 1, 1)
            elif self.menu_pos == 3:
                self.display.print_small_text(str("Drooney-sept-nov '16"), 0, 0,1, 1)
                self.display.print_small_text(str("Conception of LoRa"), 0, 10,1, 1)
                self.display.print_small_text(str("sensor pushing data"), 0, 20,1, 1)
                self.display.print_small_text(str("to cloud."), 0, 30, 1, 1)
                self.display.print_small_text(str("Development of PCB,"), 0, 40,1, 1)
                self.display.print_small_text(str("firmware & cloud"), 0, 50,1, 1)
            elif self.menu_pos == 4:
                self.display.text(str("Pers. projects"), 0, 0)
                self.display.print_small_text(str("Home automation"), 0, 15,1, 1)
                self.display.print_small_text(str("Alarm clock"), 0, 25,1, 1)
                self.display.print_small_text(str("Quadcopters"), 0, 35, 1, 1)
            elif self.menu_pos == 5:
                self.display.text(str("Distinctions"), 0, 0)
                self.display.print_small_text(str("Hackathons:"), 0, 15,1, 1)
                self.display.print_small_text(str(" HackUPC"), 0, 25,1, 1)
                self.display.print_small_text(str("  2nd place"), 0, 35,1, 1)
                self.display.print_small_text(str(" Citizens of Wallonia"), 0, 45, 1, 1)
                self.display.print_small_text(str("  Jury Prize"), 0, 55, 1, 1)
            elif self.menu_pos == 6:
                self.display.print_small_text(str("Inno Pepites Junior"), 0, 0,1, 1)
                self.display.print_small_text(str(" Entrepreneurship"), 0, 10,1, 1)
                self.display.print_small_text(str(" contest"), 0, 20,1, 1)
                self.display.print_small_text(str(" snapClassify:"), 0, 30, 1, 1)
                self.display.print_small_text(str(" solution to classify"), 0, 40,1, 1)
                self.display.print_small_text(str(" your photos"), 0, 50,1, 1)
            elif self.menu_pos == 7:
                self.display.text(str("Education"), 0, 0)
                self.display.print_small_text(str("UMONS 2012-2017"), 0, 15,1, 1)
                self.display.print_small_text(str(" Master in"), 0, 25,1, 1)
                self.display.print_small_text(str(" Computer science"), 0, 35,1, 1)
                self.display.print_small_text(str("McCutcheon"), 0, 45, 1, 1)
                self.display.print_small_text(str("High"), 10*6+3, 45, 1, 1)
                self.display.print_small_text(str("School"), 10*6+3+4*6+3, 45, 1, 1)
                self.display.print_small_text(str(" 2011-2012 Indiana,US"), 0, 55, 1, 1)
            elif self.menu_pos == 8:
                self.display.text(str("Skills"), 0, 0)
                self.display.print_small_text(str("C, Rust, Python"), 0, 15,1, 1)
                self.display.print_small_text(str("Yocto, Kernel, drivers"), 0, 25,1, 1)
                self.display.print_small_text(str("device tree, u-boot"), 0, 35, 1, 1)
                self.display.print_small_text(str("git, jenkins"), 0, 45, 1, 1)
            self.display.show()
            while self.running:
                old_resume_pos = self.menu_pos
                self.menu_pos = self.buttons.manage_up_down_values(self.menu_pos, 0, 8)
                if self.menu_pos != old_resume_pos:
                    time.sleep(0.05)
                    break
                await asyncio.sleep(0)
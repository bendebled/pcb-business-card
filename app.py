from machine import Pin, I2C
import mysh1106
import time
from statemachine import *
from tetris import *
import network
import asyncio
from microdot_asyncio import Microdot, send_file

i2c = I2C(scl=Pin(6), sda=Pin(7), freq=400000)
oled = mysh1106.MY_SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)

LEFT_BTN_GPIO = 0
RIGHT_BTN_GPIO = 1
UP_BTN_GPIO = 3
DOWN_BTN_GPIO = 4

left_btn = Pin(LEFT_BTN_GPIO, Pin.IN, Pin.PULL_UP)
right_btn = Pin(RIGHT_BTN_GPIO, Pin.IN, Pin.PULL_UP)
up_btn = Pin(UP_BTN_GPIO, Pin.IN, Pin.PULL_UP)
down_btn = Pin(DOWN_BTN_GPIO, Pin.IN, Pin.PULL_UP)

state_machine = StateMachine()
main_menu_pos = 0
fun_menu_pos = 0
resume_pos = 0

def manage_up_down_values(value, min_value, max_value):
    if down_btn.value() == 0:
        value -= 1
    if up_btn.value() == 0:
        value += 1
    return max(min_value, min(max_value, value))

def display_menu_entry(txt, pos, selected_pos):
    if selected_pos == pos:
        txt = "> {} <".format(txt)
    x_pos = int((128 - len(txt)*8)/2)
    y_pos = 15 + pos*10
    oled.text(txt, x_pos, y_pos)

def display_menu_header():
    oled.fill_rect(0,0,128,9,1)

    t = (int(time.time()/5)) % 4
    if t == 0:
        oled.print_small_text(str("Benoit DEBLED"), 1, 1, 1, 0)
    elif t == 1:
        oled.print_small_text(str("www.debled.com"), 1, 1,1,0)
    elif t == 2:
        oled.print_small_text("benoit@debled.com",1,1,1,0)
    else:
        oled.print_small_text("0487/52.44.31",1,1,1,0)
    
    oled.print_small_text("22",128-4*6+2,1,1,0)
    oled.print_small_text("°C",128-2*6,1,1,0)


def state0_logic():
    global main_menu_pos

    oled.fill(0)
    display_menu_header()
    display_menu_entry("My Resume", 0, main_menu_pos)
    display_menu_entry("Web Server", 1, main_menu_pos)
    display_menu_entry("Temp Logger", 2, main_menu_pos)
    display_menu_entry("Fun", 3, main_menu_pos)
    display_menu_entry("Settings", 4, main_menu_pos)
    oled.show()

    main_menu_pos = manage_up_down_values(main_menu_pos, 0, 4)

    if main_menu_pos == 0 and right_btn.value() == 0:
        state_machine.force_transition_to(resume_state)
    if main_menu_pos == 1 and right_btn.value() == 0:
        state_machine.force_transition_to(web_server_state)
    if main_menu_pos == 2 and right_btn.value() == 0:
        state_machine.force_transition_to(temp_logger_state)
    if main_menu_pos == 3 and right_btn.value() == 0:
        state_machine.force_transition_to(fun_state)

def resume_logic():
    global resume_pos
    transition_to_state0 = False
    while True:
        if transition_to_state0 == True:
            break
        oled.fill(0)
        if resume_pos == 0:
            oled.text(str("Contacts"), 0, 0)
            oled.print_small_text(str("Benoit Debled"), 0, 15,1, 1)
            oled.print_small_text(str("Embedded Engineer"), 0, 25,1, 1)
            oled.print_small_text(str("www.debled.com"), 0, 35, 1, 1)
            oled.print_small_text(str("benoit@debled.com"), 0, 45, 1, 1)
            oled.print_small_text(str("0487/52.44.31"), 0, 55, 1, 1)
        elif resume_pos == 1:
            oled.text(str("Experiences"), 0, 0)
            oled.print_small_text(str("HMS - Jun 2018 - now"), 0, 15,1, 1)
            oled.print_small_text(str("Developping embedded"), 0, 25,1, 1)
            oled.print_small_text(str("industrial routers"), 0, 35,1, 1)
            oled.print_small_text(str("Tech: C, Rust, Yocto,"), 0, 45, 1, 1)
            oled.print_small_text(str("u-boot, kernel,"), 0, 55,1, 1)
        elif resume_pos == 2:
            oled.print_small_text(str("drivers, docker,"), 0, 0,1, 1)
            oled.print_small_text(str("modem-manager,"), 0, 10,1, 1)
            oled.print_small_text(str("UTF-8, UCS-2"), 0, 20,1, 1)
            oled.print_small_text(str(""), 0, 55, 1, 1)
        elif resume_pos == 3:
            oled.print_small_text(str("Drooney-sept-nov '16"), 0, 0,1, 1)
            oled.print_small_text(str("Conception of LoRa"), 0, 10,1, 1)
            oled.print_small_text(str("sensor pushing data"), 0, 20,1, 1)
            oled.print_small_text(str("to cloud."), 0, 30, 1, 1)
            oled.print_small_text(str("Development of PCB,"), 0, 40,1, 1)
            oled.print_small_text(str("firmware & cloud"), 0, 50,1, 1)
        elif resume_pos == 4:
            oled.text(str("Pers. projects"), 0, 0)
            oled.print_small_text(str("Home automation"), 0, 15,1, 1)
            oled.print_small_text(str("Alarm clock"), 0, 25,1, 1)
            oled.print_small_text(str("Quadcopters"), 0, 35, 1, 1)
        elif resume_pos == 5:
            oled.text(str("Distinctions"), 0, 0)
            oled.print_small_text(str("Hackathons:"), 0, 15,1, 1)
            oled.print_small_text(str(" HackUPC"), 0, 25,1, 1)
            oled.print_small_text(str("  2nd place"), 0, 35,1, 1)
            oled.print_small_text(str(" Citizens of Wallonia"), 0, 45, 1, 1)
            oled.print_small_text(str("  Jury Prize"), 0, 55, 1, 1)
        elif resume_pos == 6:
            oled.print_small_text(str("Inno Pepites Junior"), 0, 0,1, 1)
            oled.print_small_text(str(" Entrepreneurship"), 0, 10,1, 1)
            oled.print_small_text(str(" contest"), 0, 20,1, 1)
            oled.print_small_text(str(" snapClassify:"), 0, 30, 1, 1)
            oled.print_small_text(str(" solution to classify"), 0, 40,1, 1)
            oled.print_small_text(str(" your photos"), 0, 50,1, 1)
        elif resume_pos == 7:
            oled.text(str("Education"), 0, 0)
            oled.print_small_text(str("UMONS 2012-2017"), 0, 15,1, 1)
            oled.print_small_text(str(" Master in"), 0, 25,1, 1)
            oled.print_small_text(str(" Computer science"), 0, 35,1, 1)
            oled.print_small_text(str("McCutcheon"), 0, 45, 1, 1)
            oled.print_small_text(str("High"), 10*6+3, 45, 1, 1)
            oled.print_small_text(str("School"), 10*6+3+4*6+3, 45, 1, 1)
            oled.print_small_text(str(" 2011-2012 Indiana,US"), 0, 55, 1, 1)
        elif resume_pos == 8:
            oled.text(str("Skills"), 0, 0)
            oled.print_small_text(str("C, Rust, Python"), 0, 15,1, 1)
            oled.print_small_text(str("Yocto, Kernel, drivers"), 0, 25,1, 1)
            oled.print_small_text(str("device tree, u-boot"), 0, 35, 1, 1)
            oled.print_small_text(str("git, jenkins"), 0, 45, 1, 1)
        oled.show()
        while True:
            old_resume_pos = resume_pos
            resume_pos = manage_up_down_values(resume_pos, 0, 8)
            if resume_pos != old_resume_pos:
                break
            if left_btn.value() == 0:
                transition_to_state0 = True
                break
    state_machine.force_transition_to(state0)

def display_oled_webserver(connected):
    oled.fill(0)
    display_menu_header()
    oled.print_small_text(str("Please connect to"), 0, 15, 1, 1)
    oled.print_small_text(str("SSID \"bendebled\""), 0, 25, 1, 1)
    oled.print_small_text(str("and go to"), 0, 35, 1, 1)
    oled.print_small_text(str("http://192.168.4.1"), 0, 45, 1, 1)
    oled.print_small_text("creating AP" if not connected else "AP created", 0, 55, 1, 1)
    oled.show()

def web_server_logic():
    display_oled_webserver(False)

    ssid = 'bendebled'
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid)
    ap.active(True)
    while ap.active() == False:
        pass
    print('Connection successful')
    display_oled_webserver(True)
    print(ap.ifconfig())
    app = Microdot()

    @app.route('/')
    async def index(request):
        return 'Hello, world!'
    
    @app.route('/resume.pdf')
    def resume(request):
        return send_file('resume.pdf', content_type="application/pdf")
    
    async def check_for_exit_webserver_state():
        while True:
            if left_btn.value() == 0:
                break
            await asyncio.sleep(0.001)
        app.shutdown()
        ap.active(False)
        state_machine.force_transition_to(state0)

    async def start_web_server():
        await app.start_server(port=80, debug=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(check_for_exit_webserver_state(), start_web_server()))

def temp_logger_logic():
    oled.fill(0)
    oled.text(str("temp logger"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

def fun_logic():
    global fun_menu_pos

    oled.fill(0)
    display_menu_header()
    display_menu_entry("Tetris", 0, fun_menu_pos)
    display_menu_entry("Pong", 1, fun_menu_pos)
    oled.show()

    fun_menu_pos = manage_up_down_values(fun_menu_pos, 0, 1)

    if fun_menu_pos == 0 and right_btn.value() == 0:
        state_machine.force_transition_to(fun_tetris_state)
    if fun_menu_pos == 1 and right_btn.value() == 0:
        state_machine.force_transition_to(fun_pong_state)
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

def fun_tetris_logic():
    oled.fill(0)
    oled.text(str("tetris"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

def fun_pong_logic():
    oled.fill(0)
    oled.text(str("pong"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

state0 = state_machine.add_state(state0_logic)
resume_state = state_machine.add_state(resume_logic)
web_server_state = state_machine.add_state(web_server_logic)
temp_logger_state = state_machine.add_state(temp_logger_logic)
fun_state = state_machine.add_state(fun_logic)
fun_tetris_state = state_machine.add_state(fun_tetris_logic)
fun_pong_state = state_machine.add_state(fun_pong_logic)

while True:
    state_machine.run()

from machine import Pin, I2C
from display import *
import time
from statemachine import *
from tetris import *
import asyncio
from config import conf
from resume import *
from buttons import *
from webserver import *

i2c = I2C(scl=Pin(6), sda=Pin(7), freq=400000)
oled = MY_SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)
oled.contrast(int(conf["brightness"]*2.55))

buttons = Buttons()

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

def manage_up_down_values(value, min_value, max_value):
    if down_btn.value() == 0:
        value -= 1
    if up_btn.value() == 0:
        value += 1
    return max(min_value, min(max_value, value))

def state0_logic():
    global main_menu_pos

    oled.fill(0)
    oled.display_menu_header()
    oled.display_menu_entry("My Resume", 0, main_menu_pos)
    oled.display_menu_entry("Web Server", 1, main_menu_pos)
    oled.display_menu_entry("Temp Logger", 2, main_menu_pos)
    oled.display_menu_entry("Fun", 3, main_menu_pos)
    oled.display_menu_entry("Settings", 4, main_menu_pos)
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
    if main_menu_pos == 4 and right_btn.value() == 0:
        state_machine.force_transition_to(settings_state)

async def check_for_exit_state(obj):
    while True:
        if left_btn.value() == 0:
            obj.stop()
            break
        await asyncio.sleep(0.001)
    state_machine.force_transition_to(state0)

async def start_state(obj):
    await obj.run()

def resume_logic():
    resume = Resume(oled, buttons)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_for_exit_state(resume), start_state(resume)))

def web_server_logic():
    webserver = WebServer(oled)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_for_exit_state(webserver), start_state(webserver)))

def temp_logger_logic():
    oled.fill(0)
    oled.text(str("temp logger"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

def fun_logic():
    global fun_menu_pos

    oled.fill(0)
    oled.display_menu_header()
    oled.display_menu_entry("Tetris", 0, fun_menu_pos)
    oled.display_menu_entry("Pong", 1, fun_menu_pos)
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

def settings_logic():
    global settings_menu_pos

    oled.fill(0)
    oled.display_menu_header()
    oled.display_menu_entry("Brightness", 0, settings_menu_pos)
    oled.display_menu_entry("Buzzer", 1, settings_menu_pos)
    oled.show()

    if down_btn.value() == 0:
        settings_menu_pos -= 1
    if up_btn.value() == 0:
        settings_menu_pos += 1
    if settings_menu_pos < 0:
        settings_menu_pos = 0
    elif settings_menu_pos > 1:
        settings_menu_pos = 1

    if settings_menu_pos == 0 and right_btn.value() == 0:
        while True:
            oled.fill(0)
            oled.rect(59,0,10,64,1)
            size = int((conf["brightness"]/100)*62)
            oled.fill_rect(60,63-size,8,size,1)
            oled.text(str(conf["brightness"])+"%",75,28,1)
            oled.show()
            if up_btn.value() == 0:
                conf["brightness"] += 1
                if conf["brightness"] > 100:
                    conf["brightness"] = 100
                oled.contrast(int(conf["brightness"]*2.55))
            elif down_btn.value() == 0:
                conf["brightness"] -= 1
                if conf["brightness"] < 0:
                    conf["brightness"] = 0
                oled.contrast(int(conf["brightness"]*2.55))
            if left_btn.value() == 0:
                f = open("config.py", "w")
                f.write("conf={}".format(str(conf)))
                f.close()
                time.sleep(0.1)
                break
    if settings_menu_pos == 1 and right_btn.value() == 0:
        buzzer_menu_pos = 0 if conf["buzzer"] else 1
        while True:
            oled.fill(0)
            oled.display_menu_header()
            oled.display_menu_entry("On", 0, buzzer_menu_pos)
            oled.display_menu_entry("Off", 1, buzzer_menu_pos)
            oled.show()
            if down_btn.value() == 0:
                buzzer_menu_pos -= 1
            if up_btn.value() == 0:
                buzzer_menu_pos += 1
            if buzzer_menu_pos < 0:
                buzzer_menu_pos = 0
            elif buzzer_menu_pos > 1:
                buzzer_menu_pos = 1
            if left_btn.value() == 0:
                conf["buzzer"] = True if buzzer_menu_pos == 0 else False
                f = open("config.py", "w")
                f.write("conf={}".format(str(conf)))
                f.close()
                time.sleep(0.1)
                break

    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

state0 = state_machine.add_state(state0_logic)
resume_state = state_machine.add_state(resume_logic)
web_server_state = state_machine.add_state(web_server_logic)
temp_logger_state = state_machine.add_state(temp_logger_logic)
fun_state = state_machine.add_state(fun_logic)
fun_tetris_state = state_machine.add_state(fun_tetris_logic)
fun_pong_state = state_machine.add_state(fun_pong_logic)
settings_state = state_machine.add_state(settings_logic)

while True:
    state_machine.run()

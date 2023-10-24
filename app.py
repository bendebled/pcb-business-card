from machine import Pin, I2C
import mysh1106
import time
from statemachine import *
from tetris import *

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
    oled.fill(0)
    oled.text(str("resume"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

def web_server_logic():
    oled.fill(0)
    oled.text(str("web server"), 10, 35)
    oled.show()
    if left_btn.value() == 0:
        state_machine.force_transition_to(state0)

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

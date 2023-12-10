from machine import Pin, I2C, PWM, Timer,wake_reason
from display import *
import time
from statemachine import *
from tetris import *
import asyncio

from config import conf
from resume import *
from buttons import *
from webserver import *
from settings import *
from numberfacts import *
import temperature
from power_mgmt import *
import led_effect

def beep(t):
    p = Pin(10, Pin.OUT)
    pwm = PWM(p, freq=1000, duty=512)
    time.sleep(0.1)
    pwm.deinit()

def background_loop(_):
    power.go_to_sleep_if_needed()

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

    main_menu_pos = buttons.manage_up_down_values(main_menu_pos, 0, 4)
    time.sleep(0.05)

    if main_menu_pos == 0 and buttons.is_right_pressed():
        state_machine.force_transition_to(resume_state)
    if main_menu_pos == 1 and buttons.is_right_pressed():
        state_machine.force_transition_to(web_server_state)
    if main_menu_pos == 2 and buttons.is_right_pressed():
        state_machine.force_transition_to(temp_logger_state)
    if main_menu_pos == 3 and buttons.is_right_pressed():
        state_machine.force_transition_to(fun_state)
    if main_menu_pos == 4 and buttons.is_right_pressed():
        state_machine.force_transition_to(settings_state)

async def check_left_and_right_for_exit(obj, outro=None):
    counter = 0
    while True:
        if buttons.is_left_pressed() and buttons.is_right_pressed():
            counter += 1
        else:
            counter = 0
        if counter == 10:
            obj.stop()
            break
        await asyncio.sleep(0.001)
    if outro:
        oled.fill(0)
        oled.display_menu_entry("Thanks for", 1, 0)
        oled.display_menu_entry("playing!", 2, 0)
        oled.show()
        time.sleep(1)
    state_machine.force_transition_to(state0)

async def check_left_for_exit(obj):
    while True:
        if buttons.is_left_pressed():
            obj.stop()
            break
        await asyncio.sleep(0)
    state_machine.force_transition_to(state0)

async def start_state(obj):
    await obj.run()

def resume_logic():
    led_effect.cancel()
    resume = Resume(oled, buttons)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_left_for_exit(resume), start_state(resume)))

def web_server_logic():
    global allow_inactivity
    power.allow_inactivity = True
    led_effect.cancel()
    webserver = WebServer(oled)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_left_for_exit(webserver), start_state(webserver)))
    power.allow_inactivity = False

def temp_logger_logic():
    oled.fill(0)
    oled.text(str("temp logger"), 10, 35)
    oled.show()
    if buttons.is_left_pressed():
        state_machine.force_transition_to(state0)

def fun_logic():
    global fun_menu_pos

    oled.fill(0)
    oled.display_menu_header()
    oled.display_menu_entry("Tetris", 0, fun_menu_pos)
    oled.display_menu_entry("Number Facts", 1, fun_menu_pos)
    oled.show()

    fun_menu_pos = buttons.manage_up_down_values(fun_menu_pos, 0, 1)
    time.sleep(0.05)

    if fun_menu_pos == 0 and buttons.is_right_pressed():
        state_machine.force_transition_to(fun_tetris_state)
    if fun_menu_pos == 1 and buttons.is_right_pressed():
        state_machine.force_transition_to(fun_numbers_state)
    if buttons.is_left_pressed():
        state_machine.force_transition_to(state0)

def fun_tetris_logic():
    led_effect.cancel()
    oled.fill(0)
    oled.print_small_text("Press LEFT & RIGHT", 0, 15, 1, 1, centered=True)
    oled.print_small_text("for 2 seconds", 0, 25, 1, 1, centered=True)
    oled.print_small_text("to return to", 0, 35, 1, 1, centered=True)
    oled.print_small_text("main menu", 0, 45, 1, 1, centered=True)
    oled.show()
    time.sleep(3)
    tetris = Tetris(oled, buttons)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_left_and_right_for_exit(tetris, "Thanks for playing!"), start_state(tetris)))

def fun_numbers_logic():
    led_effect.cancel()
    numberfacts = NumberFacts(oled, buttons)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_left_for_exit(numberfacts), start_state(numberfacts)))


def settings_logic():
    led_effect.cancel()
    settings = Settings(oled, buttons, temp)
    asyncio.new_event_loop().run_until_complete(asyncio.gather(check_left_for_exit(settings), start_state(settings)))

buttons = Buttons()
power = PowerMgmt(buttons)
power.enable_peripherals(True)
time.sleep(0.5)

pbuz = Pin(10, Pin.OUT)
pbuz.value(0)

i2c = I2C(scl=Pin(6), sda=Pin(7), freq=400000)
temp = temperature.Temperature(i2c)
oled = MY_SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180, temperature=temp)
oled.contrast(int(conf["brightness"]*2.55))

state_machine = StateMachine()
state0 = state_machine.add_state(state0_logic)
resume_state = state_machine.add_state(resume_logic)
web_server_state = state_machine.add_state(web_server_logic)
temp_logger_state = state_machine.add_state(temp_logger_logic)
fun_state = state_machine.add_state(fun_logic)
fun_tetris_state = state_machine.add_state(fun_tetris_logic)
fun_numbers_state = state_machine.add_state(fun_numbers_logic)
settings_state = state_machine.add_state(settings_logic)

allow_inactivity = False
main_menu_pos = 0
fun_menu_pos = 0

tim = Timer(0)
tim.init(period=10000, callback=background_loop, mode=Timer.PERIODIC)

if wake_reason() == machine.DEEPSLEEP_RESET:
    battery_mv = power_mgmt.read_battery_voltage_in_mv()
    if battery_mv != 0 and battery_mv < 3100:
        oled.fill(0)
        oled.display_menu_entry("Low Battery", 1, 0)
        oled.display_menu_entry("Please recharge", 2, 0)
        oled.show()
        time.sleep(2)
        power.enter_deep_sleep()
i = 0
steps = 0
while True:
    state_machine.run()
    led_effect.tick()
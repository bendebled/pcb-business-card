from machine import Pin, PWM
import time
from config import conf

tones = {
    'REST':0,
    'C0':16,
    'C#0':17,
    'D0':18,
    'D#0':19,
    'E0':21,
    'F0':22,
    'F#0':23,
    'G0':24,
    'G#0':26,
    'A0':28,
    'A#0':29,
    'B0':31,
    'C1':33,
    'C#1':35,
    'D1':37,
    'D#1':39,
    'E1':41,
    'F1':44,
    'F#1':46,
    'G1':49,
    'G#1':52,
    'A1':55,
    'A#1':58,
    'B1':62,
    'C2':65,
    'C#2':69,
    'D2':73,
    'D#2':78,
    'E2':82,
    'F2':87,
    'F#2':92,
    'G2':98,
    'G#2':104,
    'A2':110,
    'A#2':117,
    'B2':123,
    'C3':131,
    'C#3':139,
    'D3':147,
    'D#3':156,
    'E3':165,
    'F3':175,
    'F#3':185,
    'G3':196,
    'G#3':208,
    'A3':220,
    'A#3':233,
    'B3':247,
    'C4':262,
    'C#4':277,
    'D4':294,
    'D#4':311,
    'E4':330,
    'F4':349,
    'F#4':370,
    'G4':392,
    'G#4':415,
    'A4':440,
    'A#4':466,
    'B4':494,
    'C5':523,
    'C#5':554,
    'D5':587,
    'D#5':622,
    'E5':659,
    'F5':698,
    'F#5':740,
    'G5':784,
    'G#5':831,
    'A5':880,
    'A#5':932,
    'B5':988,
    'C6':1047,
    'C#6':1109,
    'D6':1175,
    'D#6':1245,
    'E6':1319,
    'F6':1397,
    'F#6':1480,
    'G6':1568,
    'G#6':1661,
    'A6':1760,
    'A#6':1865,
    'B6':1976,
    'C7':2093,
    'C#7':2217,
    'D7':2349,
    'D#7':2489,
    'E7':2637,
    'F7':2794,
    'F#7':2960,
    'G7':3136,
    'G#7':3322,
    'A7':3520,
    'A#7':3729,
    'B7':3951,
    'C8':4186,
    'C#8':4435,
    'D8':4699,
    'D#8':4978,
    'E8':5274,
    'F8':5588,
    'F#8':5920,
    'G8':6272,
    'G#8':6645,
    'A8':7040,
    'A#8':7459,
    'B8':7902,
    'C9':8372,
    'C#9':8870,
    'D9':9397,
    'D#9':9956,
    'E9':10548,
    'F9':11175,
    'F#9':11840,
    'G9':12544,
    'G#9':13290,
    'A9':14080,
    'A#9':14917,
    'B9':15804
}


# from here: https://github.com/vertexi/tetris_mpy/blob/main/music.py
tetris=[
    ("E6",4),
("B5",2),
("C6",2),
("D6",2),
("E6",1),
("D6",1),
("C6",2),
("B5",2),
("A5",2),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",6),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",8),
("D6",4),
("F6",2),
("A6",4),
("G6",2),
("F6",2),
("E6",6),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",4),
("B5",2),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",4),
("E6",4),
("B5",2),
("C6",2),
("D6",2),
("E6",1),
("D6",1),
("C6",2),
("B5",2),
("A5",4),
("A5",2),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",6),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",8),
("D6",4),
("F6",2),
("A6",4),
("G6",2),
("F6",2),
("E6",6),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",4),
("B5",2),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",4),
("E5",8),
("C5",8),
("D5",8),
("B4",8),
("C5",8),
("A4",8),
("G#4",8),
("B4",4),
("E5",8),
("C5",8),
("D5",8),
("B4",8),
("C5",4),
("E5",4),
("A5",8),
("G#5",8),
("E6",4),
("B5",2),
("C6",2),
("D6",2),
("E6",1),
("D6",1),
("C6",2),
("B5",2),
("A5",4),
("A5",2),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",6),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",8),
("D6",4),
("F6",2),
("A6",4),
("G6",2),
("F6",2),
("E6",6),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",4),
("B5",2),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",4),
("E6",4),
("B5",2),
("C6",2),
("D6",2),
("E6",1),
("D6",1),
("C6",2),
("B5",2),
("A5",4),
("A5",2),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",6),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",8),
("D6",4),
("F6",2),
("A6",4),
("G6",2),
("F6",2),
("E6",6),
("C6",2),
("E6",4),
("D6",2),
("C6",2),
("B5",4),
("B5",2),
("C6",2),
("D6",4),
("E6",4),
("C6",4),
("A5",4),
("A5",4),
("A5",4),
]

#From here: https://github.com/hibit-dev/buzzer/blob/master/src/other/happy_birthday/happy_birthday.ino
happy_birthday=[
    ("C4",4),
("C4",8),
("D4",4),
("C4",4),
("F4",4),
("E4",2),
("C4",4),
("C4",8),
("D4",4),
("C4",4),
("G4",4),
("F4",2),
("C4",4),
("C4",8),
("C5",4),
("A4",4),
("F4",4),
("E4",4),
("D4",4),
("A#4",4),
("A#4",8),
("A4",4),
("F4",4),
("G4",4),
("F4",2),
]

fail = [
    ("G4", 2),
    ("C4", 4)
]

BUZZER_PIN = 10
pin = Pin(BUZZER_PIN, Pin.OUT)

def return_note():
    ret = []
    for note, duration in tetris:
        for _ in range(duration):
            ret.append(tones[note])
    return ret

freqlist=return_note()

oldPWM = None
oldfreq = 0

def stop():
    if oldPWM:
        oldPWM.deinit()
    Pin(BUZZER_PIN, Pin.OUT)

def set_buzzer(freq, duty):
    global oldPWM
    global oldfreq
    if oldfreq != freq:
        if oldPWM:
            oldPWM.deinit()
        if freq > 0:
            pwm = PWM(pin, freq=freq, duty=duty)
        else:
            stop()
            pwm = None
        oldPWM = pwm
        oldfreq = freq

def tick(tick):
    if conf["buzzer"] != "Off":
        duty = 512 if conf["buzzer"] == "High" else 1020
        freq = freqlist[tick%len(freqlist)]
        set_buzzer(freq, duty)
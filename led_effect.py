import neopixel
import machine
import colorsys

np = neopixel.NeoPixel(machine.Pin(20), 4)

i = 0
color = (0,0,0)

def cancel():
    np[0] = (0,0,0)
    np[1] = np[0]
    np[2] = np[0]
    np[3] = np[0]
    np.write()

def tick():
    global i
    global color
    if i < 90 :
        color = colorsys.hls_to_rgb((i*4)/360.0,0.1, 1)
        color = (int(color[0]*255),int(color[1]*255),int(color[2]*255))
        colorhalf = (int(color[0]*0.5),int(color[1]*0.5),int(color[2]*0.5))
        if i % 6 == 0:
            np[0] = color
            np[1] = colorhalf
            np[2] = (0,0,0)
            np[3] = (0,0,0)
        elif i % 6 == 1:
            np[0] = colorhalf
            np[1] = color
            np[2] = colorhalf
            np[3] = (0,0,0)
        elif i % 6 == 2:
            np[0] = (0,0,0)
            np[1] = colorhalf
            np[2] = color
            np[3] = colorhalf
        elif i % 6 == 3:
            np[0] = (0,0,0)
            np[1] = (0,0,0)
            np[2] = colorhalf
            np[3] = color
        elif i % 6 == 4:
            np[0] = (0,0,0)
            np[1] = colorhalf
            np[2] = color
            np[3] = colorhalf
        elif i % 6 == 5:
            np[0] = colorhalf
            np[1] = color
            np[2] = colorhalf
            np[3] = (0,0,0)
        i+=1
        np.write()
        if i == 90:
            cancel()
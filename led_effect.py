import neopixel
import machine
import colorsys

np = neopixel.NeoPixel(machine.Pin(20), 4)

i = 0
steps = 0
color = (0,0,0)

def cancel():
    np[0] = (0,0,0)
    np[1] = np[0]
    np[2] = np[0]
    np[3] = np[0]
    np.write()

def tick():
    global i
    global steps
    global color
    if steps == 0 and i < 24 :
        np[0] = (i,0,0)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i+=2
        if i == 24:
            steps += 1
    if steps == 1 and i > 0 :
        np[0] = (i,0,0)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i-=2
        if i == 0:
            steps += 1

    if steps == 2 and i < 24 :
        np[0] = (0,i,0)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i+=2
        if i == 24:
            steps += 1
    if steps == 3 and i > 0 :
        np[0] = (0,i,0)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i-=2
        if i == 0:
            steps += 1

    if steps == 4 and i < 24 :
        np[0] = (0,0,i)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i+=2
        if i == 24:
            steps += 1
    if steps == 5 and i > 0 :
        np[0] = (0,0,i)
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i-=2
        if i == 0:
            steps += 1
    if steps == 6 and i < 10:
        color = colorsys.hls_to_rgb(0.0,0+(0.01)*i, 1)
        color = (int(color[0]*255),int(color[1]*255),int(color[2]*255))
        np[0] = color
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i+=1
        if i == 10:
            i = 0
            steps += 1
    if steps == 7 and i < 90 :
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
        if i == 90:
            steps += 1
            i = 0
    if steps == 8 and i <= 10:
        print(steps)
        print(i)
        color = colorsys.hls_to_rgb(0.0,0.1-(0.01)*i, 1)
        color = (int(color[0]*255),int(color[1]*255),int(color[2]*255))
        np[0] = color
        np[1] = np[0]
        np[2] = np[0]
        np[3] = np[0]
        i+=1
        if i == 11:
            i = 0
            steps += 1
    np.write()
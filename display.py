import sh1106
import time
import power_mgmt

cmap = ['00000000000000000000000000000000000', #Space
        '00100001000010000100001000000000100', #!
        '01010010100000000000000000000000000', #"
        '01010010101101100000110110101001010', ##
        '00100011111000001110000011111000100', #$
        '11001110010001000100010001001110011', #%
        '01000101001010001000101011001001101', #&
        '10000100001000000000000000000000000', #'
        '00100010001000010000100000100000100', #(
        '00100000100000100001000010001000100', #)
        '00000001001010101110101010010000000', #*
        '00000001000010011111001000010000000', #+
        '000000000000000000000000000000110000100010000', #,
        '00000000000000011111000000000000000', #-
        '00000000000000000000000000110001100', #.
        '00001000010001000100010001000010000', #/
        '01110100011000110101100011000101110', #0
        '00100011000010000100001000010001110', #1
        '01110100010000101110100001000011111', #2
        '01110100010000101110000011000101110', #3
        '00010001100101011111000100001000010', #4
        '11111100001111000001000011000101110', #5
        '01110100001000011110100011000101110', #6
        '11111000010001000100010001000010000', #7
        '01110100011000101110100011000101110', #8
        '01110100011000101111000010000101110', #9
        '00000011000110000000011000110000000', #:
        '01100011000000001100011000010001000', #;
        '00010001000100010000010000010000010', #<
        '00000000001111100000111110000000000', #=
        '01000001000001000001000100010001000', #>
        '01100100100001000100001000000000100', #?
        '01110100010000101101101011010101110', #@
        '00100010101000110001111111000110001', #A
        '11110010010100111110010010100111110', #B
        '01110100011000010000100001000101110', #C
        '11110010010100101001010010100111110', #D
        '11111100001000011100100001000011111', #E
        '11111100001000011100100001000010000', #F
        '01110100011000010111100011000101110', #G
        '10001100011000111111100011000110001', #H
        '01110001000010000100001000010001110', #I
        '00111000100001000010000101001001100', #J
        '10001100101010011000101001001010001', #K
        '10000100001000010000100001000011111', #L
        '10001110111010110101100011000110001', #M
        '10001110011010110011100011000110001', #N
        '01110100011000110001100011000101110', #O
        '11110100011000111110100001000010000', #P
        '01110100011000110001101011001001101', #Q
        '11110100011000111110101001001010001', #R
        '01110100011000001110000011000101110', #S
        '11111001000010000100001000010000100', #T
        '10001100011000110001100011000101110', #U
        '10001100011000101010010100010000100', #V
        '10001100011000110101101011101110001', #W
        '10001100010101000100010101000110001', #X
        '10001100010101000100001000010000100', #Y
        '11111000010001000100010001000011111', #Z
        '01110010000100001000010000100001110', #[
        '10000100000100000100000100000100001', #\
        '00111000010000100001000010000100111', #]
        '00100010101000100000000000000000000', #^
        '00000000000000000000000000000011111', #_
        '11000110001000001000000000000000000', #`
        '00000000000111000001011111000101110', #a
        '10000100001011011001100011100110110', #b
        '00000000000011101000010000100000111', #c
        '00001000010110110011100011001101101', #d
        '00000000000111010001111111000001110', #e
        '00110010010100011110010000100001000', #f
        '000000000001110100011000110001011110000101110', #g
        '10000100001011011001100011000110001', #h
        '00100000000110000100001000010001110', #i
        '0001000000001100001000010000101001001100', #j
        '10000100001001010100110001010010010', #k
        '01100001000010000100001000010001110', #l
        '00000000001101010101101011010110101', #m
        '00000000001011011001100011000110001', #n
        '00000000000111010001100011000101110', #o
        '000000000001110100011000110001111101000010000', #p
        '000000000001110100011000110001011110000100001', #q
        '00000000001011011001100001000010000', #r
        '00000000000111110000011100000111110', #s
        '00100001000111100100001000010000111', #t
        '00000000001000110001100011001101101', #u
        '00000000001000110001100010101000100', #v
        '00000000001000110001101011010101010', #w
        '00000000001000101010001000101010001', #x
        '000000000010001100011000110001011110000101110', #y
        '00000000001111100010001000100011111', #z
        '00010001000010001000001000010000010', #{
        '00100001000010000000001000010000100', #|
        '01000001000010000010001000010001000', #}
        '01000101010001000000000000000000000', #}~
        '00111001010011100000000000000000000',  #°
        '11111111111111111111111111111111111', #square for unknown symbols

]

class MY_SH1106_I2C(sh1106.SH1106_I2C):
    def __init__(self, width, height, i2c, res=None, addr=0x3c,
                 rotate=0, external_vcc=False, delay=0, temperature=None):
        sh1106.SH1106_I2C.__init__(self, width, height, i2c, res, addr,
                 rotate, external_vcc, delay)
        self.temperature = temperature

    def print_small_text(self, text, xpos, ypos, size, color, centered=False):
        if centered:
            xpos = int((128 - len(text)*6)/2)
        for char in text:
            self.print_char(char, xpos, ypos, size, color)
            xpos += 6
            
    def print_char(self,letter,xpos,ypos,size, color):
        origin = xpos
        charval = ord(letter)
        
        index = charval-32 #start code, 32 or space
        if letter == '°':
            index = len(cmap)-2
        index=min(index, len(cmap)-1)
        character = cmap[index] #this is our char...
        rows = [character[i:i+5] for i in range(0,len(character),5)]
        for row in rows:
            for bit in row:
                if bit == '1':
                    self.pixel(xpos,ypos,color)
                    if size==2:
                        self.pixel(xpos,ypos+1,color)
                        self.pixel(xpos+1,ypos,color)
                        self.pixel(xpos+1,ypos+1,color)
                xpos+=size
            xpos=origin
            ypos+=size

    def display_menu_entry(self, txt, pos, selected_pos):
        if selected_pos == pos:
            txt = "> {} <".format(txt)
        x_pos = int((128 - len(txt)*8)/2)
        y_pos = 15 + pos*10
        self.text(txt, x_pos, y_pos)
    
    def draw_batt(self, x, bars):
        self.rect(x, 2, 4, 6, 0)
        self.line(x+1,1,x+2,1,0)
        if bars > 0:
            self.line(x,6,x+3,6,0)
        if bars > 1:
            self.line(x,5,x+3,5,0)
        if bars > 2:
            self.line(x,4,x+3,4,0)
        if bars > 3:
            self.line(x,3,x+3,3,0)
    
    def display_battery(self):
        v = power_mgmt.read_battery_voltage_in_mv()
        if v == 0:
            ms = int((time.time_ns()/7500000)%500)
            bars = int(ms/100)
        else:
            if v > 3950:
                bars = 4
            elif v <= 3950 and v >= 3800:
                bars = 3
            elif v < 3800 and v >= 3600:
                bars = 2
            else:
                bars = 1
        self.draw_batt(123,bars) 

    def display_temp(self):
        self.print_small_text(str(int(self.temperature.read_temp())),123-4*6+2,1,1,0)
        self.print_small_text("°C",123-2*6,1,1,0)

    def display_menu_header(self):
        self.fill_rect(0,0,128,9,1)

        t = (int(time.time()/5)) % 4
        if t == 0:
            self.print_small_text(str("Benoit DEBLED"), 1, 1, 1, 0)
            self.display_battery()
            self.display_temp()
        elif t == 1:
            self.print_small_text(str("www.debled.com"), 1, 1,1,0)
            self.display_battery()
            self.display_temp()
        elif t == 2:
            self.print_small_text("benoit@debled.com",1,1,1,0)
            self.display_battery()
        else:
            self.print_small_text("0487/52.44.31",1,1,1,0)
            self.display_battery()
            self.display_temp()
        

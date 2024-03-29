import asyncio
import network
from microdot_asyncio import Microdot, send_file
import music
import neopixel, machine
import ubinascii

class WebServer: 

    def __init__(self, display):
        self.display = display
        self.app = None
        self.app = None

    def display_oled_webserver(self, connected):
        self.display.fill(0)
        self.display.display_menu_header()
        self.display.print_small_text(str("Please connect to"), 0, 15, 1, 1, centered=True)
        self.display.print_small_text(str("SSID \"bendebled\""), 0, 25, 1, 1, centered=True)
        self.display.print_small_text(str("and go to"), 0, 35, 1, 1, centered=True)
        self.display.print_small_text(str("http://192.168.4.1"), 0, 45, 1, 1, centered=True)
        self.display.print_small_text("creating AP" if not connected else "AP created", 0, 55, 1, 1, centered=True)
        self.display.show()

   
    def stop(self):
        self.app.shutdown()
        self.ap.active(False)

    async def run(self):
        self.display_oled_webserver(False)

        ssid = 'bendebled'
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=ssid)
        while self.ap.active() == False:
            pass
        print('Connection successful')
        self.display_oled_webserver(True)
        print(self.ap.ifconfig())
        self.app = Microdot()

        np = neopixel.NeoPixel(machine.Pin(20), 4)

        @self.app.route('/')
        async def index(request):
            return send_file('index.html')
        
        @self.app.route('/static/<path:path>')
        def static(request, path):
            if '..' in path:
                return 'Not found', 404
            if path.endswith(".svg"):
                return send_file('static/' + path, max_age=86400, content_type="image/svg+xml")
            else:
                return send_file('static/' + path, max_age=86400)
        
        @self.app.route('/dev/buzzer/<freq>')
        async def buzzer(request, freq):
            music.set_buzzer(int(freq), 512)

        @self.app.route('/dev/led/<led_id>/<hex>')
        async def led(request, led_id, hex):
            led_id = int(led_id)
            if led_id < 0 or led_id > 4:
                return 'led_id must be between 1 and 4', 403
            bytesValues = ubinascii.unhexlify(hex)
            np[led_id-1] = (bytesValues[0],bytesValues[1],bytesValues[2])
            np.write()
        
        @self.app.route('/benoit-debled-resume.pdf')
        def resume(request):
            return send_file('benoit-debled-resume.pdf', content_type="application/pdf")
        
        await self.app.start_server(port=80, debug=True)
import asyncio
import network
from microdot_asyncio import Microdot, send_file


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

        @self.app.route('/')
        async def index(request):
            return 'Hello, world!'
        
        @self.app.route('/resume.pdf')
        def resume(request):
            return send_file('resume.pdf', content_type="application/pdf")
        
        await self.app.start_server(port=80, debug=True)
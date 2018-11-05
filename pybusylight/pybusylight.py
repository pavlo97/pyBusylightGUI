import binascii
import usb.core
import usb.util
import signal
import time
import sys
import threading

ALIVE  = "8F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF03EB"

# RED, GREEN, BLUE, PINK, ORANGE, YELLOW, PURPLE
COLORS = ["1001FF0000010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF04ED",
          "100100FF00010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF04ED",
          "10010000FF010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF04ED",
          "1001FF203C010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0549",
          "1001FF2800010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0515",
          "1001FFFF00010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF05EC",
          "1001B400E1010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0583"
        ]
# FUNKY, NORDIC, QUIET, OPEN, KUANDO
SOUNDS = ["1178FFFF0005039B000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0686",
          "1178FFFF000503B3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF069E",
          "1178FFFF00050393000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF067E",
          "1178FFFF0005038B000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0676",
          "1178FFFF000503AB000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF0696",          
        ]

LIGHT_OFF = "1001000000010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF03EE"
MUSIC_OFF = "1001000000010080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060455FFFFFF03EE"

BLINKING_PERIOD = 0.5

def signal_handler(signal, frame):
    print('\nCaught CTRL+C turning off.')
    busylight().close()()
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

class busylight:

    def __init__(self,debug=False):
        self.ep = None 
        self.debug = debug
        self.__connect_busylight__()
        self.setColor(1) #Green
        self.blink = False
        self.keepAlive()
        
        self.sound = 0 #Funky
        self.volume = 0
    
    def __connect_busylight__(self):
        try:
            dev = usb.core.find(idVendor=0x27bb, idProduct=0x3bca)
        except NoBackendError:
            print("""ERROR: PyUSB needs at least one of the supported backends installed.
    If you're on a MAC you can install libusb via:
        $ brew install libusb

    On Ubuntu 16.04/18.04
    sudo apt-get install libusb-1.0-0 """)
            sys.exit(1)

        if dev is None: raise ValueError('Device not found')
        dev.reset()
        if dev.is_kernel_driver_active(0) == True:
                dev.detach_kernel_driver(0)

        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        self.ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert self.ep is not None
    
    def keepAlive(self):
        self.buffer = ALIVE
        self.send()
        #print(time.ctime())
        self.timer = threading.Timer(10,self.keepAlive)
        self.timer.start()
        
    def setColor(self,colorId = 0):
        self.color = COLORS[colorId]
        self.buffer = self.color
        self.send();

    def set_sound(self,sound = 0):
        self.turn_off()
        time.sleep(1)
        self.buffer = SOUNDS[sound]
        self.send()

    def setBlink(self,enable = False):
        self.blink = enable       
        if enable:
            self.light_on=True
            self.blinkTimer = threading.Timer(BLINKING_PERIOD,self.handleBlinking)
            self.handleBlinking()
        else:
            self.blinkTimer.cancel()

    def handleBlinking(self):
        if self.light_on:
            self.buffer = LIGHT_OFF
        else :
            self.buffer = self.color
        self.send()
            
        self.light_on = not self.light_on
        self.blinkTimer = threading.Timer(BLINKING_PERIOD,self.handleBlinking)
        self.blinkTimer.start()
        
    def setParty(self):
        
        
    def turn_off(self):
        if self.blink:
            self.blinkTimer.cancel()        
        self.buffer = LIGHT_OFF
        self.send()
        self.buffer = MUSIC_OFF
        self.send()
        
    def close(self):
        self.turn_off()
        self.timer.cancel()
        if self.blink:
            self.blinkTimer.cancel()
        print("Closing App")
        sys.exit(0)

    def send(self):
        self.ep.write(binascii.unhexlify(self.buffer))

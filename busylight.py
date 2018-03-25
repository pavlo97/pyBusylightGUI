#!/usr/bin/python

import usb.core
import usb.util
import time

class busylight:

    def __init__(self):
        ep = self.__connect_busylight__()
        
        red = 255
        green = 255
        blue = 255
        sound = 128
        volume = 0

    def __connect_busylight__(self):
        dev = usb.core.find(idVendor=0x04d8, idProduct=0xf848)

        if dev is None: raise ValueError('Device not found')
        dev.reset()
        if dev.is_kernel_driver_active(0) == True:
                dev.detach_kernel_driver(0)

        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert ep is not None
        return ep

    def send_signal(self):
        buff = ("\x10\x00%s%s%s\x00\x00%s\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"%(chr(red),chr(green),chr(blue),chr(int(sound)+int(volume))))
        self.ep.write(buff)





sounds={"off":128,
        "OpenOffice":136,
        "Quiet":144,
        "Funky":152,
        "FairyTale":160,
        "KuandoTrain":168,
        "TelephoneNordic":176,
        "TelephoneOriginal":184,
        "TelephonePickMeUp":192,
        "Buzz":216
        }
# Colors are good for 30 sec, sounds are applied until turned off.
# Red is 3
# Green is 4
# Blue is 5
# Sound is 8
red   ="\x10\x00\x1f\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"
green ="\x10\x00\x00\x06\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\x92"
blue  ="\x10\x00\x00\x00\x1f\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"

quiet   ="\x10\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"


# for i in sounds:
#     ep.write(quiet)
#     time.sleep(1)
#     sound_val=int(sounds[i]+4)
#     print("Playing %s (%s)"%(i,sound_val))
#     to_write=("\x10\x00\x00\x00\x00\x00\x00%s\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"%chr(sound_val))
#     ep.write(to_write)
#     time.sleep(5)S



try:
    while True:
        ep.write(red)
        time.sleep(0.1)
        ep.write(quiet)
        time.sleep(0.1)
except usb.core.USBError as e:
    print "Write USBError: " + str(e)
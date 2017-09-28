from modules.core.core import cbpi
from modules.core.basetypes import Actor
from modules.core.proptypes import Property
from datetime import datetime, timedelta

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print e
    pass

cbpi.gpio_compressors = []

class Compressor(Actor):
    c_delay = Property.Number("Compressor Delay", True, 10, description="Minium time between cycles in minutes")
    gpio = Property.Select("GPIO", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="GPIO to which the actor is connected")
    compressor_on = False
    compressor_wait = datetime.utcnow()
    delayed = False

    def init(self):
        GPIO.setup(int(self.gpio), GPIO.OUT)
        cbpi.gpio_compressors += [self]

    def on(self, power=0):
        if datetime.utcnow() >= self.compressor_wait:
            self.compressor_on = True
            super(Compressor, self).on(power)
            self.delayed = False
        else:
            print "Delaying Turing on Compressor"
            self.delayed = True

    def off(self):
        if self.compressor_on:
            self.compressor_on = False
            self.compressor_wait = datetime.utcnow() + timedelta(minutes=int(self.c_delay))
        self.delayed = False
        super(Compressor, self).off()

@cbpi.addon.core.backgroundjob(key="update_compressors", interval=5)
def update_compressors(api):
    for compressor in cbpi.gpio_compressors:
        if compressor.delayed and datetime.utcnow() >= compressor.compressor_wait:
            compressor.on()

@cbpi.addon.actor.type("Relay Board Compressor")
class RelayCompressor(Compressor):

    def init(self):
        super(Compressor, self).init()
        GPIO.output(int(self.gpio), 1)

    def on(self, power=0):
        GPIO.output(int(self.gpio), 0)

    def off(self):
        GPIO.output(int(self.gpio), 1)

@cbpi.addon.actor.type("Simple GPIO Compressor")
class GPIOCompressor(Compressor):

    def init(self):
        super(Compressor, self).init()
        GPIO.output(int(self.gpio), 0)

    def on(self, power=0):
        GPIO.output(int(self.gpio), 1)

    def off(self):
        GPIO.output(int(self.gpio), 0)

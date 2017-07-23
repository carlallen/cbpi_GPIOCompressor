from modules import cbpi
from modules.base_plugins.gpio_actor import *
from modules.core.props import Property
from datetime import datetime, timedelta

cbpi.gpio_compressors = []

class Compressor(object):
    c_delay = Property.Number("Compressor Delay", True, 10, "minutes")
    compressor_on = False
    compressor_wait = datetime.utcnow()
    delayed = False

    def init(self):
        super(Compressor, self).init()
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

@cbpi.backgroundtask(key="update_compressors", interval=5)
def update_compressors(api):
    for compressor in cbpi.gpio_compressors:
        if compressor.delayed and datetime.utcnow() >= compressor.compressor_wait:
            compressor.on()

@cbpi.actor
class RelayCompressor(Compressor, RelayBoard):
    pass

@cbpi.actor
class GPIOCompressor(Compressor, GPIOSimple):
    pass

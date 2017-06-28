from modules import cbpi
from modules.base_plugins.gpio_actor import *
from modules.core.props import Property
from datetime import datetime, timedelta

class Compressor(object):
    c_delay = Property.Number("Compressor Delay", True, 10, "minutes")
    compressor_on = False
    compressor_wait = datetime.utcnow()

    def on(self, power=0):
        if datetime.utcnow() >= self.compressor_wait:
            self.compressor_on = True
            super(Compressor, self).on(power)

    def off(self):
        if self.compressor_on:
            self.compressor_on = False
            self.compressor_wait = datetime.utcnow() + timedelta(minutes=int(self.c_delay))
        super(Compressor, self).off()

@cbpi.actor
class RelayCompressor(Compressor, RelayBoard):
    pass

@cbpi.actor
class GPIOCompressor(Compressor, GPIOSimple):
    pass

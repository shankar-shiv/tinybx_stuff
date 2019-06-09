import itertools
from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen.build import Resource,Subsignal,Pins
from nmigen.build import ResourceError
from nmigen.tools import bits_for

from boneless.gateware.core_fsm import BonelessFSMTestbench 

from uart import Loopback 
from processor import Boneless

from cores.larson import OnOff
from cores.breathe import Breathe

class Loop(Elaboratable):
    " Loopback uart on serial 0 and serial 1"
    def __init__(self,baud_rate=9600):
        self.baud_rate = baud_rate

    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        counter  = Signal(23)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += user_led.o.eq(counter[-1])
        
        clock = platform.lookup('clk16').clock
        serial = platform.request("serial",0)
        l = Loopback(serial.tx,serial.rx,clock.frequency,self.baud_rate)
        m.submodules.loopback = l

        serial2  = platform.request("serial",1)
        l2 = Loopback(serial2.tx,serial2.rx,clock.frequency,9600)
        m.submodules.loop2 = l2 

        return m


class CPU(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        b = Boneless() 
        m.submodules.boneless = b

        leds = []
        for n in itertools.count():
            try:
                leds.append(platform.request("user_led", n))
            except ResourceError:
                break

        leds = Cat(led.o for led in leds)
        m.d.comb += leds.eq(b.pins)
        
        
        clock = platform.lookup('clk16').clock
        serial = platform.request("serial",0)
        l = Loopback(serial.tx,serial.rx,clock.frequency,9600)
        m.submodules.loopback = l

        return m
    
class Extend(TinyFPGABXPlatform):
        resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
            Resource("serial",0,
                Subsignal("tx", Pins("19",conn=("gpio",0),dir="o")),
                Subsignal("rx", Pins("20",conn=("gpio",0),dir="i")),
            ),
        # Serial to AVR
            Resource("serial",1,
                Subsignal("tx", Pins("14",conn=("gpio",0), dir="o")),
                Subsignal("rx", Pins("15",conn=("gpio",0), dir="i")),
            ),
        ]

if __name__ == "__main__":
    from plat import BB
    platform = BB()
    platform.build(CPU(),do_program=True)

from nmigen import *

from boneless.gateware.core_fsm import BonelessFSMTestbench
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform 

class boneless_core(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        cpu = BonelessFSMTestbench()

        m.submodules.cpu = cpu

        return m

if __name__ == "__main__":
    platform = TinyFPGABXPlatform()
    platform.build(boneless_core(),build_dir='boneless')


# Automatically generated by nMigen d5ba26b. Do not edit.
set -e
yosys -q -l top.rpt top.ys
nextpnr-ice40 --quiet --placer heap --log top.tim --lp8k --package cm81 --json top.json --pcf top.pcf --pre-pack top_pre_pack.py --asc top.asc
icepack top.asc top.bin
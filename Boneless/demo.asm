J init
.macro on 
    MOVI R3,4095
    STX R3,R7,0
.endm

.macro off
    MOVI R3,0
    STX R3,R7,0
.endm


wait:
    MOVI R2,0
waiter:
    ADDI R2,1
    CMP R2,R1
    JE ex
    J waiter 
ex:
    JR R7,0

.macro WAIT
    JAL R7, wait
.endm

.macro long
    WAIT
    WAIT
    WAIT
    WAIT
    WAIT
    WAIT
.endm

init:
    MOVI R1, 24
blink:
    on
    long 
    long
    off
    long
    long
    long 
    long
J blink 


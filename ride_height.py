#!/usr/bin/python

import quick2wire.i2c as i2c

bus = i2c.I2CMaster()
adc_address1 = 0x68	#68=first i2c A/D chip
adc_address2 = 0x69	#69=second i2c A/D chip
adc_address3 = 0x6A	#board 2 first A/D chip


varDivisior = 16 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

#def changechannel(address, adcConfig):
#    bus.transaction(i2c.writing_bytes(address, adcConfig))
		
def getadcreading(address):
    h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
    t = h << 8 | m  
    # check if positive or negative number and invert if needed
    if (h > 128):
        t = ~(0x020000 - t)
    return t * varMultiplier

def setadc(addr,channel):	#incorporated channel change in setadc
    mode = 1
    sr = 2   # 0:240, 1:60, 2:15, 3:3.75 
    gain = 0 # gain = 2^x
		
    config_register = 0;
    config_register |= channel    << 5	#channel bits
    config_register |= mode << 4
    config_register |= sr   << 2
    config_register |= gain		
    bus.transaction(i2c.writing_bytes(addr, config_register))

start = 0.0
setadc(adc_address1,0)
setadc(adc_address2,0)
setadc(adc_address3,0)

def weight():
    #time.sleep(.01)
    return getadcreading(adc_address1)*505.07-341.5

def height():
    #setadc(adc_address2,0)
    #time.sleep(.01)
    return getadcreading(adc_address2)* 1.9476

def shock():
    #setadc(adc_address3,0)	#change to channel 1, does not work yet as it needs a delay or check status bit
    #time.sleep(.01)
    return getadcreading(adc_address3)

if __name__ == "__main__":
    import sys,time
    while True:
        h = "\rheight= %.6f " % height()
        w = " weight= %.6f " % weight()
        s = " shock= %.6f   " % shock()
        sys.stdout.write(h+w+s)
        time.sleep(0.1)


#!/usr/bin/python3

import sys
import quick2wire.i2c as i2c

bus = i2c.I2CMaster()
adc_address1 = 0x68	#68=first i2c A/D chip
adc_address2 = 0x69	#69=second i2c A/D chip
adc_address3 = 0x6A	#board 2 first A/D chip

CALIBRATION_FILE = "/etc/sharks.calibration"

ADC1_GAIN = 1.0
ADC2_GAIN = 1.0
ADC3_GAIN = 1.0
ADC1_OFFSET = 0.0
ADC2_OFFSET = 0.0
ADC3_OFFSET = 0.0

varDivisior = 16 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

def _write_settings_file(filename):
    with open(filename, "w") as f:
        f.write("%f, %f\n" % (ADC1_GAIN, ADC1_OFFSET))
        f.write("%f, %f\n" % (ADC2_GAIN, ADC2_OFFSET))
        f.write("%f, %f\n" % (ADC3_GAIN, ADC3_OFFSET))
                        

def writesettings(corner, gains, offsets):
    global ADC1_GAIN
    global ADC2_GAIN
    global ADC3_GAIN
    global ADC1_OFFSET
    global ADC2_OFFSET
    global ADC3_OFFSET

    if gains is not None:
        if   corner == "LF":
            gains = gains[0:8]
        elif corner == "LR":
            gains = gains[8:16]
        elif corner == "RF":
            gains = gains[16:24]
        elif corner == "RR":
            gains = gains[24:32]

        try:    
            ADC1_GAIN = float(gains[0])
        except:
            pass
        try:
            ADC2_GAIN = float(gains[1])
        except:
            pass
        try:
            ADC3_GAIN = float(gains[2])
        except:
            pass

        print(ADC1_GAIN,ADC2_GAIN,ADC3_GAIN)
        _write_settings_file(CALIBRATION_FILE)
        

def reloadsettings():
    global ADC1_GAIN
    global ADC2_GAIN
    global ADC3_GAIN
    global ADC1_OFFSET
    global ADC2_OFFSET
    global ADC3_OFFSET

    try:
        with open(CALIBRATION_FILE, "r") as f:
            line1 = f.readline()
            line2 = f.readline()
            line3 = f.readline()
            data1 = line1.split(",")
            data2 = line2.split(",")
            data3 = line3.split(",")
            ADC1_GAIN = float(data1[0])
            ADC2_GAIN = float(data2[0])
            ADC3_GAIN = float(data3[0])
            ADC1_OFFSET = float(data1[1])
            ADC2_OFFSET = float(data2[1])
            ADC3_OFFSET = float(data3[1])
            print(ADC1_GAIN, ADC2_GAIN, ADC3_GAIN, ADC1_OFFSET,ADC2_OFFSET,ADC3_OFFSET)
    except:
        print("Could not open calibration file")
        
reloadsettings()
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


def weight():
    return getadcreading(adc_address1)*ADC1_GAIN+ADC1_OFFSET
    #return getadcreading(adc_address1)*505.07-341.5

def height():
    #setadc(adc_address2,0)
    return getadcreading(adc_address2)*ADC2_GAIN+ADC2_OFFSET
    #return getadcreading(adc_address2)* 1.9476

def shock():
    #setadc(adc_address3,0)	#change to channel 1, does not work yet as it needs a delay or check status bit
    return getadcreading(adc_address3)*ADC3_GAIN+ADC3_OFFSET
    #return getadcreading(adc_address3)


try:
    setadc(adc_address1,0)
    setadc(adc_address2,0)
    setadc(adc_address3,0)
except IOError:
    sys.stderr.write("* Failed setting ADC addresses\n");

if __name__ == "__main__":
    import sys,time
    while True:

        try:
            h = "\rheight= %.6f " % height()
        except:
            h = "error"
            
        try:
            w = " weight= %.6f " % weight()
        except:
            w = "error"

        try:
            s = " shock= %.6f   " % shock()
        except:
            s = "error"
        sys.stdout.write(h+w+s)
        time.sleep(0.1)


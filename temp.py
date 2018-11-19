import machine
import time

adc = machine.ADC()
apin = adc.channel(pin='G5')

def getTemp():
    millivolts = apin.voltage()
    degC = (millivolts - 500.0) / 10.0 + 4
    return degC

def averageTemp():
    average = float(getTemp())
    for i in range(1,100):
        average = average + float(getTemp())
    return int(average)





while True:
    print(averageTemp())

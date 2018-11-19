from network import LoRa
import socket
import time
import binascii
import pycom
import ustruct
import machine

print('line 8')
    # takes battery voltage readings

adc = machine.ADC()
apin = adc.channel(pin='G5')
def getTemp():
    millivolts = apin.voltage()
    degC = (millivolts - 500.0) / 10.0 + 4
    return degC

def averageTemp():
    toaltemp = 0
    for i in 100:
        totaltemp = totaltemp + getTemp()
    return int(totaltemp/101)





print('line 31')
# disable LED heartbeat (so we can control the LED)
pycom.heartbeat(False)
# set LED to red
pycom.rgbled(0x7f0000)
print('line 36')
# lora config
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)
# access info
app_eui = binascii.unhexlify('70B3D57ED0013D54')
app_key = binascii.unhexlify('71CD15EFBCF23E05B70F94F19C5CEB66')
print('line 42')
# attempt join - continues attempts background
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=10000)

# wait for a connection
print('Waiting for network connection...')
while not lora.has_joined():
    pass

# we're online, set LED to green and notify via print
pycom.rgbled(0x007f00)
print('Network joined!')

# setup the socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.bind(1)

"""
# sending some bytes
print('Sending 1,2,3')
s.send(bytes([1, 2, 3]))
time.sleep(3)

#text is automatically converted to a string, data heavy (dont do it this way)
print('Sending "Hello World"')
s.send("Hello World!")
time.sleep(3)
"""

# check for a downlink payload, up to 64 bytes
rx_pkt = s.recv(64)

if len(rx_pkt) > 0:
    print("Downlink data on port 200:", rx_pkt)
    input("Downlink recieved, press any key to continue")

while True:
    data = int(averageTemp()*100)
    temperature = int(temperature)
    print("temperature:  ", data)
    # encode the packet, so that it's in BYTES (TTN friendly)
    # could be extended like this struct.pack('f',lipo_voltage) + struct.pack('c',"example text")
    packet = ustruct.pack('f',temperature)

    # send the prepared packet via LoRa
    s.send(packet)

    # example of unpacking a payload - unpack returns a sequence of
    #immutable objects (a list) and in this case the first object is the only object
    print ("Unpacked value is:", ustruct.unpack('f',packet)[0])

    time.sleep(3)

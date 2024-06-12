import serial
import time
import string
import pynmea2

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def gps():
    try:
        lon=0
        lat=0
        port="/dev/ttyUSB0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=str(ser.readline())
        print(newdata)
        GPGGA_data_available = newdata.find("$GPRMC")
        if (GPGGA_data_available>0):
                x=newdata.split("$GPRMC,",1)
                y=x[1].split(",")
                if len(y)>5:
                        lat=convert_to_degrees(float(y[2]))
                        lon=convert_to_degrees(float(y[4]))
                        #print("latitude=",lat)
                        #print("longitude=",lon)
        return lat,lon
    except:
        return 0,0

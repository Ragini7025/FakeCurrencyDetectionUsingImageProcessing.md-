import serial
import time
S = serial.Serial("COM5", baudrate=9600, timeout=2)

def sendSMS(moNum,g):
    try:
        print("Sending sms")
        #S.write(b"AT+CSMP=17,167,0,0")
        S.write(b"AT+CMGF=1\r")
        #Serial.write(b'AT+CMGF=1\r\n')
        time.sleep(1)
        nm=str(moNum)
        S.write(b"AT+CMGS=\"+91"+nm.encode()+b"\"\r")
        time.sleep(1)
        msg="accident occured coordinates: "+str(g)
        S.write(msg.encode())
        time.sleep(1)
        S.write(b"\x1A")
        time.sleep(3)
        print("sms send")
    except:
        print("sending sms failed")

    #sendSMS("hello",9633327256)

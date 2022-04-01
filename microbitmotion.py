import serial
from currentTime import getTimeDict


#ser = serial.Serial('COM4', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
ser = serial.Serial('COM4', 115200)

'''
Serial code
e = exit
b = bedroom
k = kitchen


'''


while True:
    try:
        
        ser_bytes = ser.read()
        if ser_bytes == b'e':
            print('Close')
            ser.close()
            break
        if ser_bytes != b'e':
            print(ser_bytes.decode("UTF-8"))

        # if ser_bytes != b'':
        #     decoded = ser_bytes.decode("UTF-8")

    except:
        print("Program stopped")
        break
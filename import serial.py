import serial
ser = serial.Serial('COM5', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

while True:
    try:
        ser_bytes = ser.read()
        if ser_bytes != b'':
            print(ser_bytes)
    except:
        print("Keyboard Interrupt")
        break
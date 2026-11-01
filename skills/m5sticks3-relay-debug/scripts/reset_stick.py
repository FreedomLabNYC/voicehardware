import serial, sys
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM1"
s = serial.Serial(port, 115200)
# classic RTS/DTR reset pulse for ESP32 USB-JTAG
s.dtr = False
s.rts = True
s.rts = False
s.close()
print("reset pulse sent on", port)

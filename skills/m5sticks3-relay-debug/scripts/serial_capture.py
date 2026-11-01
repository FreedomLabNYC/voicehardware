import serial, time, sys
port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM1"
secs = int(sys.argv[2]) if len(sys.argv) > 2 else 35
out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/stick_console.log"
s = serial.Serial(port, 115200, timeout=1)
t = time.time()
buf = b""
while time.time() - t < secs:
    buf += s.read(4096)
with open(out, "wb") as f:
    f.write(buf)
print(f"captured {len(buf)} bytes")

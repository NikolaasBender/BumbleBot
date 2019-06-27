import serial


class wire:
    def __init__(self, tty):
        self.ser = serial.Serial('/dev/' + tty, 9600, timeout=1)

    def send(self, dir):
        self.ser.write(bytearray(dir))

    def close(self):
        self.ser.close()

import serial

class SerialPort:
    def __init__(self):
        self.serial = serial.Serial()

    def open(self, portname, baudrate):
        self.serial.port = portname
        self.serial.baudrate = baudrate
        self.serial.open()
    
    def isOpen(self):
        return self.serial.is_open
    
    def close(self):
        self.serial.close()
    
    def write(self, message):
        message = message.strip()
        message += '\n'
        self.serial.write(message.encode('utf-8'))
    
    def read(self):
        return self.serial.readline().decode('utf-8')
    
    def inWaiting(self):
        return self.serial.inWaiting()
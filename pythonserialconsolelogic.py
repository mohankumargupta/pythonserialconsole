import serial
from Queue import Queue

class SimpleSerial:
	ser = None

	def connect(self,port, baud):
		self.ser = serial.Serial(port, baud, timeout=1)
		if self.ser.is_open:
			return True
		else:
			return False

	def disconnect(self):
		self.ser.close()

	def send(self, message):
		self.ser.write(message.encode('utf-8'))
		self.ser.write(b'\r')		
		self.ser.write(b'\n')

	def read(self):
		if (self.ser == None):
			return None
		else:
			return self.ser.read(1)		

	def readline(self):
		if (self.ser == None):
			return None
		else:
			return self.ser.readline()

	def getAllSerialPorts(self):
		ports = ["COM{}".format(i) for i in range(256)]
		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

def readSerialPort(simpleport, receiveText, queue):
	print("Started")
	while True:
		data = simpleport.readline()      
		if (data !=None and data):  
			#receiveText = receiveText + data
			#print(receiveText)
			queue.put(data)


'''
s = SimpleSerial()
s.connect("COM30", 9600)
s.send("Here's a line\r\nHere's another\r\n")
s.disconnect()
'''
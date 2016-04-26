import kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
import re
import threading
from pythonserialconsolelogic import SimpleSerial
from pythonserialconsolelogic import readSerialPort
from Queue import Queue
from kivy.clock import Clock

class PythonSerialConsole(BoxLayout):
	comPorts = ListProperty()
	isSerialOpen = NumericProperty(0)
	sendMessageTextInput = StringProperty()
	receiveMessageTextInput = StringProperty()

	def __init__(self, **kwargs):
		super(PythonSerialConsole, self).__init__(**kwargs)
		self.queue = Queue(maxsize=0)
		self.simpleserial = SimpleSerial()
		self.comPorts = self.simpleserial.getAllSerialPorts()
		t = threading.Thread(target=readSerialPort, args=(self.simpleserial,self.receiveMessageTextInput, self.queue))
		t.daemon = True
		t.start()
		Clock.schedule_interval(self.interval, 0.5)

	def interval(self, dt):
		if not self.queue.empty():
			self.receiveMessageTextInput = self.receiveMessageTextInput + self.queue.get() + "\r\n"


	def send_button_pressed(self):
		values = self.ids.values()
		textinput = values[0].__self__
		print(textinput.text)
		self.simpleserial.send(textinput.text)
		textinput.text = ""


	def button_pressed(self):
		values = self.ids.values()
		baud = values[3].__self__.text
		port = values[2].__self__.text		
		buttonText = values[1].__self__
		print("port:",port,"baud:",baud, "buttonText:", buttonText.text)
		
		if self.isSerialOpen:
				self.simpleserial.disconnect()
				buttonText.text = "Connect"
				self.isSerialOpen = 0
		else:
				connectSuccess = self.simpleserial.connect(port,baud)
				if not connectSuccess:
					message = "Serial connection failed."
					popup = Popup(title='Failed',
						content=Label(text=message),
						size_hint=(0.6, 0.6),
						)
					popup.open()
				else:
					buttonText.text = "Disconnect"
					self.isSerialOpen = 1



class PythonSerialConsoleWidget(GridLayout):
	tries = NumericProperty(0)
	def __init__(self, **kwargs):
		super(PythonSerialConsoleWidget,self).__init__(**kwargs)

	def button_pressed(self, textinput):
		self.tries = self.tries + 1
		bulls = PythonSerialConsolelogic.calculate_bulls(self.parent.answer,int(textinput))
		cows = PythonSerialConsolelogic.calculate_cows(self.parent.answer,int(textinput))
		result = str(bulls) + " bulls and " + str(cows) + " cows" 
		self.add_widget(Label(text=str(self.tries)) )
		self.add_widget(Label(text=textinput ))
		self.add_widget(Label(text=result))
		self.pos_hint = ({'x':0, 'center_y':0.7 + 0.025*(1-self.tries)})
		self.size_hint = (1,0.05 * self.tries )




class PythonSerialConsoleApp(App):
	def build(self):
		self.icon = "arduino_icon.ico"
		Config.set('graphics', 'width', '750') 
		Config.set('graphics', 'height', '315')
		return PythonSerialConsole()


if __name__ == '__main__':
	PythonSerialConsoleApp().run()

import os
from gpiozero import Motor
from time import sleep
from inputs import get_gamepad
import inputs
import datetime


EVENT_ABB = (
	# D-PAD, aka HAT
	('Absolute-ABS_HAT0X', 'HX'),
	('Absolute-ABS_HAT0Y', 'HY'),

	# Face Buttons
	('Key-BTN_NORTH', 'N'),
	('Key-BTN_EAST', 'E'),
	('Key-BTN_SOUTH', 'S'),
	('Key-BTN_WEST', 'W'),

	# Other buttons
	('Key-BTN_THUMBL', 'THL'),
	('Key-BTN_THUMBR', 'THR'),
	('Key-BTN_TL', 'TL'),
	('Key-BTN_TR', 'TR'),
	('Key-BTN_TL2', 'TL2'),
	('Key-BTN_TR2', 'TR3'),
	('Key-BTN_MODE', 'M'),
	('Key-BTN_START', 'ST'),

	# PiHUT SNES style controller buttons
	('Key-BTN_TRIGGER', 'N'),
	('Key-BTN_THUMB', 'E'),
	('Key-BTN_THUMB2', 'S'),
	('Key-BTN_TOP', 'W'),
	('Key-BTN_BASE3', 'SL'),
	('Key-BTN_BASE4', 'ST'),
	('Key-BTN_TOP2', 'TL'),
	('Key-BTN_PINKIE', 'TR')
)




# This is to reduce noise from the PlayStation controllers
# For the Xbox controller, you can set this to 0
MIN_ABS_DIFFERENCE = 0




class gpControl(object):
	def __init__(self, gamepad=None, abbrevs=EVENT_ABB):
		self.btn_state = {}
		self.old_btn_state = {}
		self.abs_state = {}
		self.old_abs_state = {}
		self.abbrevs = dict(abbrevs)
		for key, value in self.abbrevs.items():
			if key.startswith('Absolute'):
				self.abs_state[value] = 0
				self.old_abs_state[value] = 0
			if key.startswith('Key'):
				self.btn_state[value] = 0
				self.old_btn_state[value] = 0
		self._other = 0
		self.gamepad = gamepad
		if not gamepad:
			self._get_gamepad()
			
	def _get_gamepad(self):
		"""Get a gamepad object."""
		try:
			self.gamepad = inputs.devices.gamepads[0]
		except IndexError:
			raise inputs.UnpluggedError("No gamepad found.")

	def process_events(self):
		"""Process available events."""
		try:
			events = self.gamepad.read()
		except EOFError:
			events = []
		for event in events:
			return self.process_event(event)
		return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


	def process_event(self, event):
		"""Process the event into a state."""
		if event.ev_type == 'Sync':
			return
		if event.ev_type == 'Misc':
			return
		key = event.ev_type + '-' + event.code
		try:
			abbv = self.abbrevs[key]
		except KeyError:
			abbv = self.handle_unknown_event(event, key)
			if not abbv:
				return
		if event.ev_type == 'Key':
			self.old_btn_state[abbv] = self.btn_state[abbv]
			self.btn_state[abbv] = event.state
		if event.ev_type == 'Absolute':
			self.old_abs_state[abbv] = self.abs_state[abbv]
			self.abs_state[abbv] = event.state
		return self.output_state(event.ev_type, abbv)


	def output_state(self, ev_type, abbv):
		"""Print out the output state."""
		if ev_type == 'Key':
			if self.btn_state[abbv] != self.old_btn_state[abbv]:
				#print(self.format_state(), "key")
				return self.format_state()

		if abbv[0] == 'H':
			#print(self.format_state(), "H")
			return self.format_state()

		difference = self.abs_state[abbv] - self.old_abs_state[abbv]
		if (abs(difference)) > MIN_ABS_DIFFERENCE:
			#print(self.format_state())
			tmp = self.format_state()
			#print(type(tmp))
			return tmp


	def format_state(self):
		"""Format the state."""
		#output_string = ""
		output = []
		#VALUE IS A TUPLE
		for value in self.abs_state.items():
			#output_string += key + ':' + '{:>4}'.format(str(value) + ' ')
			output.append(value)

		for value in self.btn_state.items():
			#output_string += key + ':' + str(value) + ' '
			output.append(value)

		#print(type(output))
		return output #, output_string


	def handle_unknown_event(self, event, key):
		"""Deal with unknown events."""
		if event.ev_type == 'Key':
			new_abbv = 'B' + str(self._other)
			self.btn_state[new_abbv] = 0
			self.old_btn_state[new_abbv] = 0
		elif event.ev_type == 'Absolute':
			new_abbv = 'A' + str(self._other)
			self.abs_state[new_abbv] = 0
			self.old_abs_state[new_abbv] = 0
		else:
			return None

		self.abbrevs[key] = new_abbv
		self._other += 1

		return self.abbrevs[key]



Lmotor = Motor(forward=26, backward=19)
Rmotor = Motor(forward=13, backward=6)


last = []

def rC(ctrl):
	global last
	speed = 0.5
	#   0      1       2        3        4        5      6     7      8
	#[dpadX, dpadY, lstickY, lstickX, rstickY, rstickX, Xbtn, Abtn, Bbtn]
	#THERES MORE BUT I THINK THIS IS ALL I NEED
	xpo = ('HX', 1)
	xz = ('HX', 0)
	xno = ('HX', -1)
	ypo = ('HY', 1)
	yz = ('HY', 0)
	yno = ('HY', -1)
	ao = ('E', 1)
	az = ('E', 0)

	if xpo in ctrl:
		Lmotor.forward(speed)
		Rmotor.stop()
	if xno in ctrl:
		Rmotor.forward(speed)
		Lmotor.stop()
	if yno in ctrl:
		Rmotor.forward(speed)
		Lmotor.forward(speed)
	if ypo in ctrl:
		Rmotor.backward(speed)
		Lmotor.backward(speed)
	if ao in ctrl:
		print("click!")
		snap()
	# if ctrl[8] == 1:
	# 	print("!!!!!!!!!!!!!!!AUTO PILOT ENGAGED!!!!!!!!!!!!!!!")
	# 	autoPilot()
	if xz in ctrl and xz not in last:
		Lmotor.stop()
		Rmotor.stop()
	if yz in ctrl and yz not in last:
		Lmotor.stop()
		Rmotor.stop()
	if yno in ctrl and xpo in ctrl:
		Rmotor.forward(speed*0.6)
		Lmotor.forward(speed)
	if yno in ctrl and xno in ctrl:
		Rmotor.forward(speed)
		Lmotor.forward(speed*0.6)

	last = ctrl
	return 



def snap():
	file = datetime.datetime.now().strftime('%Y-%m-%d_%I:%M:%S%p') + ".jpeg"
	pic = "streamer -q -s 128x128 -o images/" + file
	#bw = "bw.cpp " + file
	cmd = pic #+ "&&" + bw
	os.system(cmd)
	return




def autoPilot():
	cmd = "python3 Bumble2.py"
	os.system(cmd)
	print("!!!!!!!!!!!!!!!AUTO PILOT DISENGAGED!!!!!!!!!!!!!!!")
	return




def main():
	"""Process all events forever."""
	ref = []
	jstest = gpControl()
	while 1:
		tmp = jstest.process_events()
		#print(type(tmp), "main")
		if type(tmp) == type(ref):
			rC(tmp)






if __name__ == "__main__":
	main()

# A0 - 127 = 0 is left joystick at center -127 is joystick all the way up and 127 is joystick all the way down

# HY -1 is dpad up
# HX -1 is dpad left

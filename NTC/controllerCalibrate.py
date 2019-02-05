print("starting")
from controller import *
from time import sleep

jstest = gpControl()
print("setup complete")
while True:
	print("testing")
	tmp = jstest.process_events()
	if tmp != None:
		print(tmp)
	sleep(1)
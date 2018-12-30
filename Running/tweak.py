from gpiozero import DistanceSensor, Motor, Button
from time import sleep,time

FMsensor = DistanceSensor(echo = 21, trigger = 20)


#min distance is 1ft 30cm

high = 0.6
low = 0.1
ok = 0.1337
limit = 5
tot = 10000
waiter = 0.005


def Ds():
	avg = 0.0
	cnt = 0.0
	for x in range(0,10):
		tmp = FMsensor.distance
		if cnt == limit:
			return avg / x
		if tmp < high and tmp > low:
			avg += tmp
		else:
			cnt += 1
			x -= 1
		sleep(0.00001)
	return avg/10

def Ds2():
	avg = 0.0
	for x in range(0,10):
		tmp = FMsensor.distance
		if tmp < high and tmp > low:
			avg += tmp
		else:
			x -= 1
		sleep(0.00001)
	return avg/10


def Ds3():
	avg = 0.0
	for x in range(0,10):
		tmp = FMsensor.distance
		if tmp < high:
			avg += tmp
		sleep(0.00001)
	return avg/10



def Ds4():
	return FMsensor.distance




def diff(lA):
	maximum = 0.001
	minimum = 1.0
	for i in range(0,tot):
		if float(lA[i]) > float(maximum):
			maximum = lA[i]
		if float(lA[i]) < float(minimum) and float(lA[i]) != 0.0:
			minimum = lA[i]

	return ((maximum - minimum), minimum, maximum)


def countz(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt


def bad(a):
	cnt = 0
	for i in range(0,tot):
		if a[i] == 0.0:
			cnt += 1
	return cnt / tot




dvec = []
dvec2 = []
dvec3 = []
dvec4 = []



start = time()

for i in range(0,tot):
	dvec.append(Ds())

end = time()


sleep(20)


start1 = time()

for i in range(0,tot):
	dvec2.append(Ds2())

end1 = time()


sleep(20)


start2 = time()

for i in range(0,tot):
	dvec3.append(Ds3())

end2 = time()



start3 = time()

for i in range(0,tot*10):
	dvec4.append(Ds4())

end3 = time()






d1 = (diff(dvec), countz(dvec), bad(dvec), (end - start))
d2 = (diff(dvec2), countz(dvec2), bad(dvec2), (end1 - start1))
d3 = (diff(dvec3), countz(dvec3), bad(dvec3), (end2 - start2))
d4 = (diff(dvec4), countz(dvec4), bad(dvec4), (end3 - start3))


print("ds delta   ds 0s    ds bad data    test time: ")
print(d1)
print(d2)
print(d3)
print(d4)

import math
from functools import reduce


TEST_INPUT = "7,13,x,x,59,x,31,19"

def findWaitTime(estimated_time, busids):
	buses = busids.split(",")
	earliest_busid = 0
	earliest_time = 0
	for bus in buses:
		if bus != "x":
			print(bus)
			busid = int(bus)
			divisor = math.floor(estimated_time / busid)
			dep_time = busid * (divisor + 1)
			if earliest_time == 0 or dep_time < earliest_time:
				earliest_time = dep_time
				earliest_busid = busid
			print(dep_time)
	print("Result:", earliest_busid, earliest_time, earliest_busid * (earliest_time - estimated_time))
	return earliest_busid * (earliest_time - estimated_time)

def findOffsetMatch(busids, opt_start = 0):
	buses = busids.split(",")
	start = int(buses[0]) 
	if (opt_start > 0):
		start = opt_start
	while checkOffsets(start, buses) == False:
		start += int(buses[0])
		print(start)
	return start

def checkOffsets(start, busarray):
	for i in range(1, len(busarray)):
		if busarray[i] != "x":
			if (start + i) % int(busarray[i]) != 0:
				return False

	return True

def solveWithChineseRemainderTheorem(input):
	busids = input.split(",")
	n = []
	a = []
	for i in range(len(busids)):
		if busids[i] != "x":
			print(i, int(busids[i]))
			a.append(int(busids[i]) - i)
			n.append(int(busids[i]))
	result = chinese_remainder(n, a)
	print("mods", result % 7, result % 13, result % 59, result % 31, result % 19)
	print(result)
	return result

def chinese_remainder(n, a):
	print(n, a)
	sum = 0
	prod = reduce(lambda a, b: a*b, n)
	for n_i, a_i in zip(n, a):
		p = prod // n_i # floor
		print("p", prod, p, n_i)
		sum += a_i * mul_inv(p, n_i) * p
	print(sum % prod)
	return sum % prod
 
def mul_inv(a, b):
	b0 = b
	x0, x1 = 0, 1
	if b == 1: return 1
	while a > 1:
		print("a, b", a, b)
		q = a // b
		a, b = b, a%b
		x0, x1 = x1 - q * x0, x0
	if x1 < 0: x1 += b0
	return x1

def testFindWaitTime():
	if findWaitTime(939, TEST_INPUT) == 295:
		print("testFindWaitTime Pass")
	else:
		print("testFindWaitTime Fail")	

def testFindOffsetMatch():
	print(checkOffsets(1068781, TEST_INPUT.split(",")))
	if findOffsetMatch(TEST_INPUT) == 1068781:
		print("testFindOffsetMatch Pass")
	else:
		print("testFindOffsetMatch Fail")

def testSolveWithChineseRemainderTheorem():
	result = 1068781
	if solveWithChineseRemainderTheorem(TEST_INPUT) == 1068781:
		print("testSolveWithChineseRemainderTheorem Pass")
	else:
		print("testSolveWithChineseRemainderTheorem Fail")


def main():
	#testFindWaitTime()
	#testFindOffsetMatch()
	testSolveWithChineseRemainderTheorem()

	f = open('data/day13_input.txt', 'r')
	lines = f.readlines()

	earliest_time = int(lines[0].strip())
	busids = lines[1].strip()

	# findWaitTime(earliest_time, busids)
	# print(findOffsetMatch(busids, 41000000000))
	print(solveWithChineseRemainderTheorem(busids))

if __name__ == '__main__':
	main()

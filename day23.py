INPUT = 219748365
TEST_INPUT = 389125467

# - The crab picks up the three cups that are immediately 
# clockwise of the current cup. They are removed from the circle; 
# cup spacing is adjusted as necessary to maintain the circle.
# - The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
# If this would select one of the cups that was just picked up, the crab will keep subtracting one 
# until it finds a cup that wasn't just picked up. If at any point in this process the value goes 
# below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
# - The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. 
# - They keep the same order as when they were picked up.
# - The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
def playCrabCup(input, num_rounds):
	cuparray = toCupArray(input)
	cups = toCupDict(cuparray)
	min_cup = min(cuparray)
	max_cup = max(cuparray)
	current_cup = cuparray[0]

	cupresult = doPlayCrabCup(min_cup, max_cup, current_cup, cups, num_rounds)
	result = toCrabInt(cupresult[:8])
	print("RESULT:", result)
	return result

def doPlayCrabCup(min_cup, max_cup, current_cup, cups, num_rounds):

	for i in range(num_rounds):
		#print()
		#print("-- move", i+1, "--")
		#printCups(cups)
		#print("current cup", current_cup)

		# pickup next 3 cups
		pickup_array = []
		pickup_cup = cups[current_cup]
		pickup_array.append(pickup_cup)
		for j in range(2):
			pickup_cup = cups[pickup_cup]
			pickup_array.append(pickup_cup)

		# print("pick up: ", pickup_array)

		# now find destination
		dest = current_cup - 1
		if current_cup == min_cup:
			dest = max_cup
		while dest in pickup_array:
			dest -= 1
			if dest < min_cup:
				dest = max_cup
		# print("destination:", dest)

		# now remove and insert the cups
		cups[current_cup] = cups[pickup_array[2]]
		destnext = cups[dest]
		cups[dest] = pickup_array[0]
		cups[pickup_array[2]] = destnext 

		current_cup = cups[current_cup]
	print("CUPS", cups[1], cups[cups[1]])
	return printCups(cups)


def playCrabCup2(input, num_rounds):
	cuparray = toCupArray(input)
	cups = toCupDict(cuparray)
	current_cup = cuparray[0]
	cups[cuparray[8]] = 10
	for i in range(10, 1000000):
		cups[i] = i+1
	cups[1000000] = cuparray[0]
	printCups(cups)

	cupresult = doPlayCrabCup(1, 1000000, current_cup, cups, num_rounds)
	result = cupresult[0] * cupresult[1]
	print("RESULT", result)
	return result

def printCups(cupdict):
	cur = 1
	cuparray = []
	for i in range(9):
		cur = cupdict[cur]
		cuparray.append(cur)
	print(cuparray)
	return cuparray

def toCupDict(cuparray):
	cups = dict()
	for i in range(8):
		cups[cuparray[i]] = cuparray[i+1] # next
	cups[cuparray[8]] = cuparray[0] 
	print(cups)
	return cups

def toCupArray(num):
	return [int(x) for x in str(num)]

def toCrabInt(order_array):
	string = "".join([str(x) for x in order_array])
	return int(string)

def testPlayCrabCup():
	result_after_10 = 92658374
	result_after_100 = 67384529
	if playCrabCup(TEST_INPUT, 10) == result_after_10 and playCrabCup(TEST_INPUT, 100) == result_after_100:
		print("testPlayCrabCup Pass")
	else:
		print("testPlayCrabCup Fail")

def testPlayCrabCup2():
	result = 149245887792
	if playCrabCup2(TEST_INPUT, 10000000) == result:
		print("testPlayCrabCup2 Pass")
	else:
		print("testPlayCrabCup2 Fail")

def main():
	# testPlayCrabCup()
	# playCrabCup(INPUT, 100)
	# testPlayCrabCup2()
	playCrabCup2(INPUT, 10000000)

if __name__ == '__main__':
	main()
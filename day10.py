TEST_INPUT = [
			16,
			10,
			15,
			5,
			1,
			11,
			7,
			19,
			6,
			12,
			4,
]

TEST_INPUT2 = [
				28,
				33,
				18,
				42,
				31,
				14,
				46,
				20,
				48,
				47,
				24,
				23,
				49,
				45,
				19,
				38,
				39,
				11,
				1,
				32,
				25,
				35,
				8,
				17,
				7,
				9,
				4,
				2,
				34,
				10,
				3,
]

TEST_INPUT_3 = [
			3, 4, 5, 6, 7, 8
]

def findVoltageDiffs(input):
	input.sort()
	print(input)
	count1diffs = 0
	count3diffs = 1
	last = 0
	for adapter in input:
		diff = adapter - last
		last = adapter
		if diff == 1:
			count1diffs += 1
		elif diff == 3:
			count3diffs += 1
		print("adapter:", adapter, diff)

	return count1diffs * count3diffs

def countDistinctPaths(input):
	input.sort()
	print(input, len(input))
	pathMap = dict()
	sum = findLeaves(input, -1, 0, pathMap)
	print("sum", sum)
	return sum

def findLeaves(input, startpos, lastval, pathMap):
	sum = 0
	if startpos >= (len(input) - 1):
		# print("leaf: ", startpos)
		pathMap[startpos] = 1
		return 1

	childpos = startpos + 1
	child = input[childpos]
	print("findLeaves", "startpos", startpos, "last", lastval, "childpos", childpos, "child", child)

	while (child - lastval <= 3 and childpos < len(input)):
		if (childpos in pathMap and pathMap[childpos] > 0):
			print("childpos in map", childpos)
			sum += 1
		else:
			sum += findLeaves(input, childpos, child, pathMap)
		if childpos >= len(input) - 1:
			print("childpos end", childpos)
			break
		childpos += 1
		child = input[childpos]
	return sum

def iterativeCountPaths(input):
	input.sort()
	input[:0] = [0]
	lastentry = input[-1] + 3
	input.append(lastentry)
	print(input)
	cache = { input[-2]: 1, input[-3]: 1 } 

	for i in range(len(input) - 4, -1, -1): # starts at 
		print(input[i], input[i+1], input[i+2], input[i+3])
		count = cache[input[i+1]]
		if input[i+3] - input[i] <=3:
			print("a")
			count += cache[input[i+2]] + cache[input[i+3]] 
		elif input[i+2] - input[i] <=3:
			print("b")
			count += cache[input[i+2]] 
		cache[input[i]] = count

	return cache[input[0]]



def testFindVoltageDiffs():
	if findVoltageDiffs(TEST_INPUT) == 35 and findVoltageDiffs(TEST_INPUT2) == 220:
		print("testFindVoltageDiffs Pass")
	else:
		print("testFindVoltageDiffs Fail")

def testIterativeCountPaths():
	if iterativeCountPaths(TEST_INPUT) == 8 and iterativeCountPaths(TEST_INPUT2) == 19208:
		print("testIterativeCountPaths Pass")
	else:
		print("testIterativeCountPaths Fail")

def testCountDistinctPaths():
	if countDistinctPaths(TEST_INPUT) == 8 and countDistinctPaths(TEST_INPUT2) == 19208:
		print("testCountDistinctPaths Pass")
	else:
		print("testCountDistinctPaths Fail")		

def main():
	# testFindVoltageDiffs()
	# testCountDistinctPaths()
	testIterativeCountPaths()

	inputList = []

	f = open('data/day10_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(int(line.strip()))

	print("len:", len(inputList))
	# # print(findVoltageDiffs(inputList))
	print(iterativeCountPaths(inputList))


if __name__ == '__main__':
	main()
TEST_INPUT = [
			35,
			20,
			15,
			25,
			47,
			40,
			62,
			55,
			65,
			95,
			102,
			117,
			150,
			182,
			127,
			219,
			299,
			277,
			309,
			576,
]
def findFirstInvalidNum(input, lastcount):
	lastSet = set()
	invalid = 0
	for i in range(lastcount):
		lastSet.add(input[i])
	for j in range(lastcount, len(input)):
		num = input[j]
		print(num, lastSet)
		if checkIfSum(lastSet, num) == False:
			return num
		lastSet.remove(input[j-lastcount])
		lastSet.add(num)
	return 0

def checkIfSum(lastSet, num):
	for entry in lastSet:
		entry2 = num - entry
		if entry2 != entry and entry2 in lastSet:
			return True
	return False

def findContinguousRange(input, num):
	for i in range(len(input)):
		sum = 0
		pos = i
		min = input[i]
		max = 0
		while sum < num:
			if input[pos] > max:
				max = input[pos]
			if input[pos] < min:
				min = input[pos]
			sum += input[pos]
			# print("sum", sum)
			pos += 1
		# print(sum, i, pos-1, max + min)
		if sum == num:
			return max + min
	return 0


def testFindFirstInvalidNum():
	if findFirstInvalidNum(TEST_INPUT, 5) == 127:
		print("testFindFirstInvalidNum Pass")
	else:
		print("testFindFirstInvalidNum Fail")		

def testFindContinguousRange():
	if findContinguousRange(TEST_INPUT, 127) == 62:
		print("testFindContinguousRange Pass")
	else:
		print("testFindContinguousRange Fail")		

def main():
	testFindFirstInvalidNum()
	testFindContinguousRange()

	inputList = []

	f = open('data/day9_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(int(line.strip()))

	print("len:", len(inputList))
	invalidNum = findFirstInvalidNum(inputList, 25)
	print(findContinguousRange(inputList, invalidNum))


if __name__ == '__main__':
	main()
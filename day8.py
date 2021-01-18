TEST_INPUT = [
			"nop +0",
			"acc +1",
			"jmp +4",
			"acc +3",
			"jmp -3",
			"acc -99",
			"acc +1",
			"jmp -4",
			"acc +6"
]

def findFinalAccumulatorValue(input):
	executed = set()
	acc = 0
	pos = 0
	while pos not in executed and pos < len(input):
		executed.add(pos)
		instruction = input[pos]
		print("pos:", pos, instruction)

		if instruction.find("acc") >= 0:
			acc += parseNum(instruction)
			pos += 1
		elif instruction.find("jmp") >= 0:
			pos += parseNum(instruction)
		else:
			pos += 1

	print("acc:", acc, "pos", pos)
	print(executed)
	return (acc, bool(pos == len(input)))

def fixProgram(input):
	for pos in range(len(input)):
		instruction = input[pos]
		if instruction.find("nop") >= 0:
			modified = input.copy()
			modified[pos] = instruction.replace("nop", "jmp")
		elif instruction.find("jmp") >= 0:
			modified = input.copy()
			modified[pos] = instruction.replace("jmp", "nop")
		else:
			continue

		result = findFinalAccumulatorValue(modified)
		print(result)
		if result[1] == True:
			print("modified", instruction)
			return result[0]

	return 0


def parseNum(instruction):
	return int(instruction[4:])

def testFindFinalAccumulatorValue():
	if findFinalAccumulatorValue(TEST_INPUT)[0] == 5 and findFinalAccumulatorValue(TEST_INPUT)[1] == False:
		print("testFindFinalAccumulatorValue Pass")
	else:
		print("testFindFinalAccumulatorValue Fail")

def testFixProgram():
	if fixProgram(TEST_INPUT) == 8:
		print("testFixProgram Pass")
	else:
		print("testFixProgram Fail")


def main():
	testFindFinalAccumulatorValue()
	testFixProgram()

	inputList = []

	f = open('data/day8_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(line.strip())

	print("len:", len(inputList))
	print("findFinalAccumulatorValue: ", findFinalAccumulatorValue(inputList))
	print("fixProgram: ", fixProgram(inputList))



if __name__ == '__main__':
	main()
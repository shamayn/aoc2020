import re
from itertools import product

TEST_INPUT = [ "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 
		"mem[8] = 11", "mem[7] = 101", "mem[8] = 0" ]

TEST_INPUT_2 = [ 
		"mask = 000000000000000000000000000000X1001X",
		"mem[42] = 100",
		"mask = 00000000000000000000000000000000X0XX",
		"mem[26] = 1"
]

def intToBinary(value):
    return f"{int(value):036b}"

def findBitmaskSum(input):
	currmask = ""
	mask0 = 0
	mask1 = 0
	addresses = dict()

	for row in input:
		if row.find("mask") == 0:
			currmask = row[7:]
			(mask0, mask1) = getMaskV1(currmask)
			print("mask", mask0, mask1)


		elif row.find("mem") == 0:
			match = re.findall(r'\d+', row)
			index = int(match[0])
			num = int(match[1])
			maskednum = (num | mask1) & mask0
			print("num  ", '{0:036b}'.format(num))
			print("maskednum ", '{0:036b}'.format(maskednum))

		addresses[index] = maskednum
	print(addresses)

	sum = 0
	for add in addresses.values():
		sum += add
	return sum

def findFloatingBitmaskSum(input):
	currmask = ""
	addresses = dict()
	masksx = []

	for row in input:
		if row.find("mask") == 0:
			currmask = row[7:]

		elif row.find("mem") == 0:
			match = re.findall(r'\d+', row)
			index = int(match[0])
			val = int(match[1])
			maskedaddr = applyAddressMask(intToBinary(index), currmask)

			print("addr        ", '{0:036b}'.format(index), index)
			print("maskedaddr  ", maskedaddr)
			masksx = getFloatingMasks(maskedaddr)

			for maskx in masksx:
				addresses[int(maskx, 2)] = val

			#addresses[index] = maskednum
	print(addresses)

	sum = 0
	for add in addresses.values():
		sum += add
	return sum

def applyAddressMask(binary, mask):
	newbinary = ""
	for i, j in enumerate(binary):
		if mask[i] == "X":
			newbinary += "X"
		if mask[i] == "0":
			newbinary += j
		if mask[i] == "1":
			newbinary += "1" 
	return newbinary

def getMaskV1(maskinstruction):
	mask0 = 0
	mask1 = 0

	print(maskinstruction)
	for i in range(len(maskinstruction)-1, -1, -1):
		if (maskinstruction[i] == "1"):
			mask1 += 2**(35-i)

	for i in range(len(maskinstruction)-1, -1, -1):
		if (maskinstruction[i] != "0"):
			mask0 += 2**(35-i)

	return (mask0, mask1)


def getFloatingMasks(maskinstruction):
	countx = maskinstruction.count("X")
	maskinstructions = []

	sequences = [x for x in product([0, 1], repeat=countx)]
	print("sequences", sequences)
	for seq in sequences:
		xpos = 0
		newinstruction = maskinstruction
		for i, j in enumerate(maskinstruction):
			if j == "X":
				# replace
				newinstruction = newinstruction[:i] + str(seq[xpos]) + newinstruction[i+1:]
				xpos += 1
		maskinstructions.append(newinstruction)
	print("maskinstructions", maskinstructions)

	return maskinstructions



def testFindBitmaskSum():
	result = 165
	if findBitmaskSum(TEST_INPUT) == result:
		print("testFindBitmaskSum Pass")
	else:
		print("testFindBitmaskSum Fail")

def testFindFloatingSum():
	result = 208
	if findFloatingBitmaskSum(TEST_INPUT_2) == result:
		print("testFindFloatingSum Pass")
	else:
		print("testFindFloatingSum Fail")

def main():
	#testFindBitmaskSum()
	testFindFloatingSum()

	f = open('data/day14_input.txt', 'r')
	lines = f.readlines()

	instructions = []
	for line in lines:
		instructions.append(line.strip())

	#print(findBitmaskSum(instructions))
	print(findFloatingBitmaskSum(instructions))

if __name__ == '__main__':
	main()
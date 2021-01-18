import sys

def findProductOf2020Sum(numberSet):
	return findProductofSum(2020, numberSet)

def findProductofSum(sum, numberSet):
	for num in numberSet:
		diff = sum - num
		if diff in numberSet:
			return num * diff
	return 0

def findProductOf2020TripleSum(numberSet):
	for num in numberSet:
		diff1 = 2020 - num
		product1 = findProductofSum(diff1, numberSet)
		if product1 > 0:
			return product1 * num;
	return 0

def testProductOf2020Sum():
	numberSet = set([1721, 979, 366, 299, 675, 1456])
	if findProductOf2020Sum(numberSet) == 514579: 
		print("Pass")
	else:
		print("Fail")

def testProductOf2020TripleSum():
	numberSet = set([1721, 979, 366, 299, 675, 1456])
	if findProductOf2020TripleSum(numberSet) == 241861950: 
		print("Pass")
	else:
		print("Fail")



def main(argv):
	testProductOf2020Sum()
	testProductOf2020TripleSum()

	inputSet = set()

	f = open('data/day1_input.txt', 'r')
	lines = f.readlines()
	for line in lines:
		inputSet.add(int(line))
	print(findProductOf2020Sum(inputSet))
	print(findProductOf2020TripleSum(inputSet))





if __name__ == '__main__':
	main(sys.argv)
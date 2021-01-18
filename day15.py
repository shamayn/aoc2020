
def findNthNumber(startnumbers, n):
	lastspokenindices = dict()
	for i, num in enumerate(startnumbers):
		lastspokenindices[num] = [i]
	#print(lastspokenindices)

	current = 0
	prev = startnumbers[len(startnumbers) - 1]
	for j in range(len(lastspokenindices), n):
		previndices = lastspokenindices[prev]
		#print("prev", prev, previndices)

		size = len(previndices)
		if size == 1:
			current = 0
		elif size > 1:
			current = previndices[-1] - previndices[-2]
		if current in lastspokenindices:
			currentindices = lastspokenindices[current]
			currentindices.append(j)
			lastspokenindices[current] = currentindices
		else:
			lastspokenindices[current] = [j]
		prev = current
		#print("current", current, currentindices, lastspokenindices)
	return current


def testFindNthNumber():
	result = 436
	if findNthNumber([0, 3, 6], 2020) == result:
		print("testFindNthNumber Pass")
	else:
		print("testFindNthNumber Fail")

def main():
	#testFindNthNumber()
	#print(findNthNumber([0,5,4,1,10,14,7], 2020))
	print(findNthNumber([0,5,4,1,10,14,7], 30000000))


if __name__ == '__main__':
	main()

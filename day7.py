
TEST_INPUT = [ "light red bags contain 1 bright white bag, 2 muted yellow bags.",
			"dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
			"bright white bags contain 1 shiny gold bag.",
			"muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
			"shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
			"dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
			"vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
			"faded blue bags contain no other bags.",
			"dotted black bags contain no other bags." ]

TEST_RULES = {
 			"light red" : "1 bright white,2 muted yellow",
			"dark orange" : "3 bright white,4 muted yellow",
			"bright white" : "1 shiny gold",
			"muted yellow": "2 shiny gold,9 faded blue",
			"shiny gold" : "1 dark olive,2 vibrant plum",
			"dark olive" : "3 faded blue,4 dotted black",
			"vibrant plum" : "5 faded blue,6 dotted black",
			"faded blue" : "",
			"dotted black" : ""
}

TEST_INPUT2 = [
			"shiny gold bags contain 2 dark red bags.",
			"dark red bags contain 2 dark orange bags.",
			"dark orange bags contain 2 dark yellow bags.",
			"dark yellow bags contain 2 dark green bags.",
			"dark green bags contain 2 dark blue bags.",
			"dark blue bags contain 2 dark violet bags.",
			"dark violet bags contain no other bags.",
]

def countColorsForGoldBags(ruleDict):
	containingColors = set()
	findAllParents("shiny gold", containingColors, ruleDict)
	return len(containingColors)

def findAllParents(color, containingColors, ruleDict):
	#print("findParents", color, containingColors)
	if color == "":
		return
	for rule in ruleDict:
		children = ruleDict[rule]
		if children.find(color) > -1:
			if rule not in containingColors:
				containingColors.add(rule)
				findAllParents(rule, containingColors, ruleDict)

def countContainedBags(color, ruleDict):
	return sumAllChildren(color, ruleDict) - 1

def sumAllChildren(color, ruleDict):
	children = ruleDict[color].split(",")
	sum = 1
	if children == [""]:
		return sum
	print("sumAllChildren:", color, children, sum)
	for child in children:
		numAndColor = extractNumAndColor(child)
		sum += numAndColor[0] * sumAllChildren(numAndColor[1], ruleDict)
		print("sum:", sum, numAndColor)
	return sum

def extractNumAndColor(entry):
	numAndColor = entry.split(" ")
	num = int(numAndColor[0])
	color = numAndColor[1] + " " + numAndColor[2]
	return (num, color)



def parseBagInput(input):
	ruleDict = dict()
	for rule in input:
		contain = rule.find("contain")
		parent = extractColors(rule[0:contain-6])
		children = rule[contain+8:len(rule)-1].split(", ")
		childcolors = ""
		for child in children:
			childcolors += extractColors(child) + ","

		ruleDict[parent] = childcolors[:-1].strip()
	print(ruleDict)
	return ruleDict

def extractColors(text):
	if text.find("no") == 0:
		return ""
	bagpos = text.find("bag")
	if (bagpos > 0):
		return text[0:bagpos].strip()
	else:
		return text.strip()

def testParseBagInput():
	result = parseBagInput(TEST_INPUT)
	if result == TEST_RULES:
		print("testParseBagInput Pass")
	else:
		print("testParseBagInput Fail")

def testCountColorsForGoldBags():
	result = countColorsForGoldBags(TEST_RULES)
	if result == 4:
		print("testCountColorsForGoldBags Pass")
	else:
		print("testCountColorsForGoldBags Fail")

def testCountContainedBags():
	goldcount = countContainedBags("shiny gold", parseBagInput(TEST_INPUT))
	plumcount = countContainedBags("vibrant plum", parseBagInput(TEST_INPUT))
	goldcount2 = countContainedBags("shiny gold", parseBagInput(TEST_INPUT2))

	if goldcount == 32 and plumcount == 11 and goldcount2 == 126:
		print("testCountContainedBags Pass")
	else:
		print("testCountContainedBags Fail")	

def main():
	testParseBagInput()
	testCountColorsForGoldBags()
	testCountContainedBags()	

	inputList = []

	f = open('data/day7_input.txt', 'r')
	lines = f.readlines()
	lastline = lines[-1]
	group = ""

	for line in lines:
		inputList.append(line.strip())

	ruleDict = parseBagInput(inputList)
	print(ruleDict)
	print("countColorsForGoldBags: ", countColorsForGoldBags(ruleDict))
	print("countContainedBags: ", countContainedBags("shiny gold", ruleDict))



if __name__ == '__main__':
	main()
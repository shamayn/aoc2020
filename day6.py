
def countQuestions(input, countall=False):
	sumOfGroups = 0
	for i in input:
		countOfOneGroup = 0
		if (countall == True):
			countOfOneGroup = countOneGroupAllYes(i)
		else:
			countOfOneGroup = countOneGroupAnyYes(i)
		print(i, countOfOneGroup)
		sumOfGroups += countOfOneGroup
	return sumOfGroups

def countOneGroupAnyYes(response):
	questions = set()
	for i in response:
		if i != " ":
			questions.add(i)

	return len(questions)

def countOneGroupAllYes(response):
	indiv = response.split(" ")
	numIndiv = len(indiv)
	allanswered = 0
	questions = dict()

	for i in response:
		if i != " ":
			if i not in questions:
				questions[i] = 1
			else:
				questions[i] += 1
			if questions[i] == numIndiv:
				allanswered += 1

	return allanswered


def testCountQuestions():
	input = ["abc","a b c", "ab ac", "a a a a", "b"]
	if (countQuestions(input) == 11 and countQuestions(input, True) == 6):
		print("Pass")
	else:
		print("Fail")

def main():
	testCountQuestions()	

	inputList = []

	f = open('data/day6_input.txt', 'r')
	lines = f.readlines()
	lastline = lines[-1]
	group = ""

	for line in lines:
		if line == "\n":
			if len(group) > 0:
				inputList.append(group.strip())
				group = ""
		else:
			group += " " + line.strip()

	if len(group) > 0:
		inputList.append(group.strip())
	#print("countQuestions: ", countQuestions(inputList))
	print("countQuestionsAll: ", countQuestions(inputList, True))


if __name__ == '__main__':
	main()
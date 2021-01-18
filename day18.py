from collections import deque

TEST_INPUT = [
	"1 + 2 * 3 + 4 * 5 + 6",
	"1 + (2 * 3) + (4 * (5 + 6))",
	"2 * 3 + (4 * 5)",
	"5 + (8 * 3 + 9 + 3 * 4 * 3)",
	"5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
	"((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
	"(8 * (7 + 7 + 8)) + 2 + 9 * 9 + 9 * 4",
]

TEST_VALUES = [ 71, 51, 26, 437, 12240, 13632, 6768]
TEST_VALUES_2 = [ 231, 51, 46, 1445, 669060, 23340, 13464]


def evaluate(expression):
	print("evaluate expression", expression)
	operatorstack = deque()
	operandstack = deque()
	result = 0
	i = 0

	while i < len(expression):
		field = expression[i]

		#print("field", field)
		if field == " ":
			i += 1
			continue
		print("stacks", operandstack, operatorstack, "exp:", expression, "i:", i, field)
		
		if isOperator(field):
			operatorstack.append(field)
		elif field.isdigit():
			# parse digits
			val = 0
			while i < len(expression) and expression[i].isdigit():
				val = val*10 + int(expression[i])
				i += 1
			i -= 1
			#print("parsed digit", val)
			operandstack.append(val)
		elif field == "(":
			(val, newexpression) = evaluate(expression[i+1:])
			operandstack.append(val)
			expression = newexpression
			i = -1

		elif field == ")":
			while (len(operatorstack) > 0):
				left = operandstack.popleft()
				right = operandstack.popleft()
				op = operatorstack.popleft()
				val = doMath(left, right, op)
				#print("val", val)
				operandstack.appendleft(val)
			return (operandstack.popleft(), expression[i+1:])
		i += 1
	#print("stacks", operandstack, operatorstack)
	while (len(operatorstack) > 0):
		left = operandstack.popleft()
		right = operandstack.popleft()
		op = operatorstack.popleft()
		val = doMath(left, right, op)
		#print("val", val)
		operandstack.appendleft(val)
	result = operandstack.popleft()
	print("RESULT", result)
	return result, expression

def precedence2(op):
	if op == "+": return 2
	if op == "*": return 1
	return 0

def evaluate2(expression):
	print("evaluate2 expression", expression)
	operatorstack = deque()
	operandstack = deque()
	result = 0
	i = 0

	while i < len(expression):
		field = expression[i]

		#print("field", field)
		if field == " ":
			i += 1
			continue
		print("stacks", operandstack, operatorstack, 
			"exp:", expression, "i:", i, field, isOperator(field))

		if isOperator(field):
			print("hello", field)
			while (len(operatorstack) != 0 and
				precedence2(operatorstack[-1]) >= precedence2(field)):
				right = operandstack.pop()
				left = operandstack.pop()
				op = operatorstack.pop()
				val = doMath(left, right, op)
				print("computing ", left, right, op, val)

				operandstack.append(val)

			operatorstack.append(field)
		elif field.isdigit():
			# parse digits
			val = 0
			while i < len(expression) and expression[i].isdigit():
				val = val*10 + int(expression[i])
				i += 1
			i -= 1
			operandstack.append(val)
		elif field == "(":
			(val, newexpression) = evaluate2(expression[i+1:])
			operandstack.append(val)
			expression = newexpression
			i = -1

		elif field == ")":
			while (len(operatorstack) > 0):
				right = operandstack.pop()
				left = operandstack.pop()
				op = operatorstack.pop()
				val = doMath(left, right, op)
				operandstack.append(val)
			return (operandstack.pop(), expression[i+1:])
		i += 1
	while (len(operatorstack) > 0):
		right = operandstack.pop()
		left = operandstack.pop()
		op = operatorstack.pop()
		val = doMath(left, right, op)
		#print("val", val)
		operandstack.append(val)
	result = operandstack.pop()
	print("RESULT", result)
	return result, expression

def isOperator(field):
	return (field == "+" or field == "*")

def doMath(left, right, operator):
	result = 0
	if operator == "+":
		result = int(left) + int(right)
	if operator == "*":
		result = int(left) * int(right)
	return result

def testEvaluate():
	for i in range(len(TEST_INPUT)):
		if evaluate2(TEST_INPUT[i])[0] != TEST_VALUES[i]:
			print("testEvaluate Fail")
			return

	print("testEvaluate Pass")

def testEvaluate2():
	for i in range(len(TEST_INPUT)):
		if evaluate2(TEST_INPUT[i])[0] != TEST_VALUES_2[i]:
			print("testEvaluate2 Fail", TEST_INPUT[i])
			return


	print("testEvaluate2 Pass")

def main():
	#testEvaluate()
	testEvaluate2()

	f = open('data/day18_input.txt', 'r')
	lines = f.readlines()

	results = []
	for line in lines:
		expression = line.strip()
		#result = evaluate(expression)[0]
		result = evaluate2(expression)[0]

		results.append(result)
		print(expression, result)
	print(sum(results))


if __name__ == '__main__':
	main()
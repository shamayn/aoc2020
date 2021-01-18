import re

TEST_RULES = [
	"0: 4 1 5",
	"1: 2 3 | 3 2",
	"2: 4 4 | 5 5",
	"3: 4 5 | 5 4",
	"4: \"a\"",
	"5: \"b\"",
]

TEST_INPUT = [
	"ababbb",
	"bababa",
	"abbbab",
	"aaabbb",
	"aaaabbb",
]

TEST_RULES_2 = [
	"42: 9 14 | 10 1",
	"9: 14 27 | 1 26",
	"10: 23 14 | 28 1",
	"1: \"a\"",
	"11: 42 31",
	"5: 1 14 | 15 1",
	"19: 14 1 | 14 14",
	"12: 24 14 | 19 1",
	"16: 15 1 | 14 14",
	"31: 14 17 | 1 13",
	"6: 14 14 | 1 14",
	"2: 1 24 | 14 4",
	"0: 8 11",
	"13: 14 3 | 1 12",
	"15: 1 | 14",
	"17: 14 2 | 1 7",
	"23: 25 1 | 22 14",
	"28: 16 1",
	"4: 1 1",
	"20: 14 14 | 1 15",
	"3: 5 14 | 16 1",
	"27: 1 6 | 14 18",
	"14: \"b\"",
	"21: 14 1 | 1 14",
	"25: 1 1 | 1 14",
	"22: 14 14",
	"8: 42",
	"26: 14 22 | 1 20",
	"18: 15 15",
	"7: 14 5 | 1 21",
	"24: 14 1",
]

TEST_INPUT_2 = [
	"abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa",
	"bbabbbbaabaabba",
	"babbbbaabbbbbabbbbbbaabaaabaaa",
	"aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
	"bbbbbbbaaaabbbbaaabbabaaa",
	"bbbababbbbaaaaaaaabbababaaababaabab",
	"ababaaaaaabaaab",
	"ababaaaaabbbaba",
	"baabbaaaabbaaaababbaababb",
	"abbbbabbbbaaaababbbbbbaaaababb",
	"aaaaabbaabaaaaababaa",
	"aaaabbaaaabbaaa",
	"aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
	"babaaabbbaaabaababbaabababaaab",
	"aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba",
]

def validateMessages(rules, input):
	ruledict = parseRules(rules)
	print("rulesdict", ruledict)
	regex = rulesToRegex(ruledict)
	print("regex", regex)

	sum = 0
	for message in input:
		sum += bool(regex.match(message))
	print("sum", sum)
	return sum

def validateMessages2(rules, input):
	ruledict = parseRules(rules)
	ruledict["8"] = "(?: 42 )+".split()
	ruledict["11"] = ("(?: (?: (?: 42 ) {1} (?: 31 ) {1} ) | " \
		+ "(?: (?: 42 ) {2} (?: 31 ) {2} ) | " \
		+ "(?: (?: 42 ) {3} (?: 31 ) {3} ) | " \
		+ "(?: (?: 42 ) {4} (?: 31 ) {4} ) | " \
		+ "(?: (?: 42 ) {5} (?: 31 ) {5} ) | " \
		+ "(?: (?: 42 ) {6} (?: 31 ) {6} ) | "  \
		+ "(?: (?: 42 ) {7} (?: 31 ) {7} ) | " \
		+ "(?: (?: 42 ) {8} (?: 31 ) {8} ) | " \
		+ "(?: (?: 42 ) {9} (?: 31 ) {9} ) )").split()

	print("updated", ruledict)
	regex = rulesToRegex(ruledict)
	print("regex", regex)

	sum = 0
	for message in input:
		sum += bool(regex.match(message))
	print("sum", sum)
	return sum

def parseRules(rule_list):
	ruledict = dict()
	for r in rule_list:
		(key, value) = r.strip().split(":")
		val = value.replace("\"", "")
		if (val.find("|") > 0):
			# turn into a regex
			val = "(?: " + val + " )" 
		ruledict[key] = val.split()
	return ruledict

def rulesToRegex(ruledict):
	result = ruledict["0"].copy()
	while any(x.isdigit() for x in result):
		i, k = next((i,x) for (i, x) in enumerate(result) if x.isdigit())
		result[i:i+1] = ruledict[k].copy()
	result.insert(0, "^")
	result.append("$")
	return re.compile("".join(result))

def testValidateMessages():
	result = 2
	if validateMessages(TEST_RULES, TEST_INPUT) == result:
		print("testValidateMessages Pass")
	else:
		print("testValidateMessages Fail")

def testValidateMessages2():
	result = 12
	if validateMessages2(TEST_RULES_2, TEST_INPUT_2) == result:
		print("testValidateMessages2 Pass")
	else:
		print("testValidateMessages2 Fail")

def main():
	# testValidateMessages()
	#testValidateMessages2()

	f = open('data/day19_input.txt', 'r')
	lines = f.readlines()

	rules = []
	messages = []
	for line in lines:
		if line.find(":") != -1:
			rules.append(line.strip())
		elif len(line) > 0:
			messages.append(line.strip())

	#validateMessages(rules, messages)
	validateMessages2(rules, messages)



if __name__ == '__main__':
	main()
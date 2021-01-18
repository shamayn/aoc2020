import re

TEST_INPUT = [ 
	"class: 1-3 or 5-7",
	"row: 6-11 or 33-44",
	"seat: 13-40 or 45-50",
	"your ticket:",
	"7,1,14",
	"nearby tickets:",
	"7,3,47",
	"40,4,50",
	"55,2,20",
	"38,6,12"
]

TEST_INPUT_2 = [ 
	"class: 0-1 or 4-19",
	"row: 0-5 or 8-19",
	"seat: 0-13 or 16-19",
	"your ticket:",
	"11,12,13",
	"nearby tickets:",
	"3,9,18",
	"15,1,5",
	"5,14,9"
]

def findValidTickets(rulerows, ticketrows):
	ruleSet = parseRuleRanges(rulerows)
	invalid_sum = 0
	validtickets = []

	for ticket in ticketrows:
		fields = [int(i) for i in ticket.split(",")] 

		is_valid = True
		for field in fields:
			if field not in ruleSet:
				print("invalid_sum", field)
				invalid_sum += field
				is_valid = False
		if is_valid == True:
			validtickets.append(fields)
	#print(invalid)

	return invalid_sum, validtickets

def parseRuleRanges(rows):
	valid = set()
	for row in rows:
		if row == "":
			continue
		pattern = re.match(r"[A-Za-z ]*: (\d*)-(\d*) or (\d*)-(\d*)", row)
		#print("find", pattern.group(1), pattern.group(2), pattern.group(3), pattern.group(4))
		valid.update(expandRange(int(pattern.group(1)), int(pattern.group(2))))
		valid.update(expandRange(int(pattern.group(3)), int(pattern.group(4))))
	print(valid)
	return valid


def expandRange(start, end):
	values = set()
	for i in range(start, end+1):
		values.add(i)
	return values

def parseRows(input):
	your = input.index("your ticket:")
	nearby = input.index("nearby tickets:")
	yourticket = input[your+1] 
	rulerows = input[:your]
	ticketrows = input[nearby+1:]
	#print(rulerows, ticketrows)

	return (rulerows, yourticket, ticketrows) 

def testFindValidTickets():
	result = 71
	(rules, myticket, tickets) = parseRows(TEST_INPUT)
	if findValidTickets(rules, tickets)[0] == result:
		print("testFindValidTickets Pass")
	else:
		print("testFindValidTickets Fail")

def matchFields(input):
	(rules, myticket, tickets) = parseRows(input)

	rule_set_dict = parseRuleSetDict(rules)
	print(rule_set_dict)
	myticketfields = [int(i) for i in myticket.split(",")] 
	tickets.append(myticket)

	tickets_by_field = parseTickets(findValidTickets(rules, tickets)[1])
	num_fields = len(tickets_by_field[0])

	index_rule_dict = dict()

	for index, fieldvals in enumerate(tickets_by_field):
		size = len(fieldvals)
		# find rule for which all fieldvals are in the set
		for key in rule_set_dict:
			match = True
			overall_match = False

			for f in fieldvals:
				if f not in rule_set_dict[key]:
					match = False
			print(key, index, match, index_rule_dict)

			if match == True:
				if index not in index_rule_dict:
					index_rule_dict[index] = [key] #TODO
				else:
					rulelist = index_rule_dict[index]
					rulelist.append(key)
					index_rule_dict[index] = rulelist

	print("by index", index_rule_dict)
	rule_dict = dict()

	size = len(index_rule_dict)
	while size > 0:
		print("size", size)

		for i, rule in list(index_rule_dict.items()):
			print(i, rule)
			if len(rule) == 1:
				removed = index_rule_dict.pop(i)
				rule_dict[removed[0]] = i
				for item in index_rule_dict.values():
					if removed[0] in item:
						item.remove(removed[0])

				size -= 1

	print("rules", rule_dict)

	product = 1
	for rule, index in rule_dict.items():
		if rule.startswith("departure") == True:
			product *= myticketfields[index]

	print(product)
	return product

def parseTickets(ticketrows):
	allticketsbyfield = []
	for row in ticketrows:		
		size = len(row)
		for i, f in enumerate(row):
			if len(allticketsbyfield) <= i:
				allticketsbyfield.append([f])
			else:
				values = allticketsbyfield[i]
				values.append(f)
				allticketsbyfield[i] = values

	print("ticketsbyfield", allticketsbyfield)
	return allticketsbyfield


def parseRuleSetDict(rulerows):
	allrules = dict()

	for row in rulerows:
		values = set()
		if row == "":
			continue
		pattern = re.match(r"([A-Za-z ]*): (\d*)-(\d*) or (\d*)-(\d*)", row)
		print("re", pattern.group(1), pattern.group(2), pattern.group(3), pattern.group(4))
		values.update(expandRange(int(pattern.group(2)), int(pattern.group(3))))
		values.update(expandRange(int(pattern.group(4)), int(pattern.group(5))))
		allrules[pattern.group(1)] = values
	return allrules

def testMatchFields():
	matchFields(TEST_INPUT_2)

def main():
	testFindValidTickets()
	testMatchFields()

	f = open('data/day16_input.txt', 'r')
	lines = f.readlines()

	ticketrules = []
	for line in lines:
		if line != "":
			ticketrules.append(line.strip())

	#print(findValidTickets(ticketrules))
	print(matchFields(ticketrules))

if __name__ == '__main__':
	main()

def countValidPasswords(passwords):
	valid_count = 0
	count = 0

	for entry in passwords:
		policy_and_password = entry.split(":")
		password = policy_and_password[1].strip()
		range_and_letter = policy_and_password[0].split(" ")
		letter = range_and_letter[1]
		range = range_and_letter[0].split("-")
		min = int(range[0])
		max = int(range[1])
		print(min, " ", max, " ", letter, ": ", password)

		lettercount = 0
		for char in password:
			if char == letter:
				lettercount += 1
		print("lettercount = ", lettercount)
		if lettercount >= min and lettercount <= max:
			print("Valid")
			valid_count += 1
		else:
			print("Invalid")
		count += 1

	print(count)
	print(valid_count)
	return valid_count;

def countValidPasswords2(passwords):
	valid_count = 0
	count = 0

	for entry in passwords:
		policy_and_password = entry.split(":")
		password = policy_and_password[1].strip()
		range_and_letter = policy_and_password[0].split(" ")
		letter = range_and_letter[1]
		range = range_and_letter[0].split("-")
		pos1 = int(range[0])
		pos2 = int(range[1])
		print(pos1, " ", pos2, " ", letter, ": ", password, " ", len(password))

		poscount = 0
		if pos1 <= len(password) and password[pos1 - 1] == letter:
			poscount += 1
		if pos2 <= len(password) and password[pos2 - 1] == letter:
			poscount += 1
		if poscount == 1:
			print("Valid")
			valid_count += 1
		else:
			print("Invalid")

		count += 1

	print(count)
	print(valid_count)
	return valid_count;

def testCountValidPasswords():
	passwords = {"1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"};
	if countValidPasswords(passwords) == 2:
		print("Pass")
	else:
		print("Fail")

def testCountValidPasswords2():
	passwords = {"1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"};
	if countValidPasswords2(passwords) == 1:
		print("Pass")
	else:
		print("Fail")


def main():
	testCountValidPasswords()
	testCountValidPasswords2()


	inputList = []

	f = open('data/day2_input.txt', 'r')
	lines = f.readlines()
	for line in lines:
		inputList.append(line)

	print(len(inputList))
	print(countValidPasswords(inputList))

	print(countValidPasswords2(inputList))


if __name__ == '__main__':
	main()
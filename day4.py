
import re

REQUIRED_PASSPORT_FIELDS = {
	"byr", # (Birth Year) - four digits; at least 1920 and at most 2002.
	"iyr", # (Issue Year) - four digits; at least 2010 and at most 2020.
	"eyr", # (Expiration Year) - four digits; at least 2020 and at most 2030.
	"hgt", # (Height) - a number followed by either cm or in:
		   #   If cm, the number must be at least 150 and at most 193.
	       #   If in, the number must be at least 59 and at most 76.
	"hcl", # (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
	"ecl", # (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
	"pid", # (Passport ID) - a nine-digit number, including leading zeroes.
}

OPTIONAL_PASSPORT_FIELDS = {
	"cid" # (Country ID) - ignored, missing or not.
}

EYE_COLORS = {
	"amb",
	"blu",
	"brn", 
	"gry", 
	"grn",
	"hzl", 
	"oth"
}

def checkYear(value, start, end):
	return int(value) >= start and int(value) <= end

def checkHeight(value):
	cm = value.find("cm");
	if cm >= 0:
		height = int(value[0:cm])
		print(height)
		return height >= 150 and height <= 193
	inches = value.find("in")
	if inches >= 0:
		height = int(value[0:inches])
		print(height)
		return height >= 59 and height <= 76
	return False

def checkHexColor(value):
	pattern = re.compile("^#(?:[a-fA-F0-9]{6})$")
	if(pattern.match(value)):
		return True
	return False

def testHexColor():
	if checkHexColor("#00ff12") == True and checkHexColor("0022211") == False:
		print("Pass")

def checkPid(value):
	pattern = re.compile("^(?:[0-9]{9})$")
	if(pattern.match(value)):
		return True
	return False

def fieldValidator(field, value):
	print("validating: ", value)
	if field == "byr":
		return checkYear(value, 1920, 2002)
	elif field == "iyr":
		return checkYear(value, 2010, 2020)
	elif field == "eyr":
		return checkYear(value, 2020, 2030)
	elif field == "hgt":
		return checkHeight(value)
	elif field == "hcl":
		return checkHexColor(value)
	elif field == "ecl":
		return value in EYE_COLORS;
	elif field == "pid":
		return checkPid(value)
	elif field == "cid":
		return True
	return False



def countValidPassports(input):
	validpassportcount = 0

	for i in range(len(input)):
		# check each passport
		print(input[i])
		fields = set()
		row = input[i].split(" ")
		for r in row:
			keyval = r.split(":")
			fields.add(keyval[0])
			print("field: ", keyval[0])
		validfieldcount = 0
		for rf in REQUIRED_PASSPORT_FIELDS:
			if rf in fields:
				validfieldcount += 1 
			else:
				break
		if validfieldcount == len(REQUIRED_PASSPORT_FIELDS):
			print("passport valid")
			validpassportcount += 1
		else:
			print("passport invalid")

	return validpassportcount


def countValidPassportsWithFields(input):
	validpassportcount = 0

	for i in range(len(input)):
		# check each passport
		print(input[i])
		fields = {}
		row = input[i].split(" ")
		for r in row:
			keyval = r.split(":")
			fields[keyval[0]] = keyval[1].strip()
			print("field:", keyval[0], ",", keyval[1])
		validfieldcount = 0
		for rf in REQUIRED_PASSPORT_FIELDS:
			if rf in fields:
				if fieldValidator(rf, fields[rf]) == True:
					print("field valid")
					validfieldcount += 1
				else:
					print("field missing or invalid") 
			else:
				break
		if validfieldcount == len(REQUIRED_PASSPORT_FIELDS):
			print("passport valid")
			validpassportcount += 1
		else:
			print("passport invalid")

	return validpassportcount

def testPassportChecker():
	input = [
			"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm",
			"iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929",
			"hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm",
			"hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in" ]
	if countValidPassports(input) == 2:
		print("Pass")
	else:
		print("Fail")

def testPassportCheckerWithFields():
	input_invalid = [
		"eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
		"iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946",
		"hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
		"hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007" ]

	input_valid = [
		"pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f",
		"eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
		"hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022",
		"iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
	]
	if countValidPassportsWithFields(input_valid) == 4 and countValidPassportsWithFields(input_invalid) == 0:
		print("Pass")
	else:
		print("Fail")

def main():
	#testPassportChecker()
	#testHexColor()
	#testPassportCheckerWithFields()

	inputList = []

	f = open('data/day4_input.txt', 'r')
	lines = f.readlines()
	passportrow = ""

	for line in lines:
		if line == "\n":
			if len(passportrow) > 0:
				inputList.append(passportrow.strip())
				passportrow = ""
		else:
			passportrow += " " + line.strip()

	print(len(inputList))
	print("count valid passports: ", countValidPassports(inputList))
	print("count passports with valid fields", countValidPassportsWithFields(inputList))



if __name__ == '__main__':
	main()

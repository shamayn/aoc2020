import math

def findSeat(seatcode):
	rowcode = seatcode[0:7]
	colcode = seatcode[7:10]
	row = binarySearch(rowcode, 127)
	col = binarySearch(colcode, 7)
	print("seat:", row, col)
	return (row, col)

def binarySearch(code, max):
	start = 0
	end = max
	for i in range(len(code)):
		if code[i] == "F" or code[i] == "L":
			end = math.floor((end + start)/ 2)
		elif code[i] == "B" or code[i] == "R":
			start = math.ceil((end + start)/ 2)
		#print(code[i], start, end)
	return start

def findMaxSeatId(seatcodes):
	maxseat = 0
	for sc in seatcodes:
		seat = findSeat(sc)
		seatid = getSeatId(seat[0], seat[1])

		if seatid > maxseat:
			maxseat = seatid
	return maxseat

def findMissingSeats(seatcodes):
	seats = set()
	for sc in seatcodes:
		seats.add(findSeat(sc))
	missingseatids = []
	for i in range(128):
		for j in range(8):
			if (i, j) not in seats:
				seatid= getSeatId(i,j)
				missingseatids.append(getSeatId(i, j))
				print("missing: ", seatid)


def getSeatId(row, col):
	return row * 8 + col

def testFindSeat():
	input = "FBFBBFFRLR"

	result = findSeat(input)
	if result == (44, 5):
		print("Pass")
	else:
		print("Fail")


def main():
	testFindSeat()

	inputList = []

	f = open('data/day5_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(line.strip())

	print(len(inputList))
	#print("find max seat: ", findMaxSeatId(inputList))
	printMissingSeats(inputList)


if __name__ == '__main__':
	main()
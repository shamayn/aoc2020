def countTreesOnSlope(input, right, down):
	length = len(input)

	pos = 0
	treecount = 0
	count = 0
	for i in range(0, length - down, down):
		width = len(input[i])
		# check next position: i+1, pos+3
		pos += right
		if pos >= width:
			pos = pos % width
		print("i = ", i, " width = ", width, " pos = ", pos)

		if input[i + down][pos] == "#":
			treecount += 1


	print("count=", count, "treecount=", treecount)
	return treecount

def productOfSlopes(input):
	return (countTreesOnSlope(input, 1, 1) * countTreesOnSlope(input, 3, 1)
	* countTreesOnSlope(input, 5, 1) * countTreesOnSlope(input, 7, 1)
	* countTreesOnSlope(input, 1, 2))


def testCountTreesRight3Down1():
	input = ["..##.......",
			"#...#...#..",
			".#....#..#.",
			"..#.#...#.#",
			".#...##..#.",
			"..#.##.....",
			".#.#.#....#",
			".#........#",
			"#.##...#...",
			"#...##....#",
			".#..#...#.#" ]
	if countTreesOnSlope(input, 3, 1) == 7:
		print("Pass")
	else:
		print("Fail")

def testProductOfSlopes():
	input = ["..##.......",
			"#...#...#..",
			".#....#..#.",
			"..#.#...#.#",
			".#...##..#.",
			"..#.##.....",
			".#.#.#....#",
			".#........#",
			"#.##...#...",
			"#...##....#",
			".#..#...#.#" ]
	if productOfSlopes(input) == 336:
		print("Pass")
	else:
		print("Fail")



def main():
	testCountTreesRight3Down1()
	testProductOfSlopes()

	inputList = []

	f = open('data/day3_input.txt', 'r')
	lines = f.readlines()
	for line in lines:
		inputList.append(line.strip())

	print(len(inputList))
	print(countTreesOnSlope(inputList, 3, 1))
	print(productOfSlopes(inputList))


if __name__ == '__main__':
	main()

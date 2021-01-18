import copy

TEST_INPUT = [
			"L.LL.LL.LL",
			"LLLLLLL.LL",
			"L.L.L..L..",
			"LLLL.LL.LL",
			"L.LL.LL.LL",
			"L.LLLLL.LL",
			"..L.L.....",
			"LLLLLLLLLL",
			"L.LLLLLL.L",
			"L.LLLLL.LL",
]
TEST_OUT1 = [
			"#.##.##.##",
			"#######.##",
			"#.#.#..#..",
			"####.##.##",
			"#.##.##.##",
			"#.#####.##",
			"..#.#.....",
			"##########",
			"#.######.#",
			"#.#####.##",
]
TEST_OUT2 = [
			"#.LL.L#.##",
			"#LLLLLL.L#",
			"L.L.L..L..",
			"#LLL.LL.L#",
			"#.LL.LL.LL",
			"#.LLLL#.##",
			"..L.L.....",
			"#LLLLLLLL#",
			"#.LLLLLL.L",
			"#.#LLLL.##",
]

TEST_OUT5 = [
			"#.#L.L#.##",
			"#LLL#LL.L#",
			"L.#.L..#..",
			"#L##.##.L#",
			"#.#L.LL.LL",
			"#.#L#L#.##",
			"..L.L.....",
			"#L#L##L#L#",
			"#.LLLLLL.L",
			"#.#L#L#.##",
]

def computeSeats(inputGrid, method=1):
	iheight = len(inputGrid)
	jwidth = len(inputGrid[0])
	output = copy.deepcopy(inputGrid)
	occupied = 0
	# print(id(inputGrid[0]), id(output[0]))
	for i in range(iheight):
		for j in range(jwidth):
			current = inputGrid[i][j]
			# print(i, j, current)
			if current == "L": # empty
				# if no occupied seats around it, change to occupied
				if method == 1 and countOccupied1(inputGrid, i, j) == 0:
					# print("flipped L to #")
					output[i][j] = "#"
					occupied += 1
				elif method == 2 and countOccupied2(inputGrid, i, j) == 0:
					output[i][j] = "#"
					occupied += 1
			elif current == "#": # occupied
				# if 4 or more seats occupied, change to empty
				if method == 1 and countOccupied1(inputGrid, i, j) >= 4:
					# print("flipped # to L")
					output[i][j] = "L"
				elif method == 2 and countOccupied2(inputGrid, i, j) >= 5:
					output[i][j] = "L"
				else:
					occupied += 1
	# print("output", occupied, output)
	return (occupied, output)

def convertToGrid(input):
	grid = []
	for i in range(len(input)):
		print(input[i])
		grid.append(list(input[i]))
	return grid

def prettyprintGrid(grid):
	for i in range(len(grid)):
		line = ""
		for j in range(len(grid[i])):
			line += grid[i][j]
		print(line)

def countOccupied1(input, i, j):
	iheight = len(input)
	jwidth = len(input[0])
	countoccupied = 0
	for x in range(max(i-1, 0), min(i+2, iheight)):
		for y in range(max(j-1, 0), min(j+2, jwidth)):
			if input[x][y] == "#" and (x != i or y != j):
				#print("occupied:", x, y, input[x][y])
				countoccupied += 1
	# print("occupied", countoccupied)
	return countoccupied

def countOccupied2(input, i, j):
	iheight = len(input)
	jwidth = len(input[0])
	print("ij", i, j, "dim", iheight, jwidth)
	countoccupied = 0
	for x in range(max(i-1, 0), min(i+2, iheight)):
		for y in range(max(j-1, 0), min(j+2, jwidth)):
			if x == i and y == j:
				continue

			xdirection = x - i
			ydirection = y - j
			xpos = x
			ypos = y
			# print("starting count ", xdirection, ydirection)
			while xpos < iheight and ypos < jwidth and xpos >= 0 and ypos >= 0:
				# print ("traversing: ", xpos, ypos, input[xpos][ypos])
				if input[xpos][ypos] == "#":
					countoccupied += 1
					break
				elif input[xpos][ypos] == "L":
					break
				xpos += xdirection
				ypos += ydirection
	#print("occupied", countoccupied)
	return countoccupied

def testCountOccupied2():
	CO2_TEST_INPUT = [
				".......#.", 
				"...#.....", 
				".#.......", 
				".........", 
				"..#L....#", 
				"....#....", 
				".........", 
				"#........", 
				"...#....." ]
	print(countOccupied2(convertToGrid(CO2_TEST_INPUT), 4, 3))
	CO2_TEST_INPUT_2 = [
				".............",
				".L.L.#.#.#.#.",
				"............." ]

	print(countOccupied2(convertToGrid(CO2_TEST_INPUT_2), 1, 1))
	CO2_TEST_INPUT_3 = [
				".##.##.",
				"#.#.#.#",
				"##...##",
				"...L...",
				"##...##",
				"#.#.#.#",
				".##.##." ]
	print(countOccupied2(convertToGrid(CO2_TEST_INPUT_3), 3, 3))




def runComputeSeats(inputGrid, method=1):
	prev = []
	current = computeSeats(inputGrid, method)
	while current[1] != prev:
		prev = copy.deepcopy(current[1])
		current = computeSeats(prev, method)
		print("Iteration prev")
		prettyprintGrid(prev)
		print("Iteration current")
		prettyprintGrid(current[1])
	return current[0]

def testComputeSeats():
	grid = convertToGrid(TEST_INPUT)
	if runComputeSeats(grid) == 37 and runComputeSeats(grid, 2) == 26:
		print("computeSeats Pass")
	else:
		print("computeSeats Fail")		

def main():
	#testCountOccupied2()
	#testComputeSeats()

	inputList = []

	f = open('data/day11_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(line.strip())

	print("len:", len(inputList))
	print(runComputeSeats(convertToGrid(inputList), 2))

if __name__ == '__main__':
	main()
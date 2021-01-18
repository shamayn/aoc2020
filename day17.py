
TEST_INPUT = [ # = active, . = inactive
		".#.",
		"..#",
		"###",
]

INPUT = [
		"##..#.#.",
		"###.#.##",
		"..###..#",
		".#....##",
		".#..####",
		"#####...",
		"#######.",
		"#.##.#.#"
]
def simCycles3D(input):
	initialstate = [list(x) for x in input]
	# print("state", initialstate)
	height = len(input)
	width = len(input[0])
	cubestates = dict()
	# first record initial state
	for x in range(width):
		for y in range(height):
			cubestates[(x, y, 0)] = initialstate[x][y]
	# print("cubestates", cubestates)

	newstates = cubestates
	for i in range(6):
		newstates = cycle3D(newstates)

	count = 0
	count += printGrid3D(newstates)
	return count

def cycle3D(cubestates):
	newstates = dict()
	for cube in cubestates:
		actives = 0
		mystate = cubestates[cube]
		neighbours = getNeighbours3D(cube)
		for i in neighbours:
			# exclude myself
			if i == cube: continue
			if i in cubestates:
				if cubestates[i] == "#":
					actives += 1
			else:
				# one more level
				# print("neighbour to add", i)
				nactives = 0
				nextneighbours = getNeighbours3D(i)
				for j in nextneighbours:
					if j == i: continue
					if j in cubestates and cubestates[j] == "#":
						nactives += 1
				newstates[i] = calculateState(".", nactives)

		newstates[cube] = calculateState(mystate, actives)
		# print("mystate", mystate, "active neighbours", actives, newstates[cube])

	#print("newstate", newstates)
	printGrid3D(newstates)
	return newstates

def simCycles4D(input):
	initialstate = [list(x) for x in input]
	# print("state", initialstate)
	height = len(input)
	width = len(input[0])
	cubestates = dict()
	# first record initial state
	for x in range(width):
		for y in range(height):
			cubestates[(x, y, 0, 0)] = initialstate[x][y]
	# print("cubestates", cubestates)

	newstates = cubestates
	for i in range(6):
		newstates = cycle4D(newstates)

	count = 0
	count += printGrid4D(newstates)
	print(count)
	return count

def cycle4D(cubestates):
	newstates = dict()
	for cube in cubestates:
		actives = 0
		mystate = cubestates[cube]
		neighbours = getNeighbours4D(cube)
		for i in neighbours:
			# exclude myself
			if i == cube: continue
			if i in cubestates:
				if cubestates[i] == "#":
					actives += 1
			else:
				# one more level
				# print("neighbour to add", i)
				nactives = 0
				nextneighbours = getNeighbours4D(i)
				for j in nextneighbours:
					if j == i: continue
					if j in cubestates and cubestates[j] == "#":
						nactives += 1
				newstates[i] = calculateState(".", nactives)

		newstates[cube] = calculateState(mystate, actives)
		# print("mystate", mystate, "active neighbours", actives, newstates[cube])

	#print("newstate", newstates)
	printGrid4D(newstates)
	return newstates

#TODO
def printGrid3D(states):
	count = 0
	minx = miny = minz = maxx = maxy = maxz = 0
	for key in states:
		if key[0] < minx:
			minx = key[0]
		elif key[0] > maxx:
			maxx = key[0]
		if key[1] < miny:
			miny = key[1]
		elif key[1] > maxy:
			maxy = key[1]
		if key[2] < minz:
			minz = key[2]
		elif key[2] > maxz:
			maxz = key[2]
	print(minx, miny, minz, maxx, maxy, maxz)
	for i in range(minz, maxz+1):
		print("z:", i)
		for j in range(minx, maxx+1):
			row = ""
			for k in range(miny, maxy+1):
				if (j, k, i) not in states:
					row += "."	
				else:
					row += states[(j, k, i)]
					if states[(j, k, i)] == "#":
						count += 1
			print(row)
	return count

def printGrid4D(states):
	count = 0
	minx = miny = minz = minw = maxx = maxy = maxz = maxw = 0
	for key in states:
		if key[0] < minx:
			minx = key[0]
		elif key[0] > maxx:
			maxx = key[0]
		if key[1] < miny:
			miny = key[1]
		elif key[1] > maxy:
			maxy = key[1]
		if key[2] < minz:
			minz = key[2]
		elif key[2] > maxz:
			maxz = key[2]
		if key[3] < minw:
			minw = key[3]
		elif key[3] > maxw:
			maxw = key[3]
	print(minx, miny, minz, minw, maxx, maxy, maxz, maxw)
	for i in range(minz, maxz+1):
		for m in range(minw, maxw+1):
			print("z:", i, "w:", m)
			for j in range(minx, maxx+1):
				row = ""
				for k in range(miny, maxy+1):
					if (j, k, i, m) not in states:
						row += "."	
					else:
						row += states[(j, k, i, m)]
						if states[(j, k, i, m)] == "#":
							count += 1
				print(row)
	return count
# If a cube is active and exactly 2 or 3 of its neighbors are also active,
# the cube remains active. Otherwise, the cube becomes inactive.
# If a cube is inactive but exactly 3 of its neighbors are active, 
# the cube becomes active. Otherwise, the cube remains inactive.
def calculateState(mystate, num_actives):
	newstate = mystate
	if mystate == "#":
		if (num_actives == 2 or num_actives == 3):
			# stays active
			newstate = "#"
		else:
			newstate = "."
	elif mystate == ".":
		if (num_actives == 3):
			newstate = "#"
		else:
			newstate = "."
	return newstate

def getNeighbours3D(coordinates):
	result = ([(x, y, z) for x in range(coordinates[0]-1, coordinates[0]+2)
			for y in range(coordinates[1]-1,coordinates[1]+2)
			for z in range(coordinates[2]-1, coordinates[2]+2)])	
	return result

def getNeighbours4D(coordinates):
	result = ([(x, y, z, w) for x in range(coordinates[0]-1, coordinates[0]+2)
			for y in range(coordinates[1]-1,coordinates[1]+2)
			for z in range(coordinates[2]-1, coordinates[2]+2)
			for w in range(coordinates[3]-1, coordinates[3]+2)])
	return result

def testSimCycles3D():
	print(getNeighbours3D((1, 2, 3)))
	result = 112
	if simCycles3D(TEST_INPUT) == result:
		print("testSimCycles3D Pass")
	else:
		print("testSimCycles3D Fail")


def testSimCycles4D():
	result = 848
	if simCycles4D(TEST_INPUT) == result:
		print("testSimCycles4D Pass")
	else:
		print("testSimCycles4D Fail")

def main():
	#testSimCycles3D()
	#print(simCycles3D(INPUT))
	#testSimCycles4D()
	print(simCycles4D(INPUT))


if __name__ == '__main__':
	main()
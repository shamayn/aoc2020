import re
from itertools import combinations, product

import numpy
from scipy import ndimage

TEST_GRID = [
	[1951, 2311, 3079],
	[2729, 1427, 2473],
	[2971, 1489, 1171],
]

SEAMONSTER = [                  
	"                  # ", 
	"#    ##    ##    ###",
 	" #  #  #  #  #  #   "
]


def alignGrids(input):
	ids_to_tiles = parseGrids(input)
	matches = findMatches(ids_to_tiles)
	result = 1
	for m in matches:
		if len(matches[m]) == 2:
			result *= int(m)
	# print("result", result)
	return result

def parseGrids(input):
	ids_to_tiles = dict()
	id = ""
	grid = []
	pattern = re.compile("Tile ([0-9]+):")
	for line in input:
		if line.strip() == "": continue
		match = pattern.search(line.strip())
		if match:
			id = match.group(1)
		else:
			grid.append(line.strip())
			if len(grid) == 10:
				ids_to_tiles[id] = grid.copy()
				grid.clear()

	return ids_to_tiles

def findMatches(ids_to_tiles):
	ids_to_edges = dict()
	matches = dict()
	for i in ids_to_tiles:
		edges = getEdges(ids_to_tiles[i])
		ids_to_edges[i] = edges

	# print(len(ids_to_edges.keys()))
	for x, y in combinations(list(ids_to_edges.keys()), r=2):
		# print("xy", x, y)
		for i, j in product(range(0,4), repeat=2):
			if ids_to_edges[x][i] == ids_to_edges[y][j] or ids_to_edges[x][i] == ids_to_edges[y][j][::-1]:
				if x not in matches:
					matches[x] = [y]
				else:
					matches[x].append(y)
				if y not in matches:
					matches[y] = [x]
				else:
					matches[y].append(x)
				# print("match", ids_to_edges[x][i], ids_to_edges[y][j])
	# print(matches)
	return matches

def getEdges(grid):
	left = []
	right = []
	for i in range(len(grid)):
		left.append(grid[i][0])
		right.append(grid[i][len(grid)-1])
	# top, right, bottom, left
	return [ "".join(grid[0]), "".join(right), "".join(grid[len(grid)-1]), "".join(left)]

def findWaterRoughness(input):
	imgdict = {"#": 1, ".": 0}
	imagearr = buildImage(input)
	image = numpy.array([
		[imgdict[x] for x in row]
			for row in imagearr
		])
	print(image)
	sea_monster = numpy.array([
	    [int(x) for x in (line.replace('#', '1').replace(' ', '0'))]
	    for line in SEAMONSTER
	])
	img_orientations = list(tileOrientations(image))
	mcounts  = [countSeaMonsters(i, sea_monster) for i in img_orientations] 
	mimage = img_orientations[numpy.argmax(mcounts)]
	roughness = mimage.sum() - countSeaMonsters(mimage, sea_monster) * sea_monster.sum()
	print("roughness", roughness)
	return roughness

def countSeaMonsters(image, monster):
    return (ndimage.correlate(image, monster, mode='constant') == monster.sum()).sum()



def buildImage(input):
	ids_to_tiles = parseGrids(input)
	ids_to_edges = dict()

	for i in ids_to_tiles:
		edges = getEdges(ids_to_tiles[i])
		ids_to_edges[i] = edges
	
	matches = findMatches(ids_to_tiles)
	# assemble
	print("matches", matches)
	corners = [i for i in matches if len(matches[i]) == 2]
	sides = [i for i in matches if len(matches[i]) == 3]
	print("corners", corners)
	print("sides", sides)
	# start with corner[0]

	grid = []
	cornerid = corners[0]
	top = matches[cornerid][0]
	left = matches[cornerid][1]
	seen = set()

	grid.append([cornerid, top])
	seen.add(cornerid)
	seen.add(top)

	# first row
	next = [i for i in matches[top] if ((i in sides or i in corners) and i not in seen)]
	# i = 0
	while len(next) > 0:
		grid[0].append(next[0])
		seen.add(next[0])
		print("next", next)

		if (next[0] in corners): 
			next = []
		else:
			next = [i for i in matches[next[0]] if ((i in sides or i in corners) and i not in seen)]

	# first column
	next = [i for i in matches[cornerid] if ((i in sides or i in corners) and i not in seen)]

	while len(next) > 0:
		print("nextcol", next, "matches", matches[next[0]])

		grid.append([next[0]])
		seen.add(next[0])
		if (next[0] in corners): 
			next = []
		else:
			next = [i for i in matches[next[0]] if ((i in sides or i in corners) and i not in seen)]

	width = len(grid[0])
	height = len(grid)
	for y in range(1, height):
		for x in range(1, width):
			top = grid[y-1][x] # grid[0][1]
			left = grid[y][x-1] # grid[1][0]
			next = [i for i in matches if (top in matches[i] and left in matches[i] and i not in seen)]
			grid[y].append(next[0])
			seen.add(next[0])

	# print(grid)


	tiles = []

	print("dim", height, width)
	for i in range(0, height):
		for j in range(0, width):
			thisarray = sides = [0, 1, 2, 3]
			x = grid[i][j] # me
			print("ij", i, j)
			if i == 0 and j == 0:
				y = grid[i][j+1] # right
				z = grid[i+1][j] # bottom
				(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
				(edgexz, edgezx, flipxz) = findMatchingEdge(ids_to_edges, x, z)
				if (edgexy, edgexz) == (1, 2):
					# no need to rotate
					print("as is")
				elif edgexz - edgexy == 1 or edgexz - edgexy == -3:
					#TODO
					thisarray = [sides[sides.index(edgexy)- 1], edgexy, edgexz, sides[sides.index(edgexz)+ 1]]
				else:
					thisarray = [sides[sides.index(edgexy) + 1], edgexy, edgexz, sides[sides.index(edgexz)-1] ]

			elif i == 0:
				if j == width-1: # right corner
					x = grid[i][j] # me
					z = grid[i+1][j] # bottom
					w = grid[i][j-1] # left

					(edgexz, edgezx, flipxz) = findMatchingEdge(ids_to_edges, x, z)
					(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)
					if (edgexz, edgexw) == (3, 4):
						# no need to rotate
						print("as is")
					elif edgexw - edgexz == 1 or edgexw - edgexz == -3:
						thisarray = [sides[sides.index(edgexz) - 2], sides[sides.index(edgexz) - 1], edgexz, edgexw]
						# no need to flip, might need to rotate
					else:
						thisarray = [sides[sides.index(edgexw) - 1], sides[sides.index(edgexw)- 2], edgexz, edgexw]
				else: 
					# top row
					y = grid[i][j+1] # right
					z = grid[i+1][j] # bottom
					w = grid[i][j-1] # left

					(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
					(edgexz, edgezx, flipxz) = findMatchingEdge(ids_to_edges, x, z)
					(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)
					if (edgexy, edgexz, edgexw) == (1, 2, 3):
						# no need to rotate
						print("as is")
					elif edgexz - edgexy == 1 or edgexz - edgexy == -3:
						thisarray = [sides[sides.index(edgexy) - 1], edgexy, edgexz, edgexw]
						# no need to flip, might need to rotate
					else:
						thisarray = [sides[sides.index(edgexy) + 1], edgexy, edgexz, edgexw]
			elif j == 0:
				if i == height-1:
					# bottom left corner
					x = grid[i][j] # me
					q = grid[i-1][j] # above, 0
					y = grid[i][j+1] # right, 1

					(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
					(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
					if (edgexq, edgexy) == (0, 1):
						# no need to rotate
						print("as is")
					elif edgexy - edgexq == 1 or edgexy - edgexq == -3:
						thisarray = [edgexq, edgexy, sides[sides.index(edgexy) + 1], sides[sides.index(edgexq) - 1]]
						# no need to flip, might need to rotate
					else:
						thisarray = [edgexq, edgexy, sides[sides.index(edgexy) - 1], sides[sides.index(edgexy) - 2]]
				else: # i is anything but corner
					# left edge
					x = grid[i][j] # me
					q = grid[i-1][j] # above, 0
					y = grid[i][j+1] # right, 1
					z = grid[i+1][j] # bottom, 2

					(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
					(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
					(edgexz, edgezx, flipxz) = findMatchingEdge(ids_to_edges, x, z)

					thisarray = sides = [0, 1, 2, 3]

					if (edgexq, edgexy, edgexz) == (0, 1, 2):
						# no need to rotate
						print("as is")
					elif edgexz - edgexy == 1 or edgexz - edgexy == -3:
						thisarray = [edgexq, edgexy, edgexz, sides[sides.index(edgexq) - 1]]
						# no need to flip, might need to rotate
					else:
						thisarray = [edgexq, edgexy, edgexz, sides[sides.index(edgexz) - 1]]
			elif j == width-1:
				# right edge
				if i == height-1:
					# bottom right corner
					x = grid[i][j] # me
					q = grid[i-1][j] # above 0
					w = grid[i][j-1] # left 3

					(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
					(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)

					if (edgexq, edgexw) == (0, 3):
						# no need to rotate
						print("as is")
					elif edgexq - edgexw == 1 or edgexq - edgexw == -3:
						thisarray = [edgexq, sides[sides.index(edgexz) -2], sides[sides.index(edgexw)- 1], edgexw]
					else:
						thisarray = [edgexq, sides[sides.index(edgexq) -1], sides[sides.index(edgexq)- 2], edgexw]
				else:
					# right edge
					x = grid[i][j] # me
					q = grid[i-1][j] # above 0
					z = grid[i+1][j] # bottom, 2
					w = grid[i][j-1] # left 3

					(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
					(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)
					(edgexz, edgezw, flipxw) = findMatchingEdge(ids_to_edges, x, z)

					if (edgexq, edgexw, edgexz) == (0, 2, 3):
						# no need to rotate
						print("as is")
					elif edgexw - edgexz == 1 or edgexw - edgexz == -3:
						thisarray = [edgexq, sides[sides.index(edgexz)-1], edgexz, edgexw]
					else:
						thisarray = [edgexq, sides[sides.index(edgexq)-1], edgexz, edgexw]

			elif i == height-1:
				x = grid[i][j] # me
				q = grid[i-1][j] # above
				y = grid[i][j+1] # right
				w = grid[i][j-1] # left

				(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
				(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
				(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)

				if (edgexq, edgexy, edgexw) == (0, 1, 3):
					# no need to rotate
					print("as is")
				elif edgexy - edgexq == 1 or edgexy - edgexq == -3:
					thisarray = [edgexq, edgexy, sides[sides.index(edgexw)-1], edgexw]
				else:
					thisarray = [edgexq, edgexy, sides[sides.index(edgexy)-1], edgexw]

			else:
				x = grid[i][j] # me
				q = grid[i-1][j] # above
				y = grid[i][j+1] # right
				z = grid[i+1][j] # bottom
				w = grid[i][j-1] # left

				(edgexq, edgeyq, flipxq) = findMatchingEdge(ids_to_edges, x, q)
				(edgexy, edgeyx, flipxy) = findMatchingEdge(ids_to_edges, x, y)
				(edgexz, edgezx, flipxz) = findMatchingEdge(ids_to_edges, x, z)
				(edgexw, edgewx, flipxw) = findMatchingEdge(ids_to_edges, x, w)

				thisarray = [edgexq, edgexy, edgexz, edgexw]
			
			print("array", thisarray)
			if j == 0:
				tiles.append([findOrientation(ids_to_tiles[x], thisarray)])
			else:
				tiles[i].append(findOrientation(ids_to_tiles[x], thisarray))


	print(tiles)
	
	imagegrid = assembleImage(tiles, height, width)
	prettyPrintTiles(imagegrid)
	return imagegrid

def prettyPrintTiles(numpyArray):
	(rows, cols) = numpyArray.shape
	for r in range(rows):
		print("".join(numpyArray[r].tolist()))


def assembleImage(tiles, height, width):
	result = numpy.array([])
	for i in range(height):
		tilerow = numpy.array([])

		for j in range(width):
			# print("ij", i, j)
			if j == 0:
				tilerow = removeBorders(tiles[i][j]) 
			else:
				tilerow = numpy.concatenate((tilerow, removeBorders(tiles[i][j])), axis = 1)
			
		if i == 0:
			result = tilerow
		else:
			result = numpy.vstack((result, tilerow))
		# print(tilerow)

	return result
	# print("result", result)

def removeBorders(nptile):
	return nptile[1:9, 1:9]

def getNumpyEdges(nptile):
	left, right = nptile[:,0], nptile[:,9]
	return ["".join(nptile[0].tolist()), "".join(right), "".join(nptile[9].tolist()), "".join(left)]

def findOrientation(tile, orientarray):
	t = numpy.array( [
		#[int(x) for x in line.replace('#', '1').replace('.', '0')]
		[x for x in line]
			for line in tile
	])
	edges = getEdges(tile)
	# print("orientarray", orientarray)
	for x in orientarray:
		print(edges[x])
	result = [ edges[x] for x in orientarray]
	# print("result", result)
	for o in tileOrientations(t):
		edgeso = getNumpyEdges(o)
		match = 0
		for i in range(4):
			if result[i] == edgeso[i] or result[i] == edgeso[i][::-1]:
				match += 1
		if match == 4:
			return o
	print("No match")

def tileOrientations(tile):
	for r in range(4):
		a = numpy.rot90(tile, r)
		yield a
		yield numpy.fliplr(a)
		yield numpy.flipud(a)
		yield numpy.flipud(numpy.fliplr(a))

def findMatchingEdge(ids_to_edges, grid1, grid2):
	for i, j in product(range(0,4), repeat=2):
		if ids_to_edges[grid1][i] == ids_to_edges[grid2][j]:
			return (i, j, False) # Flip?
		if ids_to_edges[grid1][i] == ids_to_edges[grid2][j][::-1]:
			return (i, j, True)


def prettyPrintGrid(grid):
	for i in range(10):
		print(grid[i])

def testAlignGrids():
	result = 20899048083289
	f = open('data/day20_input_test.txt', 'r')
	lines = f.readlines()

	if alignGrids(lines) == result:
		print("testAlignGrids Pass")
	else:
		print("testAlignGrids Fail")

def testFindWaterRoughness():
	result = 273
	f = open('data/day20_input_test.txt', 'r')
	lines = f.readlines()

	if findWaterRoughness(lines) == result:
		print("testFindWaterRoughness Pass")
	else:
		print("testFindWaterRoughness Fail")

def main():
	# testAlignGrids()
	#testFindWaterRoughness()

	f = open('data/day20_input.txt', 'r')
	lines = f.readlines()
	#alignGrids(lines)
	findWaterRoughness(lines)

if __name__ == '__main__':
	main()

TEST_INPUT = [
	# "esew",
	# "nwwswee",
	"sesenwnenenewseeswwswswwnenewsewsw",
	"neeenesenwnwwswnenewnwwsewnenwseswesw",
	"seswneswswsenwwnwse",
	"nwnwneseeswswnenewneswwnewseswneseene",
	"swweswneswnenwsewnwneneseenw",
	"eesenwseswswnenwswnwnwsewwnwsene",
	"sewnenenenesenwsewnenwwwse",
	"wenwwweseeeweswwwnwwe",
	"wsweesenenewnwwnwsenewsenwwsesesenwne",
	"neeswseenwwswnwswswnw",
	"nenwswwsewswnenenewsenwsenwnesesenew",
	"enewnwewneswsewnwswenweswnenwsenwsw",
	"sweneswneswneneenwnewenewwneswswnese",
	"swwesenesewenwneswnwwneseswwne",
	"enesenwswwswneneswsenwnewswseenwsese",
	"wnwnesenesenenwwnenwsewesewsesesew",
	"nenewswnwewswnenesenwnesewesw",
	"eneswnwswnwsenenwnwnwwseeswneewsenese",
	"neswnwewnwnwseenwseesewsenwsweewe",
	"wseweeenwnesenwwwswnew",
]

# Super useful for representing hex tiles: https://www.redblobgames.com/grids/hexagons
def doLobbyLayout(input):
	black_tiles = set()
	for line in input:
		(x, y, z) = (0, 0, 0) # ref tile

		# e, se, sw, w, nw, and ne
		#print(line)
		southeast = line.count("se")
		line = line.replace("se", "")
		southwest = line.count("sw")
		line = line.replace("sw", "")
		northeast = line.count("ne")
		line = line.replace("ne", "")
		northwest = line.count("nw")
		line = line.replace("nw", "")
		east = line.count("e")
		west = line.count("w")
		# print("e, se, sw, w, nw, and ne:", east, southeast, southwest, west, northwest, northeast)
		x = east + northeast - west - southwest
		y = west + northwest - east - southeast
		z = southwest + southeast - northeast - northwest
		 
		# print("xyz", x, y, z)
		if (x, y, z) in black_tiles:
			# print("flipping white")
			black_tiles.remove((x, y, z))
		else:
			# print("flipping black")
			black_tiles.add((x, y, z))
	# print(black_tiles)
	result = len(black_tiles)
	print("LOBBY LAYOUT RESULT:", result)
	return result, black_tiles

# Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
def doLobbyArt(input, num_days):
	black_tiles = doLobbyLayout(input)[1]

	for i in range(num_days):
		to_black = set()
		to_white = set()
		for b in black_tiles:
			adj_tiles = generateAdjacentTiles(b)
			#print("adjacent_tiles for black", b, adj_tiles)
			adj_black = set()
			adj_white = set()
			for a in adj_tiles:
				if a in black_tiles:
					adj_black.add(a)
				else:
					adj_white.add(a)
			for aw in adj_white:
				aw_adj = generateAdjacentTiles(aw)
				aw_blackcount = 0
				for x in aw_adj:
					if x in black_tiles:
						aw_blackcount += 1
				if aw_blackcount == 2:
					# flip to black
					to_black.add(aw)

			if len(adj_black) == 0 or len(adj_black) > 2:
				# flip to white
				to_white.add(b)
			#print("black", len(adj_black), "white", len(adj_white))
		# now do the flipping
		# print("flipblack", len(to_black), to_black)
		# print("flipwhite", len(to_white), to_white)

		black_tiles.update(to_black)
		black_tiles -= to_white
		print("Day", i+1, ":",len(black_tiles))

		print(black_tiles)


	result = len(black_tiles)
	print("RESULT:", result)
	return result

def testLobbyLayout():
	result = 10
	if doLobbyLayout(TEST_INPUT)[0] == result:
		print("testLobbyLayout Pass")
	else:
		print("testLobbyLayout Fail")

def generateAdjacentTiles(tile):
	adjacent_tiles = set()
	adjacent_tiles.add((tile[0], tile[1]+1, tile[2]-1))
	adjacent_tiles.add((tile[0], tile[1]-1, tile[2]+1))
	adjacent_tiles.add((tile[0]+1, tile[1], tile[2]-1))
	adjacent_tiles.add((tile[0]-1, tile[1], tile[2]+1))
	adjacent_tiles.add((tile[0]-1, tile[1]+1, tile[2]))
	adjacent_tiles.add((tile[0]+1, tile[1]-1, tile[2]))
	return adjacent_tiles

def testLobbyArt():
	result = 2208
	if doLobbyArt(TEST_INPUT, 100) == 2208:
		print("testLobbyArt Pass")
	else:
		print("testLobbyArt Fail")		

def main():
	# testLobbyLayout()
	testLobbyArt()

	f = open('data/day24_input.txt', 'r')
	lines = f.readlines()
	# doLobbyLayout(lines)
	doLobbyArt(lines, 100)


if __name__ == '__main__':
	main()
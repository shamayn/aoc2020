import math

TEST_INPUT = [
			"F10",
			"N3",
			"F7",
			"R90",
			"F11",
]
WINDS = [ "N", "E", "S", "W"]

class Coordinates:
	shipx = 0
	shipy = 0
	# Waypoint coordinates, relative to the ship
	wpx = 10 
	wpy = 1

	def __init_(self, x, y):
		self.shipx = x
		self.shipy = y

	def setWayPoint(x, y):
		self.wpx = x
		self.wpy = y

	def __str__(self):
		return "ship {},{} waypoint {},{}".format(self.shipx, self.shipy, self.wpx, self.wpy)


def findManhattanDistance1(input):
	xpos = 0
	ypos = 0
	current_direction = "E"
	for instruction in input:
		(xpos, ypos, current_direction) = nav(instruction, xpos, ypos, current_direction)
		print(xpos, ypos, current_direction)
	return abs(xpos) + abs(ypos)

def findManhattanDistance2(input):
	coords = Coordinates()
	for instruction in input:
		coords = nav2(instruction, coords)
		print(coords)
	result = abs(coords.shipx) + abs(coords.shipy)
	print("RESULT:", result)
	return result

# part 1 only
def nav(instruction, x, y, current_direction):
	action = instruction[0]
	val = int(instruction[1:])
	print(action, val, x, y)
	if action == "F":
		return move(x, y, current_direction, current_direction, val)
	elif action == "L" or action == "R":
		print("rotating direction")
		if action == "L":
			val = val * -1
		return rotate(x, y, current_direction, val)
	else:
		return move(x, y, current_direction, action, val)
	return (x, y, current_direction)

# part 2 only
# Action N means to move the waypoint north by the given value.
# Action S means to move the waypoint south by the given value.
# Action E means to move the waypoint east by the given value.
# Action W means to move the waypoint west by the given value.
# Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
# Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
# Action F means to move forward to the waypoint a number of times equal to the given value.
def nav2(instruction, coords):
	action = instruction[0]
	val = int(instruction[1:])
	print(action, val)
	if action == "F":
		# move the ship towards the waypoint
		#return move(x, y, current_direction, current_direction, val)
		coords.shipx += coords.wpx * val
		coords.shipy += coords.wpy * val 

	elif action == "L" or action == "R":
		# rotate around the ship
		(coords.wpx, coords.wpy) = rotateWaypoint(coords.wpx, coords.wpy, val, action == "R")
	else:
		# N/S/E/W, move the waypoint
		(coords.wpx, coords.wpy) = move(coords.wpx, coords.wpy, action, val)
	return coords

# this works for waypoints too
def move(x, y, action, value):
	if action == "E":
		x += value
	elif action == "W":
		x -= value
	elif action == "N":
		y += value
	elif action == "S":
		y -= value
	return (x, y)

def rotate(x, y, current_direction, val):
	currpos = WINDS.index(current_direction)
	newpos = currpos + int(val/90)
	if newpos >= 4:
		newpos = newpos % 4
	direction = WINDS[newpos]
	return (x, y, direction)

def rotateWaypoint(x, y, degrees, clockwise=True):
	newx = x
	newy = y
	rotations = math.floor(degrees / 90)
	for i in range(rotations):
		if clockwise == True:
			(newx, newy) = (newy, -newx)
		else:
			(newx, newy) = (-newy, newx)
	return (newx, newy)

def testRotateWaypoint():
	if rotateWaypoint(10, 4, 90) == (4, -10): 
		print("testRotateWaypoint Pass")
	else:
		print("testRotateWaypoint Fail")	


def testFindManhattanDistance():
	if findManhattanDistance1(TEST_INPUT) == 25:
		print("testFindManhattanDistance Pass")
	else:
		print("testFindManhattanDistance Fail")	

def testFindManhattanDistance2():
	if findManhattanDistance2(TEST_INPUT) == 286:
		print("testFindManhattanDistance2 Pass")
	else:
		print("testFindManhattanDistance2 Fail")	

def main():
	#testFindManhattanDistance1()
	# testFindManhattanDistance2()
	#testRotateWaypoint()

	inputList = []

	f = open('data/day12_input.txt', 'r')
	lines = f.readlines()

	for line in lines:
		inputList.append(line.strip())

	# print("len:", len(inputList))
	# print(findManhattanDistance(inputList))
	findManhattanDistance2(inputList)


if __name__ == '__main__':
	main()
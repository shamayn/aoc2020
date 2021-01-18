TEST_INPUT = [ 5764801, 17807724]
INPUT = [8421034, 15993936]


def findEncryptionKey(input):
	card_pk = input[0]
	door_pk = input[1]
	card_loop_size = findLoopSize(card_pk) # 8
	door_loop_size = findLoopSize(door_pk) # 11

	key1 = transform(card_pk, door_loop_size)
	key2 = transform(door_pk, card_loop_size)

	if key1 != key2:
		print("keys don't match")
	print("RESULT", key1)
	return key1

def findLoopSize(pk):
	# assume initial subject number is 7
	loop_size = 1
	subject_number = 7
	val = 1
	while True:
		val = val * subject_number
		val = val % 20201227
		if val == pk:
			break
		loop_size += 1
	print("found loop size:", loop_size)
	return loop_size


# To transform a subject number, start with the value 1. Then, a number of times called the loop size, perform the following steps:
# - Set the value to itself multiplied by the subject number.
# - Set the value to the remainder after dividing the value by 20201227.
def transform(pk, loop_size):
	val = 1
	for i in range(loop_size):
		val = val * pk
		val = val % 20201227
	print("transformed", val)
	return val


def testFindEncryptionKey():
	result = 14897079
	if findEncryptionKey(TEST_INPUT) == result:
		print("testFindEncryptionKey Pass")
	else:
		print("testFindEncryptionKey Fail")		

def main():
	testFindEncryptionKey()
	findEncryptionKey(INPUT)


if __name__ == '__main__':
	main()
from collections import deque

TEST_INPUT = [
"Player 1:",
"9",
"2",
"6",
"3",
"1",
"Player 2:",
"5",
"8",
"4",
"7",
"10",
]

TEST_INFINITE_INPUT = [
	"Player 1:",
	"43",
	"19",
	"Player 2:",
	"2",
	"29",
	"14",
]

def playCombat(input):
	playerdecks = parseDecks(input)

	while len(playerdecks[1]) > 0 and len(playerdecks[2]) > 0:
		cards = [playerdecks[1].popleft(), playerdecks[2].popleft()]
		print("pop", cards)
		winindex = cards.index(max(cards)) + 1
		playerdecks[winindex].append(max(cards))
		playerdecks[winindex].append(min(cards))

		print(1, list(playerdecks[1]))
		print(2, list(playerdecks[2]))
	
	wincards = list(playerdecks[winindex])
	# 0 -> len
	# n-1 -> 1
	score = getScore(wincards)
	print("SCORE", score)
	return score

def getScore(cards):
	return sum([(len(cards) - i) * cards[i] for i, x in enumerate(cards)])

def parseDecks(input):
	playerid = 0
	playerdeck0 = []
	playerdeck1 = []
	for line in input:
		if line.strip() == "": continue
		if line.startswith("Player"):
			playerid = int(line[7])
		else:
			if playerid == 1:
				playerdeck0.append(int(line.strip()))
			elif playerid == 2:
				playerdeck1.append(int(line.strip()))

	return (playerdeck0, playerdeck1)
	#return playerdecks

# if both players have at least as many cards in their own decks as the number on the card
# they just dealt, the winner of the round is
# determined by recursing into a sub-game of Recursive Combat.
def playRecursiveCombat(input):
	(deck0, deck1) = parseDecks(input)

	(winner, score) = doPlayRC(deck0, deck1, 1)
	return score



def doPlayRC(deck0, deck1, gameid):
	winindex = -1
	score = 0
	past_rounds_0 = []
	past_rounds_1 = []

	print("Playing Game", gameid)
	round = 1
	while len(deck0) > 0 and len(deck1) > 0:
		print("Begin round", round)
		print(0, deck0)
		print(1, deck1)
		if deck0 in past_rounds_0 and deck1 in past_rounds_1 and \
			past_rounds_0.index(deck0) == past_rounds_1.index(deck1): 			
			winindex = 0
			windeck = deck0
			score = getScore(deck0)
			print("The winner is player 0 by default, score", score)
			print("pastrounds")
			print(past_rounds_0)
			print(past_rounds_1)
			return (winindex, score)

		past_rounds_0.append(deck0)
		past_rounds_1.append(deck1)
		cards = [deck0[0], deck1[0]]
		deck0 = deck0[1:]
		deck1 = deck1[1:]
		
		print("pop", cards)
		if len(deck0) >= cards[0] and len(deck1) >= cards[1]:
			# move to subgame

			newdeck1 = deck0[0:cards[0]]
			newdeck2 = deck1[0:cards[1]]
			print("starting subgame with", newdeck1, newdeck2)
			(winindex, score) = doPlayRC(newdeck1, newdeck2, gameid+1)
		else:
			winindex = cards.index(max(cards))
		if winindex == 1:
			deck1.append(cards[1])
			deck1.append(cards[0])
			score = getScore(deck1)

		elif winindex == 0:
			deck0.append(cards[0])
			deck0.append(cards[1])
			score = getScore(deck0)

		round += 1
		print("Winner of this round, player", winindex)
		# print(0, playerdecks[0])
		# print(1, playerdecks[1])

	print("The winner of game", gameid, "is Player", winindex, "Score", score)
	return (winindex, score)




def testPlayCombat():
	result = 306
	if playCombat(TEST_INPUT) == result:
		print("testPlayCombat Pass")
	else:
		print("testPlayCombat Fail")

def testPlayRecursiveCombat():
	result = 291
	if playRecursiveCombat(TEST_INPUT) == result:
		print("testPlayRecursiveCombat Pass")
	else:
		print("testPlayRecursiveCombat Fail")
	#playRecursiveCombat(TEST_INFINITE_INPUT);

def main():
	#testPlayCombat()
	# testPlayRecursiveCombat()

	f = open('data/day22_input.txt', 'r')
	lines = f.readlines()
	#playCombat(lines)
	playRecursiveCombat(lines)

if __name__ == '__main__':
	main()
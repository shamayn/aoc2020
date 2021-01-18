import re

TEST_INPUT = [
"mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
"trh fvjkl sbzzf mxmxvkd (contains dairy)",
"sqjhc fvjkl (contains soy)",
"sqjhc mxmxvkd sbzzf (contains fish)",
]

def findNonAllergens(input):
	ingredientsbyfood = allergensbyfood = []
	allergendict = dict()
	pattern = re.compile("^([a-zA-Z\s]+) \(contains ([a-z,\s]+)\)")
	allingredients = set()
	mapped_ingredients = set()
	for line in input:
		result = pattern.match(line.strip())
		ibf = result.group(1).split(" ")
		abf = result.group(2).split(", ")
		ingredientsbyfood.append(ibf)
		allergensbyfood.append(abf)
		for a in abf:
			ingset = set()
			for i in ibf:
				ingset.add(i)
				allingredients.add(i)
			if a not in allergendict:
				allergendict[a] = ingset
			else:
				allergendict[a] = allergendict[a].intersection(ingset)

	has_multiples = True
	while has_multiples:
		has_multiples = False
		for a in allergendict:
			print("allergen", a, allergendict[a])
			if len(allergendict[a]) == 1:
				ing = next(iter(allergendict[a]))
				print("ing", ing)
				for al in allergendict:
					if al != a:
						if ing in allergendict[al]:
							allergendict[al].remove(ing)
						if len(allergendict[al]) > 1:
							has_multiples = True

	for a in allergendict:
		mapped_ingredients.update(allergendict[a])


	unallergenic_ingredients = allingredients.difference(mapped_ingredients)
	print(allingredients)
	print(unallergenic_ingredients)
	count = sum([countOccurrences(ingredientsbyfood, ing) for ing in unallergenic_ingredients])
	print("COUNT", count)

	sortedallergens = list(allergendict.keys())
	sortedallergens.sort()
	print(",".join([next(iter(allergendict[x])) for x in sortedallergens]))
	return count


def countOccurrences(ingredientsbyfood, ingredient):
	count = 0
	for food in ingredientsbyfood:
		if ingredient in food:
			count += 1
	return count

def testFindNonAllergens():
	result = 5

	if findNonAllergens(TEST_INPUT) == result:
		print("testFindNonAllergens Pass")
	else:
		print("testFindNonAllergens Fail")

def main():
	testFindNonAllergens()

	f = open('data/day21_input.txt', 'r')
	lines = f.readlines()
	findNonAllergens(lines)

if __name__ == '__main__':
	main()
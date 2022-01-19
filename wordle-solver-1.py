# include a quoted and comma separated word list
# you can find one in wordle source code or put any word list in here you want to use
# i've provided a recent word list from wordle in the repo
# other wordle clones may use different dictionaries, keep that in mind
words = ["words"]

letters = {
	'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0,
	'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0,
	'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
	's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0,
	'y':0, 'z':0
}

ranks = {
	'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0,
	'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0,
	'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
	's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0,
	'y':0, 'z':0
}

# count how often letters appear in the dictionary
for word in words:
	score = 0
	# there's a couple ways to approach this, take your pick and experiment with results
	#check = ''.join(set(word))  # unique letters per word   (rationale: "how many words have this letter?")
	check = word                # all letters in dictionary (rationale: "how many times does this letter appear in the dictionary?")
	for x in range(0, len(check)):
		letters[check[x]] += 1
letters_sorted = {k: v for k, v in sorted(letters.items(), key=lambda item: item[1], reverse=True)}

# find max count
lmax = 0
for letter in letters_sorted:
	lv = letters_sorted[letter]
	if lv > lmax:
		lmax = lv

# rank = just normalized values
for letter in letters_sorted:
	ranks[letter] = letters_sorted[letter] / lmax
rank_sorted = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}

# score every word in the dictionary based on rank
wmax = 0
words_scored = {}
for word in words:
	score = 0
	# score unique letters in words
	# rationale: the more duplicate letters in a word the lower this word falls in rank.
	#           we want to try the most number of unique letters per guess.
	check = ''.join(set(word))
	for x in range(0,len(check)):
		score += ranks[check[x]]
	lv = round(score, 5)
	if lv > wmax:
		wmax = lv
	words_scored[word] = lv
words_sorted = {k: v for k, v in sorted(words_scored.items(), key=lambda item: item[1], reverse=True)}

# normalize all word scores from 0 to 100, because it's nicer to read
for word in words_sorted:
	words_sorted[word] = int(round((words_sorted[word] / wmax) * 100, 0))

# now that we've scored the entire dictionary, lets start guessing
def MakeGuess(green, yellow, black):
	# check for some basic issues
	if len(green) != len(yellow):
		print("green and yellow are different sizes.")
		return

	# if no inputs are given return the full word space
	if ''.join(yellow) == '     ' and black == '' and ''.join(green) == '     ':
		# just return first 10 results for brevity
		n = 0
		toplist = {}
		for k,v in words_sorted.items():
			toplist[k] = v
			n += 1
			if n > 9:
				break
		print(toplist)
		return

	# otherwise, let's get rolling...
	newlist = {}
	wordlen = len(green)
	for word in words_sorted:
		# track stages of algorithm
		stages = {'green':False, 'black':False, 'yellow':False}
		
		# first the easiest, match on known-good guesses, green letters
		m1 = [False] * wordlen
		for x in range(0, wordlen):
			m1[x] = True if green[x] == ' ' else False
			if m1[x] == False and word[x] == green[x]:
				m1[x] = True
		if all(m1):
			stages['green'] = True

		# then filter out words that don't have black letters in them
		m2 = [False] * len(black)
		if stages['green'] == True:
			if black == '':
				stages['black'] = True
			else:
				for x in range(0, len(black)):
					if black[x] not in word:
						m2[x] = True
				if all(m2):
					stages['black'] = True

		# finally find words with variations of yellow letters per-slot
		if stages['black']:
			if ''.join(yellow) == '     ':
				stages['yellow'] = True
			else:
				yset = list(filter(lambda x: x != ' ', ''.join(yellow)))
				m3 = [False] * len(yset) 
				m4 = [True] * len(yellow)
				# keep words that contain a yellow letter
				for x in range(0, len(yset)):
					if yset[x] in word:
						m3[x] = True
				# remove words that contain a yellow word in slot 'x'
				for x in range(0, wordlen):
					for i in yellow[x]:
						if i == word[x]:
							m4[x] = False
							next
				if all(m3) and all(m4):
					stages['yellow'] = True

		# if all stages above passed then save this word
		if stages['yellow']:
			newlist[word] = words_sorted[word]

	# display the results
	if len(newlist) <= 10:
		print(newlist)
	else:
		# just return first 10 results for brevity
		n = 0
		toplist = {}
		for k,v in newlist.items():
			toplist[k] = v
			n += 1
			if n > 9:
				break
		print(toplist)

# ** for green letters, one letter per slot or a space for no value
# ** for black letters, append after each turn;  'abcdef'
# ** for yellow letters,
#   1. if you have multiple guesses per slot add them together;  'abc','yz',...
#   2. if you have the same yellow letter in multiple slots, just add them in each slot as needed; 'a','a',...
#   3. if you have no entry for the yellow enter it as a space; ' '

# as you progress through the challenge add/update the state of the game below and run the function again
# you'll get multiple words in response, choose one with the highest score and keep on going

MakeGuess(
	# green letters, per slot
	[' ',' ',' ',' ',' '],
	# yellow letters, per slot
	[' ',' ',' ',' ',' '],
	# black letters, slot doesn't matter, just keep adding every turn
	'' 
)

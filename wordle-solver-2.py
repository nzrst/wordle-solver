
# !! this script differs from wordle-solver-1 as all statistics and ranks are built **per-slot instead of per-word**

# include a quoted and comma separated word list
# you can find one in wordle source code or put any word list in here you want to use
# i've provided a recent word list from wordle in the repo
# other wordle clones may use different dictionaries, keep that in mind
words = ["words"]

# per slot letter distribution
ranks = []
letters = []
for i in range(0,5):
	letters.append({
		'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0,
		'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0,
		'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
		's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0,
		'y':0, 'z':0
	})
	ranks.append({
		'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0,
		'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0,
		'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
		's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0,
		'y':0, 'z':0
	})

# count how often letters appear in each index of each word in the dictionary
for word in words:
	for x in range(0, len(word)):
		letters[x][word[x]] += 1

# sort, because nice for output/reviewing
letters_sorted = [0] * 5
for i in range(0,len(letters)):
	letters_sorted[i] = {k: v for k, v in sorted(letters[i].items(), key=lambda item: item[1], reverse=True)}

# find maximum value for each index of each word
vmax = [0] * len(letters_sorted)
for x in range(0, len(letters_sorted)):
	for letter in letters_sorted[x]:
		lv = letters_sorted[x][letter]
		if lv > vmax[x]:
			vmax[x] = lv

# normalize everything
for x in range(0, len(letters_sorted)):
	for letter in letters_sorted[x]:
		ranks[x][letter] = letters_sorted[x][letter] / vmax[x]

# again sorting is nice if you want to dump output and review
#ranks_s1_sorted = [0] * len(ranks_s1)
#for x in range(0, len(ranks_s1)):
#	ranks_s1_sorted[x] = {k: v for k, v in sorted(ranks_s1[x].items(), key=lambda item: item[1], reverse=True)}
#print(ranks_s1_sorted)

# score all words
wmax = 0
words_scored = {}
for word in words:
	score = 0
	for x in range(0, len(word)):
		score += ranks[x][word[x]]
	lv = round(score, 5)
	if lv > wmax:
		wmax = lv
	words_scored[word] = lv

# normalize scores between 0 to 100
words_sorted = {k: v for k, v in sorted(words_scored.items(), key=lambda item: item[1], reverse=True)}
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
				# edge cases/overrides;
				wordx = list(word)
				for x in range(0, wordlen):
					# green letters per-slot override the filter
					if green[x] in black:
						wordx[x] = ' '
					# yellow letters in all slots override the filter
					yset = set(''.join(yellow))
					if word[x] in yset:
						for i in range(0, wordlen):
							if wordx[i] == word[x]:
								wordx[i] = ' '
				# once green and yellow exclusions are accounted for apply filter
				for x in range(0, len(black)):
					if black[x] not in wordx:
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
# ** the presence of a letter in yellow and green groups overrides that same letter in the black group

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

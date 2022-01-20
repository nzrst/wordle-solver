# wordle-solver

Provided are two scripts for solving wordle.
The first script builds statistics of letters across the entire word.
The second script builds statistics of letters in specific slots.

Regarding how to use the script, below is a quick and dirty step-by-step for how to update the game state in the MakeGuess function from start to completion.

This solves the wordle puzzle from Jan 20, 2022.


## Initial guess:
MakeGuess(
	[' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' '],
	''
)
## results:
{'arose': 100, 'aeros': 100, 'soare': 100, 'arise': 98, 'raise': 98, 'aesir': 98, 'reais': 98, 'serai': 98, 'aloes': 97, 'stoae': 97}
## hint: it's always "arose"

## 1. Guess "arose"
## yellow = ro, black = ase
MakeGuess(
	[' ',' ',' ',' ',' '],  # green
	[' ','r','o ',' ',' '], # yellow
	'ase' # black
)
## Results:
{'lirot': 68, 'intro': 67, 'nitro': 67, 'roily': 64, 'nidor': 64, 'loric': 64, 'milor': 63, 'toric': 63, 'rigol': 62, 'corni': 62}
## The wordle dictionary has names and fake/weird words in it, so i chose next best word "intro" here

## 2. Guess "intro"
## yellow = tro, black = in
MakeGuess(
	[' ',' ',' ',' ',' '],  # green
	[' ','r','ot','r','o'], # yellow
	'asein' # black
)
## Results:
{'dorty': 59, 'tumor': 59, 'routh': 58, 'porty': 57, 'torch': 56, 'borty': 56, 'throb': 55, 'forty': 54, 'forth': 53, 'worth': 53}
## dorty and tumor tied, so i chose "tumor"

## 3. Guess "tumor"
## green = o, yellow = tr, black = um
MakeGuess(
	[' ',' ',' ','o',' '],   # green
	['t','r','ot','r','ro'], # yellow
	'aseinum' # black
)
## Results:
{'robot': 48}

## 4. Only a single match, so fourth guess "robot", success!

import pokerlib

#import pklibtt4

from pokerlib import WINNERS_PATTERN_DICT
from pokerlib import ALL_PATTERN_DICT
import pprint
import time


numoftrials = 1000

game = 4  # 4 card omaha, or 5 or 6.

numberOfPlayers = 6

dealingUntil = 5  # 3=Flop, 4=Turn 5=River



# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

gametext = game - 4
dealuntiltext = dealingUntil - 3
games = ['Standard 4 Card Omaha','PL Big O (5 Card)','6 Card Omaha']
dealuntillist = ['just the flop.','flop and turn.','until the river.']


print('\n')
print('--------------------------------------------------------')
print('==================  SERPENT POKERLIB  ==================')
print('--------------------------------------------------------')
print()
print('--------------------------------------------------------')
print('Omaha Winning Hand Pattern Counter -- Version 2.0 Alpha')
print('--------------------------------------------------------')
print()
print('Currently dealing for:')
print('Number of trials = %s' %(numoftrials))
print('%s handed, %s, dealing %s' % (numberOfPlayers, games[gametext], dealuntillist[dealuntiltext]))
print()
print('Generating hands... (Be patient. This can take a while.)')



startTime = time.time()


for i in range(numoftrials):

    board, peoples = pokerlib.dealAll(numberOfPlayers,game,dealingUntil)

    for hand in peoples:
        pokerlib.ALL_PATTERN_DICT_append(hand)

    omahaPlayersBest = pokerlib.omahaPlayersEval(board,peoples)

    pokerlib.WINNERS_PATTERN_DICT_append(omahaPlayersBest['hand'])


print('Processing...')


for k in WINNERS_PATTERN_DICT:
    WINNERS_PATTERN_DICT[k].append(ALL_PATTERN_DICT[k])



print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
print('Writing to file...(O%s_PATTERN_DICT.py)' % (game))



fo = open('O%s_PATTERN_DICT.py' % (game), 'w')
fo.write('PATTERN_DICT = ')
fo.write(pprint.pformat(WINNERS_PATTERN_DICT))
fo.close()


endTime = time.time()
timeTook = endTime - startTime

m, s = divmod(timeTook, 60)
h, m = divmod(m, 60)
s = round(s,3)

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
print('Write successful.')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - ')

if m > 0:
	if h > 0:
		print('Operation took %s hours, %s minutes and %s seconds.' % (h, m, s))
	else:
		print('Operation took %s minutes and %s seconds.' % (m, s))
else:

	print('Operation took %s seconds.' % (round(timeTook, 3)))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
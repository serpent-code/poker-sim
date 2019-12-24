import pokerlib


print('\n')
print('--------------------------------------------------------')
print('==================  SERPENT POKERLIB  ==================')
print('--------------------------------------------------------')
print()
print('This is a test file dealing a board and holdem hands')
print('to players and determining the winner and the')
print('5 card combination he used to win.')
print('--------------------------------------------------------')
print()


board, peoples = pokerlib.dealAll(6,2,5)


print('Board is : \n')
print(pokerlib.pformat(board))
print('----------=================---------')
print('Players hands are : \n')
print(pokerlib.pformat(peoples))

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~+++++~~~~~~~~~~~~~~~')




holdemPlayersEval= pokerlib.holdemPlayersEval(board,peoples)

winnerid = holdemPlayersEval['id']
winnerid_eng = pokerlib.eng_position(winnerid)

winnercombo = holdemPlayersEval['combination']
winnerhand = holdemPlayersEval['hand']

winnerscore = holdemPlayersEval['score']
winnerscore_eng = pokerlib.eng_score(winnerscore)


print('The winner is : \n')

print('%s player in the list.\n'%(winnerid_eng))

print('Hand : %s'%(pokerlib.pformat(winnerhand)))
print()
print('5 card combination : ')
print(pokerlib.pformat(winnercombo))
print()

print('Score : %s'%(winnerscore_eng))



print('------------------------------------')

print('Winning hand pattern is : ')

print(pokerlib.patterMaker(holdemPlayersEval['hand']))

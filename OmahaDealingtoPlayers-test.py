import pokerlib


print('\n')
print('--------------------------------------------------------')
print('==================  SERPENT POKERLIB  ==================')
print('--------------------------------------------------------')
print()
print('This is a test file dealing a board and omaha hands')
print('to players and determining the winner and the')
print('5 card combination he used to win.')
print('--------------------------------------------------------')
print()


board, peoples = pokerlib.dealAll(6,4,5)


print('Board is : \n')
print(pokerlib.pformat(board))
print('----------=================---------')
print('Players hands are : \n')
print(pokerlib.pformat(peoples))

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~+++++~~~~~~~~~~~~~~~')



# board=['3C','4C', '5D', '6D', '11S']
# peoples=[['2C','12C','14H','13H'],['7C','8S','12S','13S']]




omahaPlayersEval= pokerlib.omahaPlayersEval(board,peoples)

winnerid = omahaPlayersEval['id']
winnerid_eng = pokerlib.eng_position(winnerid)

winnercombo = omahaPlayersEval['combination']
winnerhand = omahaPlayersEval['hand']

winnerscore = omahaPlayersEval['score']
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

print(pokerlib.patterMaker(omahaPlayersEval['hand']))

# print('------------------------------------')

# pprinter.pprinter(b)



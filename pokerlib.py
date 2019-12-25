# ------------------------------------------------
# =============== SERPENT POKERLIB ===============
# ------------------------------------------------
# Copyright 2016, Serpentcode.
# Released under GPL v3.
#
# See LICENSE for details.
#
# ------------------------------------------------
# SERPENTLABS DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,  
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR 
# PURPOSE. IN NO EVENT SHALL SERPENTLABS BE LIABLE FOR ANY SPECIAL,INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE
# USE OR PERFORMANCE OF THIS SOFTWARE.



import random
import itertools
import copy
import pickle
import pprint
from collections import Counter, deque
from operator import itemgetter

import core_eval as serpentlib_dll



    
def getNewSortedDeck():
    global DECK
    DECK = deque()
    for i in range (2,15):
        for c in ('C','S','H','D'):
            DECK.append(str(i)+c)
    return DECK
DECK = getNewSortedDeck()



def spread(x=None):
    if x == None:
        board = [None] * 5
    else:
        board = [None] * x
    for index,card in enumerate(board):
        while True:
            potentialCard = random.choice(DECK)
            if potentialCard not in board:
                board[index] = potentialCard
                break

    return board


        
def dealAll(numOfPlayers=6, eachPlayerGets=2, dealUntil=5):
    board = []
    deck=copy.copy(DECK)
    random.shuffle(deck)

    playersHands = [[] for i in range(numOfPlayers)]

    for hand in playersHands:
        while len(hand) < eachPlayerGets:
            hand.append(deck.pop())

    for card in range(dealUntil):
        board.append(deck.pop())

    return board , playersHands



def omahaPlayersEval(board,listOfHands):
    return serpentlib_dll.omahaPlayersEval(board,listOfHands)


def holdemPlayersEval(board,listOfHands):
    return serpentlib_dll.holdemPlayersEval(board,listOfHands)



def patterMaker(hand):

    num_list = deque()
    suit_list = deque()
    pattern = deque()

    for card in hand:
        num_list.append(int(card [:-1]))
        suit_list.append(card [-1])

    num_list_CounterDict=Counter(num_list)
    sortedlist = num_list_CounterDict.most_common()
    sortedlist.sort(key=itemgetter(1,0), reverse=True)

    for tup in sortedlist:
        for num in tup:
            pattern.append(str(num))

    
    suit_list_CounterDict = {k:suit_list.count(k) for k in set(suit_list)}
    suit_Counter_vals_sorted = sorted(suit_list_CounterDict.values(), reverse=True)

    if len(suit_Counter_vals_sorted) == 1:
        suited = 'S'

    elif suit_Counter_vals_sorted[0] >= 2:
        if suit_Counter_vals_sorted[1] >= 2:
            suited = 'SS'
        else:
            suited = 'S'
    else:
        suited = 'N'

    pattern.append(suited)

    pattern = '.'.join(pattern)

    return pattern



WINNERS_PATTERN_DICT = {} 
def WINNERS_PATTERN_DICT_append(hand):

    global WINNERS_PATTERN_DICT

    pattern = patterMaker(hand)

    try:
        WINNERS_PATTERN_DICT[pattern][0] += 1

    except KeyError:
        WINNERS_PATTERN_DICT[pattern] = [1]


ALL_PATTERN_DICT = {}
def ALL_PATTERN_DICT_append(hand):

    global ALL_PATTERN_DICT

    pattern = patterMaker(hand)

    try:
        ALL_PATTERN_DICT[pattern] += 1

    except KeyError:
        ALL_PATTERN_DICT[pattern] = 1


def pformat(input_list): #input_list is a list of strs or list of list of strs
    newlist=[]
    for item in input_list:
        if type(item) is list:
            newlist_sub=[]
            for card in item:
                newlist_sub.append(symboler(card))
            newlist.append(newlist_sub)
        else:
            newlist.append(symboler(item))
    return pprint.pformat(newlist)


def symboler(cardstring):
    replace = {'10':'T','11':'J','12':'Q','13':'K','14':'A',
               'C':9827,'S':9824,'H':9829,'D':9830}

    cardnum = cardstring[:-1]
    cardsuit = cardstring[-1]

    if cardnum in replace:
        cardnum_new = replace[cardnum]
    else:
        cardnum_new = cardnum

    cardsuit_newnum = replace[cardsuit]
    cardsuit_newsym = chr(cardsuit_newnum)

    return cardnum_new + cardsuit_newsym

def eng_position(number):
    pos = {0:'1st',1:'2nd',2:'3rd',3:'4th',
    4:'5th',5:'6th',6:'7th',7:'8th',8:'9th',9:'10th'}

    if number in pos:
        return pos[number]

def eng_score(number):
    score = {0:'Nothing',1:'One Pair',2:'Two Pair',3:'Three of a kind',
    4:'Straight',5:'Flush',6:'Full House',7:'Four of a kind',8:'Straight Flush'}

    if number in score:
        return score[number]


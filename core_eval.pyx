
#cython:boundscheck=False

from libcpp.unordered_map cimport unordered_map
from libcpp.set cimport set as cppset
from libcpp.algorithm cimport sort as cppsort


import pickle
import itertools
from operator import itemgetter



cdef int evalHand(list hand): # hand is a list of 5, 6 or 7 cards.


    cdef int len_set_suitlist, i, len_set_numarray, tempcardnum
    cdef int* wheel_array = [2,3,4,5,14]
    cdef bint wheel = False
    cdef bint onepair = False
    cdef bint twopair = False 
    cdef bint threeofknd = False
    cdef bint straight = False
    cdef bint flush = False
    cdef bint fullhouse3 = False

    cdef int[5] numarray
    cdef cppset[int] numset
    cdef unordered_map[int, int] cpphash_counter



    suit_list = []
    for i,card in enumerate(hand):

        suit_list.append(card [-1])

        numarray[i] = int(card [:-1])


    len_set_suitlist = len(set(suit_list))


    for i in range(5):
        numset.insert(numarray[i])

    len_set_numarray = numset.size()

    for i in range(5):
        tempcardnum = numarray[i]
        if cpphash_counter.count(tempcardnum) == 1:

            cpphash_counter[tempcardnum] += 1

            if cpphash_counter[tempcardnum] == 4:
                return 7 # Four Of A Kind

            if cpphash_counter[tempcardnum] == 3:
                fullhouse3 = True

        else: 
            cpphash_counter[tempcardnum] = 1




    # Full House
    if len_set_numarray == 2 and fullhouse3 == True:
        return 6    

    else:


        #num_list_sorted = sorted(num_list)
        cppsort(numarray,numarray+5)

        if numarray == wheel_array:
            wheel = True


        if len_set_numarray == 5:
            straight = (numarray[4] - numarray[0] == 4)


        onepair = len_set_numarray == 4

        if len_set_numarray == 3:
            if fullhouse3 == True:
                threeofknd = True
            else:
                twopair = True

        if ((straight == True) or (wheel == True)):
            straight = True

        if len_set_suitlist == 1:
            flush = True



        # Nothing
        if not onepair and not twopair and not threeofknd and not straight and not flush:
            return 0 

        # One Pair        
        elif onepair and not straight and not flush:
            return 1

        # Two Pair
        elif twopair and not straight and not flush:
            return 2

        # Three Of A Kind
        elif threeofknd and not straight and not flush:
            return 3

        # Straight
        elif straight and not flush:
            return 4

        # Flush
        elif not straight and flush:
            return 5

        # Straight Flush
        elif straight and flush:
            return 8


cdef omahaEval(list board, list hand): # hand is a list omaha hand. 4, 5 or 6 cards.

    cdef int numofcombs, i

    hand_combos = [list(x) for x in itertools.combinations(iter(hand),2)]

    board_combos = [list(x) for x in itertools.combinations(iter(board),3)]

    numofcombs = len(hand_combos) * len(board_combos)

    combos_list = [{'id': None ,'combination': None , 'score':None} for i in range(numofcombs)]


    for i, (h_combo, b_combo) in enumerate([(h_combo,b_combo) for h_combo in hand_combos for b_combo in board_combos]):

        to_eval = h_combo + b_combo
        combos_list[i]['id'] = i
        combos_list[i]['combination'] = to_eval
        combos_list[i]['score'] = evalHand(to_eval)

    top_id_hc = topRanker(combos_list)

    top_item = next((dc for dc in combos_list if dc['id'] == top_id_hc), None)

    return top_item



def omahaPlayersEval(list board, list listOfHands):

    cdef int index, top_id_h

    playersInfo = [{'id':None, 'hand': None, 'combination':None, 'score':None} for i in range(len(listOfHands))]

    for index,hand in enumerate(listOfHands):
        playersInfo[index]['id'] = index
        playersInfo[index]['hand'] = hand

        omahaeval_output = omahaEval(board, hand)

        playersInfo[index]['combination'] = omahaeval_output['combination']
        playersInfo[index]['score'] = omahaeval_output['score']

    playersInfo.sort(key=itemgetter('score'), reverse=True)

    if len(playersInfo) > 1:
        if playersInfo[0]['score'] == playersInfo[1]['score']:
            top_id_h = topRanker(playersInfo)

            return next((item for item in playersInfo if item['id'] == top_id_h), None)

        else:

            return playersInfo[0]




cdef int topRanker(list input_listOfDicts):

    cdef int highestScore, i, j, top_id
    cdef list wheel_14 = [14, 5, 4, 3, 2]
    cdef list wheel_5 = [5, 4, 3, 2, 1]

    workingList = pickle.loads(pickle.dumps(input_listOfDicts, -1))
    workingList.sort(key=itemgetter('score'), reverse=True)

    highestScore = workingList[0]['score']

    workingList=[item for item in workingList if item['score'] == highestScore]



    for i,handDict in enumerate(workingList):
        for j,card in enumerate(handDict['combination']):
            workingList[i]['combination'][j] = int(card [:-1])

        if highestScore == 4 or highestScore == 8:
            workingList[i]['combination'].sort(reverse=True)

            if workingList[i]['combination'] == wheel_14:
                workingList[i]['combination'] = wheel_5

        elif highestScore == 0 or highestScore == 5:
            workingList[i]['combination'].sort(reverse=True)

        else:
            sortedlist=[(k,workingList[i]['combination'].count(k)) for k in set(workingList[i]['combination'])] 
            sortedlist.sort(key=itemgetter(1,0), reverse=True)
            workingList[i]['combination'] = sortedlist

    workingList.sort(key=itemgetter('combination'), reverse=True)

    top_id = workingList[0]['id']

    return top_id




cdef holdemEval(list board, list hand): # hand is 2 cards. Board is 3,4 or 5 cards.

    cdef int numofcombs, i

    boardnhand = hand + board

    hand_combos = [list(x) for x in itertools.combinations(iter(boardnhand),5)]

    numofcombs = len(hand_combos)

    combos_list = [{'id': None ,'combination': None , 'score':None} for i in range(numofcombs)]


    for i, hand_combo in enumerate(hand_combos):

        combos_list[i]['id'] = i
        combos_list[i]['combination'] = hand_combo
        combos_list[i]['score'] = evalHand(hand_combo)

    top_id_hc = topRanker(combos_list)

    top_item = next((dc for dc in combos_list if dc['id'] == top_id_hc), None)

    return top_item









def holdemPlayersEval(list board, list listOfHands):

    cdef int index, top_id_h

    playersInfo = [{'id':None, 'hand': None, 'combination':None, 'score':None} for i in range(len(listOfHands))]

    for index,hand in enumerate(listOfHands):
        playersInfo[index]['id'] = index
        playersInfo[index]['hand'] = hand

        holdemEval_output = holdemEval(board, hand)

        playersInfo[index]['combination'] = holdemEval_output['combination']
        playersInfo[index]['score'] = holdemEval_output['score']

    playersInfo.sort(key=itemgetter('score'), reverse=True)

    if len(playersInfo) > 1:
        if playersInfo[0]['score'] == playersInfo[1]['score']:
            top_id_h = topRanker(playersInfo)

            return next((item for item in playersInfo if item['id'] == top_id_h), None)

        else:

            return playersInfo[0]


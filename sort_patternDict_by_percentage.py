import importlib
import pprint
from operator import itemgetter



filename_to_be_sorted_by_winprcnt = 'COMBINED_DICT' # Without the .py extension.


# ------------------------------------------------------------------------------



module = importlib.import_module(filename_to_be_sorted_by_winprcnt, package=None)
D = module.PATTERN_DICT

for k in D:
    won = D[k][0]
    dealt = D[k][1]

    winpercent = round((won / dealt) * 100 , 2)

    D[k].append(winpercent)

LstOfTups = sorted(([k]+v for k,v in D.items()), key=itemgetter(3), reverse=True)

fo = open('%s_WINPERCENT_SORTED.py' %(filename_to_be_sorted_by_winprcnt), 'w')
fo.write('PATTERN_DICT_SORTED = ')
fo.write(pprint.pformat(LstOfTups))
fo.close()

print('%s file sorted.' %(filename_to_be_sorted_by_winprcnt))
print('%s_WINPERCENT_SORTED.py file created.'%(filename_to_be_sorted_by_winprcnt))
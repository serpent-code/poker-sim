# poker-sim
Simulating poker hands in order to evaluate starting hands ranking statistically

A programming exercise with the goal of simulating Holdem, Omaha and 5 card Omaha poker hands between varying number of psudo players (headsup, shorhand, fulltable) many times and export a ranking list of hands simply sorted by the number of hands they finish best when the flop, turn or river card is dealt. There is no folding, as there is no betting, and every hand dealt is evaluated.

The core evaluating part was rewritten in cython, both to speed it up since the simulation is supposed to run in a loop many times and also as a venture to learn cython. The cython part was tested on Anaconda python distribution under windows. I haven't tested it under different platforms and situations.

You can see one result it made for 6 handed holdem over 100k trials here: [HE_6H_100k_Result.py](https://github.com/serpent-code/poker-sim/blob/master/HE_6H_100k_Result.py)

Project was done circa 2016.

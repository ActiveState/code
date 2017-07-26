###Poker hand calculation and comparison

Originally published: 2013-05-30 18:39:24
Last updated: 2013-06-24 05:03:10
Author: Magnus Åhman

Calculates 1. the category of the hand (high card, one pair, etc...) and 2. the "kicker" values that act as tiebreakers to (possibly) distinguish two hands of the same category from each other. These two attributes, category and kickers, are then used by the cmp method to compare two hand objects and return -1, 0 or 1.
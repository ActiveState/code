###Infinite Stream Divisor

Originally published: 2010-07-21 12:50:16
Last updated: 2010-07-21 12:50:17
Author: Narayana Chikkam

Maintain an F.S.A to keep track of the consequent remainders as states, input symbols as driving actions on each state. O(N) is the time complexity to find the given large string [in some radix(R), for some specific divisor(D)], where N is the length of the Input String which confirms to the Language Rules under the alphabet. O(R*D) is the space complexity to keep the F.S.A in memory for lookup!
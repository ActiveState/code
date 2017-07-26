## Finite State Machine (FSM)

Originally published: 2002-08-23 02:47:49
Last updated: 2007-12-05 01:25:49
Author: Noah Spurrier

This recipe shows a Finite State Machine (FSM) that can be used for small parsing tasks. The code is quite simple. The bulk of it is comments. In addition to state this FSM also maintains a user defined "memory". So this FSM is a Push-down Automata (PDA) since a PDA is a FSM + memory. This module contains an example function that demonstrates a simple RPN expression evaluator.
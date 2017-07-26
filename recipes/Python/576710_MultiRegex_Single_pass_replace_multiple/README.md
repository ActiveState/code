## Multi-Regex: Single pass replace of multiple regexes

Originally published: 2009-04-03 07:59:27
Last updated: 2009-04-03 13:38:39
Author: Michael Palmer

Not really - all regexes first get combined into a single big disjunction. Then, for each match, the matching sub-regex is determined from a group name and the match object dispatched to a corresponding method, or simply replaced by a string. 
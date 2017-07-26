## Cheap-date trick; a different way to parse  
Originally published: 2012-03-06 13:59:32  
Last updated: 2012-03-06 14:08:10  
Author: Scott S-Allen  
  
... a light meal with a heavy dose of "tutorial mash" on the side.

In the constructive spirit of "more ways to solve a problem"; this is a portion of my lateral, occasionally oblique, solutions. Nothing new in le régime de grande, but hopefully the conceptual essence will amuse.

Initially started as a response to recipe 577135 which parses incremental date fragments and preserves micro-seconds where available. That script does more work than this, for sure, but requires special flow-control and iterates a potentially incumbering shopping list (multi-dimensional with some detail).

So here's a different box for others to play with. Upside-down in a sense, it doesn't hunt for anything but a numerical "pulse"; sequences of digits punctuated by other 'stuff' we don't much care about.

Missing a lot of things, intentionally, this snippet provides several examples demoin' flexibility. Easy to button-up, redecorate and extend later for show, till then the delightful commentary makes it hard enough to see bones already -- all six lines or so!

**Note:** *The core script is repeated for illustrative purposes. The first is step-by-step, the second is lean and condensed for utilitarian purposes. It is the second, shorter, version that I yanked from a file and gussied up.*

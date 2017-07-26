## determine google count by automatisation

Originally published: 2012-12-31 15:25:42
Last updated: 2012-12-31 15:33:39
Author: Peer Valhoegen

Sometimes you need o know the number of results that google gets for a specific query.\nThere are lots of scripts that claim to do that, but I didn't find any that worked.\nThey mostly rely on urllib, which is blocked by Google.\n\nThis script automates what you would do by hand.\nIt is therefore incredibly slow, but it works and seems future proof to me.\n\nYou may want to adjust the respective timespan that is waited before certain operations.\nThis script relies on the unix command xsel.\nI'm sure there are equivalent solutions on other operating systems.
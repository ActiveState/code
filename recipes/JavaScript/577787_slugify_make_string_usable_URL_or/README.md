## slugify: make a string usable in a URL or filename

Originally published: 2011-07-12 17:41:07
Last updated: 2011-07-12 17:46:49
Author: Trent Mick

"Slugify" a string so it has only alphanumeric and hyphen characters. Useful for URLs and filenames.  This is a JavaScript (node.js too) version of Recipe 577257.\n\nNote: It is missing the guarantee that only ascii characters are passed through. I don't know an NFKD equivalent in JavaScript-land.
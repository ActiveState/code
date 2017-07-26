###Quickslice decorator: Abbreviated slice arguments in functions

Originally published: 2005-05-29 20:41:36
Last updated: 2005-05-31 19:30:02
Author: Brian Beck

Sometimes I wish slice creation had a form that looked more like its invocation: [1:5], for example. This recipe allows slice arguments to be passed that look like {1:5}. NOTE: I don't recommend actually using this in practice. It will most likely just confuse any readers of your code. It is just a proof-of-concept. In an interview with Guido van Rossum, Guido was explaining the benefits of Python's built-in types. He gave an example of being able to pass slices as arguments instead of having individual start, stop and step arguments -- and this is very true. But I don't think a syntax to concisely create slices should be out of the question. (Step is not supported by this syntax, it wouldn't be possible and I rarely find myself using step anyway).
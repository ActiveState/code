## == Ruby Array#each_cons, each_slice (overlapping and non-overlapping windows onto iterable seq)Originally published: 2004-11-26 10:45:31 
Last updated: 2004-11-26 19:38:52 
Author: Gene tani 
 
Simple versions what Hamish Lawson ("getting items in batches") and Brian QUinlan ("group list into n-tuples") submitted.\n\nIterables must support indexing and len(); doesn't use itertools.
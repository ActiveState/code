## Safe Expression EvaluationOriginally published: 2004-06-14 02:10:22 
Last updated: 2004-06-14 09:56:27 
Author: Sami Hangaslammi 
 
Often, we might want to let (untrusted) users input simple Python expressions and evaluate them, but the eval-function in Python is unsafe. The restricted execution model in the rexec module is deprecated, so we need another way ensure only "safe" expressions will be evaluted: analyzing bytecodes.
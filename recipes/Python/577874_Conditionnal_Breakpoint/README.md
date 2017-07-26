###Conditionnal Breakpoint

Originally published: 2011-09-20 18:44:58
Last updated: 2011-09-20 18:49:23
Author: s_h_a_i_o 

Decorates a class so that it encounters a breakpoint for any call to class.method_name(self,*args,**kwargs), where\n- method_name is given by string\n- only if arguments meet a test: arg_test(self,*args,**kwargs) -> bool [default -> True]\n\nBehaviour easily changed for other actions than breakpoint (logging,...)
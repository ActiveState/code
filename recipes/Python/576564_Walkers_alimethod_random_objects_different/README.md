## Walker's alias method for random objects with different probablities  
Originally published: 2008-11-16 15:05:51  
Last updated: 2008-11-16 15:05:51  
Author: denis   
  
an example, strings A B C or D with probabilities .1 .2 .3 .4 --

    abcd = dict( A=1, D=4, C=3, B=2 )
      # keys can be any immutables: 2d points, colors, atoms ...
    wrand = Walkerrandom( abcd.values(), abcd.keys() )
    wrand.random()  # each call -> "A" "B" "C" or "D"
                    # fast: 1 randint(), 1 uniform(), table lookup
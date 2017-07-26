## nth-Root

Originally published: 2009-07-27 04:41:45
Last updated: 2011-01-29 12:29:38
Author: Fouad Teniou

I realised a lack of an nth root function within Python maths' modules, even though, you could fulfil the task by using the power function, and I wrote nth-Root program.\nHowever, I used Newton’s method Xn+1 = Xn - f(Xn)/f’(Xn) , n = 1,2,3... and worked out myself the formula to solve the equation X^(b) - a for nth-root(a) as follows:\nXn+1 = 1/b((b-1)Xn + a/Xn^(b-1)). Though my program nth-Root uses a generator to generate each value approximation in the sequence from its predecessor, and it display the nth root value once two equal values are generated. \nNowadays Scientifics’ calculators display 9 digits to the right of a decimal point and my program nth-Root displays a 16 figures  precision  to the right of a decimal point.
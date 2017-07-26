## NPV / IRR / Payback Analysis  
Originally published: 2009-03-11 01:52:18  
Last updated: 2013-09-06 23:04:55  
Author: Alia Khouri  
  
A few financial functions for quick analysis of an investment opportunity and a series of associated cashflows.

As a module, it currently provides straightforward and easy to understand implementations of the Net Present Value (NPV), Internal Rate of Return (IRR), and Payback Period functions.

As a script, it provides a simple command line interface which integrates the above functions into a concise analysis of the investment opportunity.

        usage: invest discount_rate [cashflow0, cashflow1, ..., cashflowN]
            where 
                discount_rate is the rate used to discount future cashflows 
                                 to their present values
                cashflow0 is the investment (always a negative value)
                cashflow1 .. cashflowN values can be positive (net inflows) 
                                                     or
                                                     negative (net outflows)

Here is an example of actual usage and output:

    $ ./invest 0.05 -10000 6000 6000 6000
    ----------------------------------------------------------------------
    year      0        1      2      3     
    cashflow  -10,000  6,000  6,000  6,000 

    Discount Rate: 5.0%

    Payback: 1.67 years
        IRR: 36.31%
        NPV: 6339.49

    ==> Approve Investment of 10,000
    ----------------------------------------------------------------------


*Note*: A check of the output of the Microsoft Excel NPV function against that of the function implemented here reveals a curious discrepancy/bug in the way Excel calculates its NPV. For further details see: http://www.tvmcalcs.com/blog/comments/the_npv_function_doesnt_calculate_net_present_value/

Furthermore, the method used to calculate the IRR is rough to say the least and fails at fewer than 3 entries. Please use the secant method along the lines of the following haskell code from (http://www.haskell.org/haskellwiki/Haskell_Quiz/Internal_Rate_of_Return/Solution_Dolio) for greater accuracy.

    secant :: (Double -> Double) -> Double -> Double
    secant f delta = fst $ until err update (0,1)
      where
        update (x,y) = (x - (x - y) * f x / (f x - f y), x)
        err (x,y) = abs (x - y) < delta

    npv :: Double -> [Double] -> Double
    npv i = sum . zipWith (\t c -> c / (1 + i)**t) [0..]

    irr :: [Double] -> Double
    irr cashflows = secant (`npv` cashflows) (0.1**4)

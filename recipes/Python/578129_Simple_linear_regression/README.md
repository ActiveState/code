## Simple linear regression  
Originally published: 2012-05-12 10:34:10  
Last updated: 2012-05-12 13:36:55  
Author: Thomas Lehmann  
  
**What?**

 * It's about forecasting.
 * It's about calculating a linear function.
 * *Details I found*: http://www.faes.de/Basis/Basis-Statistik/Basis-Statistik-Korrelation-Re/basis-statistik-korrelation-re.html (in german)

Also I don't know how the formula have been created the practical part was very easy to me. I have verified one example (see code) using Open Office Calc (I've learned: you can display the formula for the trend line as well as the coefficient of correlation - great).

**Why?**

 * In recipe 578111 I'm printing out current error rate for different training sessions in mental arithmetic.
 * Anyway I would like to be able to given information - approximately - about how many you have improved since you train yourself.

**What has changed?**

 * **Revision2**: Didn't compile with Jython 2.5.3b1 because of not supported exception syntax. Now it does work without exception.
 * **Revision3**: Test data row for failure not removed.
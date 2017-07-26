## pick all combinations of items in buckets  
Originally published: 2015-09-05 07:36:01  
Last updated: 2015-09-05 07:39:42  
Author: yota   
  
Let be a number of buckets, containing each, a variable number of items. This function return all combinations possible of one item picked out of each bucket

example, with three buckets {ba, be, bi}, {ka, ko, ku, ke} and {to, ty}, the function enumerate as such: 

     0. ba-ka-to
     1. ba-ka-ty
     2. ba-ko-to
     3. ba-ko-ty
     4. ba-ku-to
     5. ba-ku-ty
     6. ba-ke-to
     7. ba-ke-ty
     8. be-ka-to
     9. be-ka-ty
    10. be-ko-to
    11. be-ko-ty
    12. be-ku-to
    13. be-ku-ty
    14. be-ke-to
    15. be-ke-ty
    16. bi-ka-to
    17. bi-ka-ty
    18. bi-ko-to
    19. bi-ko-ty
    20. bi-ku-to
    21. bi-ku-ty
    22. bi-ke-to
    23. bi-ke-ty
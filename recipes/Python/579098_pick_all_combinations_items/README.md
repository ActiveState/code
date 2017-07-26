## pick all combinations of items in buckets

Originally published: 2015-09-05 07:36:01
Last updated: 2015-09-05 07:39:42
Author: yota 

Let be a number of buckets, containing each, a variable number of items. This function return all combinations possible of one item picked out of each bucket\n\nexample, with three buckets {ba, be, bi}, {ka, ko, ku, ke} and {to, ty}, the function enumerate as such: \n\n     0. ba-ka-to\n     1. ba-ka-ty\n     2. ba-ko-to\n     3. ba-ko-ty\n     4. ba-ku-to\n     5. ba-ku-ty\n     6. ba-ke-to\n     7. ba-ke-ty\n     8. be-ka-to\n     9. be-ka-ty\n    10. be-ko-to\n    11. be-ko-ty\n    12. be-ku-to\n    13. be-ku-ty\n    14. be-ke-to\n    15. be-ke-ty\n    16. bi-ka-to\n    17. bi-ka-ty\n    18. bi-ko-to\n    19. bi-ko-ty\n    20. bi-ku-to\n    21. bi-ku-ty\n    22. bi-ke-to\n    23. bi-ke-ty
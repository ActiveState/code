## Simple Universally Unique ID (UUID or GUID)

Originally published: 2003-08-02 06:36:42
Last updated: 2003-08-02 06:36:42
Author: Carl Free Jr

This is a short & sweet UUID function. Uniqueness is based on network address, time, and random.\n\nAnother good point: does not create a "hot spot" when used in a b-tree (database) index. In other words, if your IDs look something like "abc100" and "abc101" and "abc102"; then they will all hit the same spot of a b-tree index, and cause the index to require frequent reorganization. On the other hand, if your IDs look more like "d29fa" and "67b2c" and "e5d36" (nothing alike); then they will spread out over the index, and your index will require infrequent reorganization.
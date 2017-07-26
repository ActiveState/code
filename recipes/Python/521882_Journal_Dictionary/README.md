###Journal Dictionary and Mixin for Transactions

Originally published: 2007-06-03 13:52:14
Last updated: 2007-06-03 13:52:14
Author: Oran Looney

First, a Dictionary class that 'journals' sets and dels.  The changes in the journal can either be applied (like committing a transaction) or wiped (like rollback.)\n\nThe journalled dictionary is used to implement a JournalledMixin class that gives journalling/transaction behavor to any object.\n\nLinks and discussion below.
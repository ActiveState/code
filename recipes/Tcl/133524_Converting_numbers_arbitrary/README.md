###Converting numbers from arbitrary bases

Originally published: 2002-06-17 15:12:58
Last updated: 2002-06-17 15:12:58
Author: andreas kupries

Origin: http://wiki.tcl.tk/1067\nAuthor: Michael A. Cleverly\n\nThe other day someone on OpenACS.org asked [http://openacs.org/bboard/q-and-a-fetch-msg.tcl?msg_id=0000k2&topic_id=11&topic=OpenACS] for a Tcl proc that would convert a base-62 number into a base-10 integer. I replied with a version I'd written. Here is a slightly expanded one. convert_number employs some Salt and Sugar which I quite like.\n\n(One caveat is that base_n_to_decimal will either return an incorrect answer or generate an error for really large numbers that are > than 2147483647.)\n
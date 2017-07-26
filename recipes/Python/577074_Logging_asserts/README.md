###Logging asserts

Originally published: 2010-02-28 13:15:40
Last updated: 2010-03-01 03:22:43
Author: d.schlabing 

This tries to marry assert statements with logging. If you use asserts together with logging and the script stops because an assertion is not fulfilled, you will not find any information about this in the logs.\nUnless you do something like this:\n    \n    meal = ["eggs", "bacon", "spam"]\n    try:\n        assert "spam" not in meal, "But I don't like spam!"\n    except AssertionError:\n        log.exception("But I don't like spam!")\n        raise\n\nWith the proposed recipe a somewhat similar behaviour can be achieved by:\n    \n    log_assert("spam" not in meal, "But I don't like spam!")\n
## Monkey-patch execnet with more ssh settings, port, identity file, non-interactive

Originally published: 2011-01-15 16:34:59
Last updated: 2011-01-15 16:35:00
Author: Dima Tisnek

execnet ( http://codespeak.net/execnet/ ) is pretty cool, but its ssh support needs a few tweaks, here they are.\n\nThis snipped is a monkey patch, not a diff, import it and you can use execnet.makeportgateway instead of makegateway.\n\nAdapt to your needs even more!
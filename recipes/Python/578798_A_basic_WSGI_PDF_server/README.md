###A basic WSGI PDF server

Originally published: 2013-12-26 18:45:35
Last updated: 2013-12-26 18:45:35
Author: Vasudev Ram

This recipe shows how to create a rudimentary Python WSGI server that can serve PDF. I had seen a post on the Python Reddit about how to create 'a basic WSGI server (aka "enough to make a website without using a framework")'. Thought of modifying it to serve PDF content (hard-ccded, though, not dynamic content, just as a basic example). This is the result. It's meant for learning, as was the original from which it was adapted, not for production use. It requires my xtopdf toolkit and the Reportlab toolkit, v1.21\n\n\n\n
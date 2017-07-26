from pyembed.core import PyEmbed
html = PyEmbed().embed('http://www.youtube.com/watch?feature=player_detailpage&v=3oFm4MYbb9o')
print html

Run the above code with Python.
Then paste the output (which will be enclosed in an iframe tag) in an HTML page. This will result in the multimedia content referred to by the URL, being embedded in the page. E.g. If the content is a YouTube video, that video will be embedded in the HTML page.

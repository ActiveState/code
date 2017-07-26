def SequenceToUnorderedList(seq):

	html_code = "<ul>" + "\n\n"

	for item in seq:
		html_code = html_code + "<li>" + item + "\n"

	html_code = html_code + "\n" + "</ul>" 

	return html_code

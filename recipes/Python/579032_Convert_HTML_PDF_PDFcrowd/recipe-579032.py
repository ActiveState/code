# Demo program to show how to use the PDFcrowd API
# to convert HTML content to PDF.
# Author: Vasudev Ram - www.dancingbison.com

import pdfcrowd

try:
    # create an API client instance
    # Dummy credentials used; to actually run the program, enter your own.
    client = pdfcrowd.Client("user_name", "api_key")
    client.setAuthor('author_name')
    # Dummy credentials used; to actually run the program, enter your own.
    client.setUserPassword('user_password')

    # Convert a web page and store the generated PDF in a file.
    pdf = client.convertURI('http://www.dancingbison.com')
    with open('dancingbison.pdf', 'wb') as output_file:
        output_file.write(pdf)
    
    # Convert a web page and store the generated PDF in a file.
    pdf = client.convertURI('http://jugad2.blogspot.in/p/about-vasudev-ram.html')
    with open('jugad2-about-vasudevram.pdf', 'wb') as output_file:
        output_file.write(pdf)

    # convert an HTML string and save the result to a file
    output_file = open('html.pdf', 'wb')
    html = "My Small HTML File"
    client.convertHtml(html, output_file)
    output_file.close()

except pdfcrowd.Error, why:
    print 'Failed:', why

import sys, smtplib, MimeWriter, base64, StringIO

message = StringIO.StringIO()
writer = MimeWriter.MimeWriter(message)
writer.addheader('Subject', 'The kitten picture')
writer.startmultipartbody('mixed')

# start off with a text/plain part
part = writer.nextpart()
body = part.startbody('text/plain')
body.write('This is a picture of a kitten, enjoy :)')

# now add an image part
part = writer.nextpart()
part.addheader('Content-Transfer-Encoding', 'base64')
body = part.startbody('image/jpeg')
base64.encode(open('kitten.jpg', 'rb'), body)

# finish off
writer.lastpart()

# send the mail
smtp = smtplib.SMTP('smtp.server.address')
smtp.sendmail('from@from.address', 'to@to.address', message.getvalue())
smtp.quit()

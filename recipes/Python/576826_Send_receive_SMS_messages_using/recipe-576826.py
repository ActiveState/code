import textmagic.client

# Use your username and API password to create a client
client = textmagic.client.TextMagicClient('your_username', 'your_api_password')

# Send a message and store its message id
result = client.send("Hello, World!", "1234567890")
message_id = result['message_id'].keys()[0]

# Now you can retrieve the delivery status using the message id
response = client.message_status(message_id)
status = response[message_id]['status']

# Replies to your outgoing messages are delivered to your TextMagic Inbox
# This is how you receive messages from your Inbox
received_messages = client.receive(0)
messages_info = received_messages['messages']
for message_info in messages_info:
  print "%(text)s received from %(from)s" % message_info

# Delete a message from your Inbox
client.delete_reply(message_info['message_id'])

# Get your account balance
balance = client.account()['balance']

# Find the country and cost of a telephone number
response = client.check_number('44123456789')
info = response['44123456789']
country = info['country']
credits = info['price']

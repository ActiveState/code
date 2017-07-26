#!/bin/sh
# Usage: /full/path/to/reminder "Your text here with spaces inside double quotes."
text=$1
if [ "$1" == "" ]
then
	text="You have started reminder, what have you forgotten?"
	echo ""
	echo 'Usage: /full/path/to/reminder "Your text here with spaces inside double quotes."'
fi
> /tmp/reminder.sh
chmod 755 /tmp/reminder.sh
echo "#!/bin/sh" >> /tmp/reminder.sh
echo "printf '\033[1m\033[12;3f$text\033[0m\n\n\n'" >> /tmp/reminder.sh
echo "sleep 3" >> /tmp/reminder.sh
echo "exit 0" >> /tmp/reminder.sh
while true
do
	# Display your reminder for about 3 seconds...
	xterm -e /tmp/reminder.sh &
	# Use Ctrl-C to stop after xterm has closed down...
	sleep 30
done

"""

A script to capture network streams using VLC, based on a scheduler. It was originally designed for mpeg transport streams on the local network, but can be modified for other stream types. It runs as an infinite loop and can be terminated by pressing "Q" (see below for key commands).

Last updated 19th August 2015.


Dependencies:
- My fork of Danny Yoo's getch()-like function: https://code.activestate.com/recipes/579095
- vlc.py http://wiki.videolan.org/Python_bindings


The end user will need to create two JSON files in the same directory as the script:
- capture.json to store the network stream/channel information
- schedule.json to store the timer recordings


Example format of capture.json:

{
	"stream name one":"stream one address",
	"stream name two":"stream two address"
}


Example format of schedule.json:

[
	{ "start":"2015-08-18 18:08:00", "duration":1, "channel":"stream name one", "programme":"Test Recording"},
	{ "start":"2015-08-18 19:20:00", "end":"2015-08-18 20:20:00", "channel":"stream name two", "programme":"Second Recording"}
]

You can specify either the length of the recording or an end datetime. The programme field is simply a descriptor (the recording will be named YYYYMMDD_HHMMSS_channel_programme.ts).


Commands:

Once the script is running, it will automatically parse the channel list and schedule. There are three basic commands, trigger by key presses:

- pressing "R" reloads the schedule and will update any upcoming scheduled recordings
- pressing "C" reloads the channel list
- pressing "Q" exits the script


"""

import os
import sys
import json
import datetime
import time
import getch # External py file
import vlc # External py file

# Static global variables
PATH = os.path.abspath(os.path.dirname(__file__))
SCRIPT = os.path.basename(__file__)

# FUTURE IMPROVEMENT
# Add optionParser to allow user to specify config file
config_file = os.path.join(PATH, 'capture.json')
timer_file = os.path.join(PATH, 'schedule.json')
log_file = os.path.join(PATH, "%s.log" % os.path.splitext(SCRIPT)[0])



def writePrint(text):
    '''Write to the log and print to the screen.'''

    f = open(log_file, 'a')
    print text
    f.write(text)
    f.close()


def timePrint(text, dt=None):
    '''Print to STDOUT with a datetime prefix. If no timestamp is provided,
    the current date and time will be used.'''

    if dt is None:
        now = datetime.datetime.now()
        dt = now.strftime('%H:%M:%S')

    writePrint("%s  %s" % (dt, text))


def indentPrint(text):
    '''Print to STDOUT with an indent matching the timestamp printout in
    timePrint().'''

    writePrint("\t    %s" % (text))


def loadChannelConfig(silent=False):
    '''Load the stream configuration file.'''

    f = open(config_file, 'r')
    cjson = json.load(f)
    f.close()

    channels = len(cjson.keys())
    if not silent:
        writePrint("%d channels available." % channels)

    return cjson


def loadSchedule(silent=False):
    '''Load the scheduled recordings file.'''

    # Read the schedule file
    f = open(timer_file, 'r')
    rjson = json.load(f)
    f.close()

    recordings = len(rjson)
    if not silent:
        writePrint("%d recordings scheduled." % recordings)

    return rjson


def parseSchedule(schedule, channels):
    '''Parse the schedule and return a list of timings to check against.'''

    recordings = {}
    schedules = len(schedule)

    for x in xrange(0, schedules):
        entry = schedule[x] # should be a JSON object

        # Recording start time
        start = entry['start']
        dt = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

        channel = entry['channel'] # Extract the channel name

        # Check for an endtime or a duration
        endtime = None
        offset = None

        if 'end' in entry:
            endtime = datetime.datetime.strptime(entry['end'], '%Y-%m-%d %H:%M:%S')

        if 'duration' in entry:
            duration = entry['duration'] # Get the timer duration (minutes)
            offset = dt + datetime.timedelta(minutes=duration)

        # Check to see which gives the longer recording - the duration or end timestamp
        if offset is not None and endtime is not None:
            if offset > endtime:
                endtime = offset

        elif offset is not None:
            endtime = offset

        elif endtime is None and offset is None:
            # No valid duration/end time
            writePrint('End or duration missing for scheduled recording %s (%s).' % (dt, channel))
            continue

        elif endtime is not None and endtime < dt:
            # End is earlier than the start!
            writePrint('End timestamp earlier than start! Cannot record %s (%s).' % (dt, channel))

        programme = None

        if 'programme' in entry:
            programme = entry['programme']

        addr = channels[channel] # Get the channel URL
        pid = '%s %s' % (start, channel)

        recordings[pid] = {
            'url': addr,
            'channel': channel,
            'start':dt,
            'end': endtime,
            'programme': programme,
            'sid': x # Basic schedule id - this can be improved upon later to make it a unique identifier that is read/written by the schedule editor (or a database primary key)
        }

    return recordings


def initialiseTS(channel, tstamp=datetime.datetime.now(), programme=None, ext='.ts'):
    '''Check for a free filename.'''

    # Get list of existing files
    d = set(x for x in os.listdir(PATH) if (x.endswith(ext)))

    # Filename template
    fn = [tstamp.strftime('%Y%m%d_%H%M%S'), channel]

    # If we have a programme name, add it to the filename
    if programme is not None:
        programme.replace(' ', '_') # Replace whitespace with underscores
        fn.append(programme)

    fn_str = '_'.join(fn)
    name = '%s%s' % (fn_str, ext)
    n = 0

    # While a filename matches the standard naming pattern, increment the
    # counter until we find a spare filename
    while name in d:
        name = '%s_%d%s' % (fn_str, n, ext)
        n += 1

    return os.path.join(PATH, name)


def recordStream(instream, outfile):
    '''Record the network stream to the output file.'''

    inst = vlc.Instance() # Create a VLC instance
    p = inst.media_player_new() # Create a player instance
    cmd1 = "sout=file/ts:%s" % outfile
    media = inst.media_new(instream, cmd1)
    media.get_mrl()
    p.set_media(media)
    return (inst, p, media)


def initialise(silent=False):
    '''Load the channel list and scheduled recordings.'''

    # Initial startup
    channels = loadChannelConfig(silent) # Get the available channels
    schedule = loadSchedule(silent) # Get the schedule
    recordings = parseSchedule(schedule, channels) # Parse the schedule information

    return recordings


def reloadSchedule(existing, running):
    '''Reload the list of scheduled recordings.'''

    now = datetime.datetime.now() # Get the current timestamp
    revised = initialise(True) # Get the revised schedule

    # Get the schedule id for each of the running recordings
    running_ids = {}
    for r in running:
        sid = running[r]['sid']
        running_ids[sid] = r

    # Get the schedule id for each of the upcoming recordings
    upcoming_ids = {}
    for e in existing:
        sid = existing[e]['sid']
        upcoming_ids[sid] = e

    # Number of new entries
    new_rec = 0

    # Compare the revised schedule against the existing
    for r in revised:
        data = revised[r]
        sched_id = data['sid']
        endtime = data['end']

        # If this recording is already running
        if sched_id in running_ids:
            h = running_ids[sched_id]

            # TO DO: When the SID is implemented properly with the
            # schedule editor, there will be no need to check any of these
            # fields apart from the end time

            # Check if it's the same channel and programme
            ch = (data['channel'] == running[h]['channel'])
            pr = (data['programme'] == running[h]['programme'])

            # If it's the same channel and programme, check if we need to revise the end time
            if pr and ch and endtime != running[h]['end']:
                timePrint('Changed end time for running recording:')

                if data['programme'] is not None:
                    indentPrint('%(programme)s (%(channel)s)' % data)
                else:
                    indentPrint('%s' % h)

                indentPrint('%s to %s' % (running[h]['end'].strftime('%Y-%m-%d %H:%M:%S'), endtime.strftime('%Y-%m-%d %H:%M:%S')))

                running[h]['end'] = endtime

        # Otherwise, it's not a currently-running recording
        # We only want to consider programmes that haven't finished yet
        elif endtime > now:
            if sched_id in upcoming_ids:
                s = upcoming_ids[sched_id]

                # Remove the old data so that it can be replaced with the new
                temp = existing.pop(s, None)

                # Check if it's the same channel and programme
                ch = (data['channel'] == temp['channel'])
                pr = (data['programme'] == temp['programme'])

                # Only notify a change if it's the same programme
                if temp != data and ch and (pr or temp['programme'] is None):
                    timePrint('Changes made to scheduled recording:')

                    if data['programme'] is not None:
                        indentPrint('%(programme)s (%(channel)s)' % data)
                    else:
                        indentPrint('%s' % s)

            else:
                new_rec += 1

            existing[r] = data

    if new_rec > 0:
        timePrint('Added %d new scheduled recordings.' % new_rec)

    return (existing, running)


def main():
    recordings = initialise() # Load the channels and schedule
    handles = {} # Create storage for the recording handles
    busy = True

    while busy:
        now = datetime.datetime.now() # Get the current timestamp

        # Check existing recordings
        hs = handles.keys()
        for h in hs:
            data = handles[h]
            end = data['end']
            channel = data['channel']
            programme = data['programme']

            if now > end:
                timePrint("Finished recording %s (%s)." % (programme, channel))
                try:
                    data['player'].stop() # Stop playback
                    data['player'].release() # Close the player
                    data['inst'].release() # Destroy the instance
                except Exception, err:
                    timePrint("Unable to destroy player reference due to error:")
                    writePrint(str(err))
                handles.pop(h) # Remove the handle to the player

        # Loop through the schedule
        rs = recordings.keys()
        for r in rs:
            data = recordings[r] # Schedule entry details
            start = data['start']
            end = data['end']
            channel = data['channel']
            programme = data['programme']

            # If we're not recording the stream but we're between the
            # start and end times for the programme, record it
            if r not in handles and (now > start):
                if (now < end):
                    # Determine a suitable output filename
                    fn = initialiseTS(channel, start, programme)

                    # Create the VLC instance and player
                    (inst, player, media) = recordStream(data['url'], fn)

                    # Store the handle to the VLC instance and relevant data
                    handles[r] = {
                        'inst': inst,
                        'player': player,
                        'media': media,
                        'end': end,
                        'programme': programme,
                        'channel': channel,
                        'sid': data['sid']
                    }

                    # Start the stream and hence the recording
                    player.play()
                    timePrint("Started recording:")
                    indentPrint("%s (%s)" % (programme, channel))
                    indentPrint("%s to %s" % (start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')))

                else:
                    timePrint("Missed scheduled recording:")
                    indentPrint("%s (%s)" % (programme, channel))
                    indentPrint("%s to %s" % (start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')))

                # Remove the item from the schedule to prevent it being
                # processed again
                recordings.pop(r)

        k = len(handles.keys()) + len(recordings.keys())
        #busy = k > 0

        # Loop for 10 seconds, checking for a keyhit
        n = 10
        while n > 0:
            keyhit = getch.getch()
            n -= 1

            # Check if we have a keyhit
            if keyhit is not None:
                kl = keyhit.lower()

                # Reload schedule
                if 'r' in kl:
                    timePrint('Reloading schedule...')
                    (recordings, handles) = reloadSchedule(recordings, handles)

                # Reload channel config
                if 'c' in kl:
                    pass

                # Quit
                if 'q' in kl:
                    # Add request for confirmation here
                    busy = False

        if not busy:
            timePrint("Exiting...\n")


if __name__ == '__main__':
    main()

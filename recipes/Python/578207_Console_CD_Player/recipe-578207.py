import pygame.cdrom as face

def main():
    face.init()
    count = face.get_count()
    if count == 0:
        raw_input('There is no cdrom drive.')
    elif count == 1:
        cmd(face.CD(0))
    else:
        num = which_CD(count)
        if num != -1:
            cmd(face.CD(num))
    face.quit()

def which_CD(maximum):
    print 'You have %s cdrom drives.' % maximum
    while True:
        try:
            num = int(raw_input('What cdrom drive do you want to use? '))
        except ValueError:
            print 'Please try typing a number.'
        except:
            return -1
        else:
            if 0 < num <= maximum:
                return num - 1
            print 'The number is out of range.'

def cmd(disc):
    disc.init()
    total = disc.get_numtracks()
    table = map(disc.get_track_audio, range(total))
    if sum(table) == 0:
        print 'This is not an audio CD.'
    else:
        index = {}
        count = 0
        for i, b in enumerate(table):
            if b:
                count += 1
                index[count] = i
        cmd_line(disc, index)
    disc.stop()
    disc.quit()

def cmd_line(disc, index):
    while True:
        prompt = get_prompt()
        if prompt == 'nop':
            pass
        elif prompt == 'help':
            print 'help:  get this message'
            print 'nop:   does nothing'
            print 'total: shows total tracks'
            print 'play:  plays the selected track'
            print 'quit:  leaves the commmand line'
        elif prompt == 'total':
            print 'There are %s tracks.' % len(index)
        elif prompt == 'play':
            track = get_track(len(index))
            if track != -1:
                disc.play(index[track])
            else:
                print 'Okay ...'
        elif prompt == 'quit':
            return
        else:
            print '"%s" cannot be understood.' % prompt

def get_prompt():
        try:
            return raw_input('>>> ').lower()
        except:
            return 'nop'

def get_track(maximum):
    while True:
        try:
            num = int(raw_input('What track should be played? '))
        except ValueError:
            print 'Please try typing a number.'
        except:
            return -1
        else:
            if 0 < num <= maximum:
                return num
            print 'The number is out of range.'

if __name__ == '__main__':
    main()

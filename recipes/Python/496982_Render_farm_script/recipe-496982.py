#!/usr/bin/python

import os, sys, threading, time

# Dimensions for recommended povray rendering
recommended_width, recommended_height = 751, 459
povray_aspect_ratio = (1. * recommended_width) / recommended_height

def set_resolution(w, h):
    global mpeg_width, mpeg_height, povray_width, povray_height
    # mpeg_height and mpeg_width must both be even to make mpeg2encode
    # happy. The aspect ratio for video should be 4:3.
    def even(x):
        return int(x) & -2
    mpeg_width = even(w)
    mpeg_height = even(h)
    povray_height = mpeg_height
    povray_width = int(povray_aspect_ratio * povray_height)

def set_width(w):
    set_resolution(w, (3.0 / 4.0) * w)
def set_height(h):
    set_resolution((4.0 / 3.0) * h, h)

set_resolution(600, 450)

worker_list = [
    ('localhost', '/tmp/mpeg'),
    ('server', '/tmp/mpeg'),
    ('laptop', '/tmp/mpeg'),
    ('mac', '/Users/wware/tmp')
    ]

bitrate = 6.0e6

framelimit = None

povray_pretty = True

border = None

####################
#                  #
#   DEBUG STUFF    #
#                  #
####################

DEBUG = False

def linenum(*args):
    try:
        raise Exception
    except:
        tb = sys.exc_info()[2]
        f = tb.tb_frame.f_back
        print f.f_code.co_filename, f.f_code.co_name, f.f_lineno,
    if len(args) > 0:
        print ' --> ',
        for x in args:
            print x,
    print

def do(cmd, howfarback=0):
    if DEBUG:
        if False:
            try:
                raise Exception
            except:
                tb = sys.exc_info()[2]
                f = tb.tb_frame.f_back
                for i in range(howfarback):
                    f = f.f_back
                print f.f_code.co_filename, f.f_code.co_name, f.f_lineno
        print cmd
    if os.system(cmd) != 0:
        raise Exception(cmd)

############################
#                          #
#    DISTRIBUTED POVRAY    #
#                          #
############################

_which_povray_job = 0

class PovrayJob:
    def __init__(self, srcdir, dstdir, povfmt, povmin, povmax_plus_one, yuv,
                 pwidth, pheight, ywidth, yheight, textlist):

        assert povfmt[-4:] == '.pov'
        assert yuv[-4:] == '.yuv'
        self.srcdir = srcdir
        self.dstdir = dstdir
        self.povfmt = povfmt
        self.povmin = povmin
        self.povmax_plus_one = povmax_plus_one
        self.yuv = yuv
        self.pwidth = pwidth
        self.pheight = pheight
        self.ywidth = ywidth
        self.yheight = yheight
        self.textlist = textlist

    def go(self, machine, workdir):

        local = machine in ('localhost', '127.0.0.1')

        def worker_do(cmd):
            if DEBUG: print '[[%s]]' % machine,
            if local:
                # do stuff on this machine
                do(cmd, howfarback=1)
            else:
                # do stuff on a remote machine
                do('ssh %s "%s"' % (machine, cmd), howfarback=1)

        if povray_pretty:
            povray_options = '+A -V -D +X'
        else:
            povray_options = '-A +Q0 -V -D +X'

        worker_do('mkdir -p ' + workdir)
        # worker_do('find %s -type f -exec rm -f {} \;' % workdir)

        #
        # Create a shell script to run on the worker machine
        #
        global _which_povray_job
        self.scriptname = 'povray_job_%08d.sh' % _which_povray_job
        _which_povray_job += 1
        video_aspect_ratio = 4.0 / 3.0
        w2 = int(video_aspect_ratio * self.pheight)
        jpg = (self.povfmt % self.povmin)[:-4] + '.jpg'
        tgalist = ''
        povlist = ''
        scriptlines = [ ]
        scriptlines.append('cd %s' % workdir)
        # Worker machine renders a bunch of pov files to tga files
        for i in range(self.povmin, self.povmax_plus_one):
            pov = self.povfmt % i
            povlist += ' ' + pov
            tga = pov[:-4] + '.tga'
            tgalist += ' ' + tga
            scriptlines.append('povray +I%s +O%s +FT %s +W%d +H%d 2>/dev/null' %
                              (pov, tga, povray_options, self.pwidth, self.pheight))
        # Worker machine averages the tga files into one jpeg file
        scriptlines.append('convert -average %s -crop %dx%d+%d+0 -geometry %dx%d! %s' %
                           (tgalist, w2, self.pheight, (self.pwidth - w2) / 2,
                            self.ywidth, self.yheight, jpg))
        # Worker cleans up the pov and tga files, no longer needed
        scriptlines.append('rm -f %s %s' %
                           (povlist, tgalist))
        if DEBUG:
            for line in scriptlines:
                print machine + '>>> ' + line
        shellscript = open(os.path.join(self.srcdir, self.scriptname), 'w')
        for line in scriptlines:
            shellscript.write(line + '\n')
        shellscript.close()

        #
        # Copy shell script and pov files to worker
        #
        if local:
            cmd = ('(cd %s; tar cf - %s %s) | (cd %s; tar xf -)' %
                   (self.srcdir, self.scriptname, povlist, workdir))
        else:
            cmd = ('(cd %s; tar cf - %s %s) | gzip | ssh %s "(cd %s; gunzip | tar xf -)"' %
                   (self.srcdir, self.scriptname, povlist, machine, workdir))
        do(cmd)
        do('rm -f ' + os.path.join(self.srcdir, self.scriptname))
        worker_do('chmod +x ' + os.path.join(workdir, self.scriptname))

        #
        # Run the shell script on the worker
        #
        worker_do(os.path.join(workdir, self.scriptname))

        #
        # Retrieve finished image file back from worker
        #
        if DEBUG: print '[[%s]]' % machine,
        if local:
            do('cp %s %s' % (os.path.join(workdir, jpg),
                             os.path.join(self.dstdir, jpg)))
        else:
            do('scp %s:%s %s' % (machine, os.path.join(workdir, jpg),
                                 os.path.join(self.dstdir, jpg)))

        #
        # Put text on finished image, apply border, and convert to YUV
        #
        if self.textlist:
            cmd = ('convert %s -font times-roman -pointsize 30' %
                   (os.path.join(self.dstdir, jpg)))
            for i in range(len(self.textlist)):
                cmd += ' -annotate +10+%d "%s"' % (30 * (i + 1), self.textlist[i])
            if border is not None:
                cmd += ' -bordercolor black -border %dx%d' % border
            cmd += ' ' + os.path.join(self.dstdir, self.yuv)
            do(cmd)
        else:
            do('convert %s %s' %
               (os.path.join(self.dstdir, jpg),
                os.path.join(self.dstdir, self.yuv)))

        #
        # Clean up remaining files on the worker machine
        #
        worker_do('rm -f %s %s' %
                  (os.path.join(workdir, self.scriptname),
                   os.path.join(workdir, jpg)))

all_workers_stop = False

class Worker(threading.Thread):

    def __init__(self, jobqueue, machine, workdir):
        threading.Thread.__init__(self)
        self.machine = machine
        self.jobqueue = jobqueue
        self.workdir = workdir
        self.busy = True

    #
    # Each worker grabs a new jobs as soon as he finishes the previous
    # one. This allows mixing of slower and faster worker machines; each
    # works at capacity.
    #
    def run(self):
        global all_workers_stop
        while not all_workers_stop:
            job = self.jobqueue.get()
            if job is None:
                # no jobs left in the queue, we're finished
                self.busy = False
                return
            try:
                job.go(self.machine, self.workdir)
            except:
                all_workers_stop = True
                raise

class PovrayJobQueue:

    def __init__(self):
        self.worker_pool = [ ]
        self.jobqueue = [ ]
        self._lock = threading.Lock()
        for machine, workdir in worker_list:
            self.worker_pool.append(Worker(self, machine, workdir))

    def append(self, job):
        self._lock.acquire()   # thread safety
        self.jobqueue.append(job)
        self._lock.release()
    def get(self):
        self._lock.acquire()   # thread safety
        try:
            r = self.jobqueue.pop(0)
        except IndexError:
            r = None
        self._lock.release()
        return r

    def start(self):
        for worker in self.worker_pool:
            worker.start()
    def wait(self):
        busy_workers = 1
        while busy_workers > 0:
            time.sleep(0.5)
            busy_workers = 0
            for worker in self.worker_pool:
                if worker.busy:
                    busy_workers += 1
            if all_workers_stop:
                raise Exception

####################
#                  #
#    MPEG STUFF    #
#                  #
####################

params = """MPEG-2 Test Sequence, 30 frames/sec
%(sourcefileformat)s    /* name of source files */
-         /* name of reconstructed images ("-": don't store) */
-         /* name of intra quant matrix file     ("-": default matrix) */ 
-         /* name of non intra quant matrix file ("-": default matrix) */
stat.out  /* name of statistics file ("-": stdout ) */
1         /* input picture file format: 0=*.Y,*.U,*.V, 1=*.yuv, 2=*.ppm */ 
%(frames)d       /* number of frames */
0         /* number of first frame */
00:00:00:00 /* timecode of first frame */
15        /* N (# of frames in GOP) */
3         /* M (I/P frame distance) */
0         /* ISO/IEC 11172-2 stream */
0         /* 0:frame pictures, 1:field pictures */
%(width)d       /* horizontal_size */
%(height)d       /* vertical_size */
2         /* aspect_ratio_information 1=square pel, 2=4:3, 3=16:9, 4=2.11:1 */
5         /* frame_rate_code 1=23.976, 2=24, 3=25, 4=29.97, 5=30 frames/sec. */
%(bitrate)f  /* bit_rate (bits/s) */
112       /* vbv_buffer_size (in multiples of 16 kbit) */
0         /* low_delay  */
0         /* constrained_parameters_flag */
4         /* Profile ID: Simple = 5, Main = 4, SNR = 3, Spatial = 2, High = 1 */
8         /* Level ID:   Low = 10, Main = 8, High 1440 = 6, High = 4          */
0         /* progressive_sequence */
1         /* chroma_format: 1=4:2:0, 2=4:2:2, 3=4:4:4 */
2         /* video_format: 0=comp., 1=PAL, 2=NTSC, 3=SECAM, 4=MAC, 5=unspec. */
5         /* color_primaries */
5         /* transfer_characteristics */
4         /* matrix_coefficients */
%(width)d       /* display_horizontal_size */
%(height)d       /* display_vertical_size */
0         /* intra_dc_precision (0: 8 bit, 1: 9 bit, 2: 10 bit, 3: 11 bit */
1         /* top_field_first */
0 0 0     /* frame_pred_frame_dct (I P B) */
0 0 0     /* concealment_motion_vectors (I P B) */
1 1 1     /* q_scale_type  (I P B) */
1 0 0     /* intra_vlc_format (I P B)*/
0 0 0     /* alternate_scan (I P B) */
0         /* repeat_first_field */
0         /* progressive_frame */
0         /* P distance between complete intra slice refresh */
0         /* rate control: r (reaction parameter) */
0         /* rate control: avg_act (initial average activity) */
0         /* rate control: Xi (initial I frame global complexity measure) */
0         /* rate control: Xp (initial P frame global complexity measure) */
0         /* rate control: Xb (initial B frame global complexity measure) */
0         /* rate control: d0i (initial I frame virtual buffer fullness) */
0         /* rate control: d0p (initial P frame virtual buffer fullness) */
0         /* rate control: d0b (initial B frame virtual buffer fullness) */
2 2 11 11 /* P:  forw_hor_f_code forw_vert_f_code search_width/height */
1 1 3  3  /* B1: forw_hor_f_code forw_vert_f_code search_width/height */
1 1 7  7  /* B1: back_hor_f_code back_vert_f_code search_width/height */
1 1 7  7  /* B2: forw_hor_f_code forw_vert_f_code search_width/height */
1 1 3  3  /* B2: back_hor_f_code back_vert_f_code search_width/height */
"""

def textlist(i):
    return [ ]

# Where will I keep all my temporary files? On Mandriva, /tmp is small
# but $HOME/tmp is large.
mpeg_dir = '/home/wware/tmp/mpeg'

def remove_old_yuvs():
    # you don't always want to do this
    do("rm -rf " + mpeg_dir + "/yuvs")
    do("mkdir -p " + mpeg_dir + "/yuvs")

class MpegSequence:

    def __init__(self):
        self.frame = 0
        self.width = mpeg_width
        self.height = mpeg_height
        self.size = (self.width, self.height)

    def __len__(self):
        return self.frame

    def yuv_format(self):
        # Leave off the ".yuv" so we can use it for the
        # mpeg2encode parameter file.
        return mpeg_dir + '/yuvs/foo.%06d'

    def yuv_name(self, i=None):
        if i is None:
            i = self.frame
        return (self.yuv_format() % i) + '.yuv'

    # By default, each title page stays up for five seconds
    def titleSequence(self, titlefile, frames=150):
        assert os.path.exists(titlefile)
        if framelimit is not None: frames = min(frames, framelimit)
        first_yuv = self.yuv_name()
        if border is not None:
            w, h = self.width - 2 * border[0], self.height - 2 * border[1]
            borderoption = ' -bordercolor black -border %dx%d' % border
        else:
            w, h = self.width, self.height
            borderoption = ''
        do('convert %s -geometry %dx%d! %s %s' %
           (titlefile, w, h, borderoption, first_yuv))
        self.frame += 1
        for i in range(1, frames):
            import shutil
            shutil.copy(first_yuv, self.yuv_name())
            self.frame += 1

    def previouslyComputed(self, fmt, frames, begin=0):
        assert os.path.exists(titlefile)
        if framelimit is not None: frames = min(frames, framelimit)
        for i in range(frames):
            import shutil
            src = fmt % (i + begin)
            shutil.copy(src, self.yuv_name())
            self.frame += 1

    def motionBlurSequence(self, povfmt, frames,
                           ratio, avg, begin=0):
        # avg is how many subframes are averaged to produce each frame
        # ratio is the ratio of subframes to frames
        if framelimit is not None: frames = min(frames, framelimit)
        pq = PovrayJobQueue()
        yuvs = [ ]
        srcdir, povfmt = os.path.split(povfmt)

        for i in range(frames):
            yuv = self.yuv_name()
            yuvs.append(yuv)
            dstdir, yuv = os.path.split(yuv)
            ywidth, yheight = mpeg_width, mpeg_height
            if border is not None:
                ywidth -= 2 * border[0]
                yheight -= 2 * border[1]
            job = PovrayJob(srcdir, dstdir, povfmt,
                            begin + i * ratio,
                            begin + i * ratio + avg,
                            yuv,
                            povray_width, povray_height,
                            ywidth, yheight, textlist(i))
            pq.append(job)
            self.frame += 1
        pq.start()
        pq.wait()

    def encode(self):
        parfil = mpeg_dir + "/foo.par"
        outf = open(parfil, "w")
        outf.write(params % {'sourcefileformat': self.yuv_format(),
                             'frames': len(self),
                             'height': self.height,
                             'width': self.width,
                             'bitrate': bitrate})
        outf.close()
        # encoding is an inexpensive operation, do it even if not for real
        do('mpeg2encode %s/foo.par %s/foo.mpeg' % (mpeg_dir, mpeg_dir))
        do('rm -f %s/foo.mp4' % mpeg_dir)
        do('ffmpeg -i %s/foo.mpeg -sameq %s/foo.mp4' % (mpeg_dir, mpeg_dir))

"""
Here is an example usage of this stuff.

import os, sys, animate, string

animate.worker_list = [
    ('localhost', '/tmp/mpeg'),
    ('server', '/tmp/mpeg'),
    ('laptop', '/tmp/mpeg'),
    ('mac', '/Users/wware/tmp')
    ]

for arg in sys.argv[1:]:
    if arg == 'debug':
        animate.DEBUG = True
    elif arg == 'ugly':
        animate.povray_pretty = False
    elif arg.startswith('framelimit='):
        animate.framelimit = string.atoi(arg[11:])

h = 438
w = 584
animate.set_resolution(w, h)
animate.border = (w/10, h/10)

#################################

N = 1   # nominally 1, test with 4, 5, or 9

animate.remove_old_yuvs()

m = animate.MpegSequence()
m.titleSequence('title1.gif', 150 / N)

# Each frame is 5 femtoseconds, each subframe is 0.5 fs
def textlist(i):
    nsecs = i * 5.0e-6
    return [
        '%.4f nanoseconds' % nsecs,
        '%.4f rotations' % (nsecs / 0.2),
        ]
animate.textlist = textlist
m.titleSequence('title2.gif', 150 / N)
m.motionBlurSequence(os.path.join(animate.mpeg_dir, 'fastpov/fast.%06d.pov'),
                     450 / N, 10 * N, 10 / N)


# Each frame is 20 femtoseconds, each subframe is 2 fs
def textlist(i):
    nsecs = i * 20.0e-6
    return [
        '%.3f nanoseconds' % nsecs,
        '%.3f rotations' % (nsecs / 0.2),
        ]
animate.textlist = textlist
m.titleSequence('title3.gif', 150 / N)
m.motionBlurSequence(os.path.join(animate.mpeg_dir, 'medpov/med.%06d.pov'),
                     450 / N, 10 * N, 10 / N)


# Each frame is 200 femtoseconds, each subframe is 20 fs
def textlist(i):
    nsecs = i * 200.0e-6
    return [
        '%.2f nanoseconds' % nsecs,
        '%.2f rotations' % (nsecs / 0.2),
        ]
animate.textlist = textlist
m.titleSequence('title4.gif', 150 / N)
m.motionBlurSequence(os.path.join(animate.mpeg_dir, 'slowpov/slow.%06d.pov'),
                     450 / N, 10 * N, 10 / N)
m.encode()
"""

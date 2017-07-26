# Denis Gorodetskiy
# linkedin.com/in/gorodetskiy
import array
import sys
import os
import math
import re

def frame_diff(frame1_data, frame2_data, begin_pos, end_pos, w, h):

    luma_size = w * h
    chroma_size = w * h/4
    frame_size = w * h * 3/2

    print "data size: %d, w*h=%d, w*h*3/2=%d" % (end_pos-begin_pos,
            luma_size, frame_size)
    print "evaluating mse.."

    def psnr(mse):
        log10 = math.log10
        return 10.0*log10(float(256*256)/float(mse))

    def mean(seq):
        if len(seq) == 0: return 0.0
        else: return sum(seq)/float(len(seq))

    def sum_square_err(data1, data2, beg, end):
        return sum( (a-b)*(a-b) for a,b in zip(data1[beg:end],data2[beg:end]))


    y = begin_pos
    u = y + luma_size
    v = u + chroma_size

    begin   = [y,u,v,y]
    end     = [u,v,end_pos,end_pos]
    size    = [luma_size, chroma_size, chroma_size, frame_size]

    colorspace_mse = [sum_square_err(frame1_data,frame2_data,
        begin[i], end[i])/float(size[i]) for i in range(4)]

    colorspace_psnr = [psnr(m) for m in colorspace_mse]
    return colorspace_mse, colorspace_psnr, colorspace_psnr[-1]

def width_height_from_str(s):
    m = re.search(".*[_-](\d+)x(\d+).*", s)
    if not m:
        raise RuntimeError()

    w = int(m.group(1))
    h = int(m.group(2))
    return w,h

def usage(me):
    print "usage: %s filename1.yuv filename2.yuv [width height]" % me
    print "\tif you don't want to specify width height explicitly,"
    print "\tscript will try to extract width, height from filenames,"
    print "\tfilename_1024x768.yuv or filename-1024x768.yuv yield (width,height)=(1024,768)"

def main(argv):
    if len(argv) < 3:
        usage(argv[0])


    filename1 = argv[1]
    filename2 = argv[2]

    if filename1 == filename2:
        print "warning! do you really mean to compare the file with itself?"

    data1 = array.array('B')
    data2 = array.array('B')

    file1_size = os.path.getsize(filename1)
    file2_size = os.path.getsize(filename2)

    minsize = min(file1_size, file2_size)

    if file1_size != file2_size:
        print "warning, file sizes do not match! comparing min size %d bytes" % minsize

    if len(argv) >= 5:
        w = int(argv[3])
        h = int(argv[4])
    else:
        try:
            w,h = width_height_from_str(filename1)
        except RuntimeError:
            try:
                w,h = width_height_from_str(filename2)
            except RuntimeError:
                print "failed to parse width,height from filename"
                usage(argv[0])
                return


    assert w*h*3/2 <= minsize
    data_end = w*h * 3 /2

    data1.fromfile(open(filename1,"rb"),minsize)
    data2.fromfile(open(filename2,"rb"),minsize)

    colorplane_mse, colorplane_psnr, frame_psnr = frame_diff(data1, data2,
        0, data_end, w, h)
    print "planes: Y, U, V, Whole frame"
    print 'colorplane mse: ', colorplane_mse
    print 'colorplane psnr: ', colorplane_psnr
    print 'frame psnr: ', frame_psnr

if __name__ == '__main__':
    main(sys.argv)

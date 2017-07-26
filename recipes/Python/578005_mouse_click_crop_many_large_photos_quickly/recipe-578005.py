import os
import pygame, sys
from pygame.locals import K_a, K_s,K_w,K_d,K_LEFTBRACKET,K_RIGHTBRACKET, K_RIGHT, K_LEFT, QUIT

from PIL import Image
pygame.init()


'''

main() sets these (perhaps differently), so make changes down there.
If you cut/copy this code somewhere you need these variables globally,
or make it a class and make these attributes.

'''

resolution = 300    #the resolution (in dpi) the resulting cropped images should have.

infile_folder = '.'             #path to folder images to process are in.  '.' is the folder this script is in
infile_prefix = "album80-86_"   #prefix common to all the images you'd like to access

start_page = 1                  #which page to start on.  0 is the first page.

outfile_folder= "./cropped"
outfile_prefix = "photo80-86_"
outfile_extension = "jpg"      #must be three character extension with no period. Why? Because I am lazy.  So no "jpeg", okay?


BG_COLOR = (0,0,0)

def displayRect(screen, px, topleft, prior,pos,scale):
    # ensure that the rect always has positive width, height

    if topleft == None:
        #func was called without a topleft, which means clear the previous rectangle
        screen.fill(BG_COLOR)
        rect = px.get_rect()
        px = pygame.transform.scale(px,[int(rect.width/scale), int(rect.height/scale)])
        screen.blit(px, (rect[0]-pos[0],rect[1]-pos[1]))
        pygame.display.flip()

        return None

    #or, the usual situation, topleft is defined, so blit over the old rect and blit in the new.
    topleft = [(val/scale-pos[i]) for i,val in enumerate(topleft)]
    x, y = topleft
    bottomright = pygame.mouse.get_pos()
    width =  bottomright[0] - topleft[0]
    height = bottomright[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
 
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    rect = px.get_rect()
    px = pygame.transform.scale(px,[int(rect.width/scale), int(rect.height/scale)])
    screen.blit(px, (rect[0]-pos[0],rect[1]-pos[1]))
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)

def setup(px):
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def move(pos,scale,px,screen):
    x,y = pos
    #print pos,x
    rect = px.get_rect()
    screen.fill(BG_COLOR)
    px = pygame.transform.scale(px,[int(rect.width/scale), int(rect.height/scale)])
    screen.blit(px, (rect[0]-x,rect[1]-y))
    pygame.display.flip()
    #px.rect.topleft = pr.rect.topleft[0] - x, 

def mainLoop():
    topleft = bottomright = prior = None
    n=0
    scale = 1
    pos = [0,0]

    #create list of files matching prefix in folder, and sort it
    # input_loc = first file  #input_loc = 'album86-92_003.jpg'
    infiles = []
    len_prefix = len(infile_prefix)
    for fname in os.listdir(infile_folder):
        if fname[:len_prefix] == infile_prefix:
            if fname[-3:] in ['jpg','png']:
                infiles.append(fname)
    infiles.sort()

    file_idx = start_page
    try:
        infile = infiles[file_idx]
    except IndexError:
        print "the start page you requested is beyond the scope of the files loaded.\nYou have been taken to the last page instead."
        file_idx = len(infiles)-1
        infile = infiles[file_idx]

    #get files begining with output prefix, grab suffixes and sort.
    #but, if folder does not exist or is empty, just start at 0 
    outfiles = []
    len_prefix = len(outfile_prefix)

    try:
        for fname in os.listdir(outfile_folder):
            if fname[:len_prefix] == outfile_prefix:
                outfiles.append(fname)
    except OSError:
        os.makedirs(outfile_folder)
        out_idx = 0

    else:
        outfiles.sort()
        try:
            out_idx = int(outfiles[-1][len_prefix:-4])+1
        except ValueError:
            print "Egad! Not all files with the output prefix specified end with a number followed by a three character extension\nMaybe start a new output folder?"
            print "...Quitting"
            return 0
        except IndexError:
            #folder exisits but is empty
            out_idx = 0

    input_loc = os.path.join(infile_folder,infile)
    screen, px = setup(px = pygame.image.load(input_loc))        
    
    outfilename = outfile_prefix+str(out_idx).zfill(3)+'.'+outfile_extension
    output_loc = os.path.join(outfile_folder,outfilename)
    while n!=1:
        for event in pygame.event.get():

            if event.type == QUIT: 
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = [(val+pos[i])*scale for i,val in enumerate(event.pos)]
                    #print "tr: ",topleft
                else:
                    bottomright = [(val+pos[i])*scale for i,val in enumerate(event.pos)]
                    #print "br: ",bottomright
                    

            if event.type == pygame.KEYDOWN and event.key == K_a:
                pos = [pos[0]-200,pos[1]]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_d:
                pos = [pos[0]+200,pos[1]]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_w:
                pos = [pos[0],pos[1]-200]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_s:
                pos = [pos[0],pos[1]+200]
                move(pos,scale,px,screen)


            if event.type == pygame.KEYDOWN and event.key == K_RIGHTBRACKET:
                scale = scale/1.25
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_LEFTBRACKET:
                scale = scale*1.25
                move(pos,scale,px,screen)
            
            if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                file_idx += 1
                try:
                    infile = infiles[file_idx]
                    #print "file_idx: ",file_idx
                except IndexError:
                    file_idx -= 1
                    print "End of album"
                    #raise
                else:
                    input_loc = os.path.join(infile_folder,infile)
                    px = pygame.image.load(input_loc)
                    pos = [0,0]
                    topleft = bottomright = prior = None
                    prior = displayRect(screen, px, topleft, prior,pos,scale)

            if event.type == pygame.KEYDOWN and event.key == K_LEFT:
                if file_idx == 0:
                    print "This is the begining of the album, cannot go back a page."
                else:
                    #print "file_idx",file_idx
                    file_idx -= 1
                    infile = infiles[file_idx]
                    input_loc = os.path.join(infile_folder,infile)
                    px = pygame.image.load(input_loc)
                    pos = [0,0]
                    topleft = bottomright = prior = None
                    prior = displayRect(screen, px, topleft, prior,pos,scale)


                
        if topleft:
            #first corner has been selected
            prior = displayRect(screen, px, topleft, prior,pos,scale)
            if bottomright:
                #selection has been made!
                left, upper, right, lower = ( topleft + bottomright )
                # ensure output rect always has positive width, height
                if right < left:
                    left, right = right, left
                if lower < upper:
                    lower, upper = upper, lower
                im = Image.open(input_loc)
                im = im.crop(( int(left), int(upper), int(right), int(lower)))
                dpi = resolution
                im.save(output_loc, dpi = (dpi,dpi))
                out_idx += 1
                outfilename = outfile_prefix+str(out_idx).zfill(3)+'.'+outfile_extension
                output_loc = os.path.join(outfile_folder,outfilename)
                topleft = bottomright = prior = None
                prior = displayRect(screen, px, topleft, prior,pos,scale)
                print "saved"
                
    return

if __name__ == "__main__":
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    print'''
Hello! 

This program exists to speed up cropping out many sections from larger images 
while also changing the resolution of the cropped images.

The Zudell family photo album was scanned at 600 dpi resolution.
The default resolution for cropped images is 300 dpi.
    '''
    resolution = raw_input('enter new integer resolution, or nothing for default: ')
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    try: resolution = int(resolution)
    except:
        print '\nNo new resolution specified, using 300 dpi'
        resolution = int(300)
    dirs = []
    for f in os.listdir('.'):
        if os.path.isdir(f):
             dirs.append(f)

    print '''\n\n\n\n
now, enter the name of the directory you want to work on. here is a list of sub 
directories within this current directory:\n'''
    if dirs:
        for dir in dirs: print dir
    else:
        print "oops, there are no sub-directories here"

    print "\n\nenter nothing or nonsense to use the current directory"
    path = raw_input("enter directory to use: ")
    infile_folder = path.strip()
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    if os.path.isdir(infile_folder):
        pass
    elif os.path.isdir('./'+infile_folder):
        infile_folder = './'+infile_folder
    else:
        print "no valid directory entered, using current"
        infile_folder = '.'

    for f in os.listdir(infile_folder):
        print f
    if not os.listdir(infile_folder):
        print "oh... There aren't any files at all in here"
        d = raw_input("press enter to quit")
        pygame.display.quit()
 
    print '''\n\n
You may choose a filename prefix so that only some of the images in this dir 
are available for editing.  all files in this directory are listed above. \n'''

    infile_prefix = raw_input('input file prefix (or nothing to use all files): ')
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

    print '''\n\n
You may choose a prefix for output files also. they will go in the ./cropped folder.\n'''

    outfile_prefix = raw_input('output file prefix (or nothing for default): ')
    if not outfile_prefix: outfile_prefix = "image_"
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

    print '''
Use the left ard right arrows to change image. 

'[' and ']' zoom out and in, respectively.  

click and drag a box to crop. 

too move around:

   w
  asd


And come back to this screen to see unnecessary messages.
    '''
    raw_input('\npress enter to begin')
    mainLoop()

    pygame.display.quit()

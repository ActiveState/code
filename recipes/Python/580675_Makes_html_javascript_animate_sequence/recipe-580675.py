#!/usr/bin/env python
from __future__ import print_function
'''makes html with javascript to animate a sequence of images'''

__author__ = 'Brian Fiedler'
# This module can be imported to access the function makeanim. 
# Or it can be run independently as a script from the command line.
# Suppose the command "ls mydir/*.png" gives the list of files to be animated.
#
# python janim.py myimages/*.png > myanimator.html
# 
# python janim.py -i listofimageurls.txt -o myanimator.html -t "rainfall animation"
#
# myanimator.html wll be viewable in a browser, but you may want to add more html to it.
# Or you can embed myanimator.html within another web page, with html code like:
# <object type="text/html" data="myanimator.html" width="930" height="680" >error message here</object>
# (The width and height in the above example is for 900x600 images, with controls at the bottom.)
#
# Alternative to using janim.py from the command line:
# files = glob.glob("pngs/*.png")
# janim.makeanim(files,outfile="myanimator.html",sortOrder=True,ctlOnSide=True,titlestring="rainfall animation")
#
# For a similar animator, but with more features, see http://www.ssec.wisc.edu/hanis/

def makeanim(files=[],ctlOnSide=False,revOrder=False,sortOrder=False,
             titlestring="animation",fileOfFileNames="",outfile=""):
    # files is a list of paths to the image files

    # possible to append more paths to files:
    if fileOfFileNames: # file with image file names, either on new lines or separated by white space
        urls = open(fileOfFileNames).read().split()
        files += [x.strip() for x in urls if x.strip()]

    if sortOrder: files.sort()
    if revOrder: files.reverse()

    nim=len(files) #number of image files

    #### some large template strings follow:

    top = """<html>
    <title>%s</title>
    <script>
    // semi-colons are optional in javascript, and are often not included in this code!  
    var maxFrameNum=%d 
    var delay = 1000 // time between frames in milliseconds
    var frameNum = 0    // The frame counter: keeps track of current frame
    var timeout_id = null  // Allows us to stop the animation with clearTimeout( )
    var aniFrames = new Array()
    """
    script = """

    document.onkeydown = myKeyDownHandler;

    function myKeyDownHandler(e){
        if (timeout_id!=null) {killAnimate()} 
    //  if (e.which==13) {Animate()} // oddly, the enter key seems to be reserved for repeating the last click  
        if (e.which==39 || e.which==40) {incrementFrame()} // rightarrow
        if (e.which==37 || e.which==38) {decrementFrame()} // leftarrow
    //    alert(e.which+" was pressed")
    }

    // This function performs the animation. 
    function xanimate() {
        incrementFrame()
        timeout_id = setTimeout("xanimate()", delay )  // Display the next frame after delay millisecs
    }
    //A better way? http://creativejs.com/resources/requestanimationframe/ 
    function yanimate() {
        timeout_id = setTimeout( function() {
        requestAnimationFrame(yanimate);
        incrementFrame();
        }, delay );  // Display the next frame after delay millisecs
    }

    function slower() {
        delay=delay*1.5
        if (delay > 4000) delay = 4000
    }

    function faster() {
        delay=delay*2/3
        if (delay < 50 ) delay = 50
    }

    function incrementFrame(){
        frameNum++ 
        if (frameNum > maxFrameNum) { frameNum = 0  }
        showFrame()
    }

    function decrementFrame(){
        frameNum+=-1 
        if (frameNum < 0 ) { frameNum = maxFrameNum  }
        showFrame()
    }

    // Note that we refer to the onscreen image and text using the id imageWindow and textWindow,  defined by us.
    function showFrame(){
        var str = "" + frameNum
        var pad = "000"
        var frameNumPad = pad.substring(0, pad.length - str.length) + str    
        document.getElementById('textWindow').innerHTML = frameNumPad // Display frame number as text 
        document.imageWindow.src = aniFrames[frameNum].src // Display the current frame image
    }

    function killAnimate(){
    if (timeout_id) clearTimeout(timeout_id)
    timeout_id=null
    }
    </script>
    """


    form = """
    <form>  <!-- This form contains buttons to control the animation -->
        <input value="Slower" onclick="slower()" type="button">
        <input value="1 sec" onclick="delay=1000;" type="button">
        <input value="Faster" onclick="faster()" type="button">
        <input style="color: rgb(0, 0, 0); background-color: rgb(153, 255, 153);"
               value="Start" onclick="if (timeout_id == null) yanimate( );" type="button">
        <input value="Stop" onclick="killAnimate();" type="button">
        <input value="-1" onclick="killAnimate(); decrementFrame();" type="button">
        <input value="+1" onclick="killAnimate(); incrementFrame();" type="button">
        <input value="First" onclick="killAnimate(); frameNum=0; showFrame();" type="button">
        <input value="Last" onclick="killAnimate(); frameNum=maxFrameNum; showFrame();" type="button">
        &nbsp;&nbsp;<b id='textWindow'>000</b> 
    </form>
    """

    ### use the paths to images stored in files list to make javascript links to the images: 

    imagecode = """aniFrames[%d] = new Image();\naniFrames[%d].src = "%s";\n"""
    imagepaths = "" 
    for i in range(nim):
        imagepaths += imagecode % (i,i,files[i])

    # show the first image, before animation replaces it:
    firstimgtag = '<img name="imageWindow" src="%s" alt="your image should have been seen here!">' % files[0] 

    ### now put together the web page containing javascript and html for your animation:

    webpage = top % (titlestring,nim-1) 
    webpage += imagepaths
    webpage += script 
    webpage += "<body><center>\n"
    if ctlOnSide: #controls are on the left side of the image
        webpage += "<table><tr><td width=1>\n"
        webpage += form
        webpage += "</td><td>\n"
        webpage += firstimgtag
        webpage += "</td></tr></table>\n"
    else: #controls are below the image
        webpage += firstimgtag
        webpage += form 
    webpage += "</center></body></html>\n"
    if outfile: # write out the html file
        ouf = open(outfile,'w')
        ouf.write(webpage)
        ouf.close()
    else: # written the html file contents as a string
        return webpage


#### optionally process command line arguments for a call to makeanim
if __name__ == '__main__':
    import argparse 
    parser = argparse.ArgumentParser(description= "produces html with javascript for animation" )
    parser.add_argument("-s","--side", dest="ctlOnSide",action="store_true",help="put controls on side")
    parser.add_argument("--sort", dest="sortOrder",action="store_true",help="sorts the image order")
    parser.add_argument("--rev", dest="revOrder",action="store_true",help="reverses the image order")
    parser.add_argument("-t","--title", dest="titlestring",type=str,
                     help="title string in quotes",default="javascript animation")
    parser.add_argument("-i","--fof", dest="fileOfFileNames",type=str,help="name of file containing file urls",default="")
    parser.add_argument("-o","--outfile", dest="outfile",type=str,help="name of html output file",default="")
    parser.add_argument("files",help="paths to image files",nargs='*')
    args = parser.parse_args()

    if len(args.files) == 0:
        parser.print_help()
        
    else: 
        webpage = makeanim(args.files,ctlOnSide=args.ctlOnSide,revOrder=args.revOrder,sortOrder=args.sortOrder,
             titlestring=args.titlestring, fileOfFileNames=args.fileOfFileNames,outfile=args.outfile)
        if not args.outfile:
            print(webpage)

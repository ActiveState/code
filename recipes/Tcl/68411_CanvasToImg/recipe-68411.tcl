# Draw filled rectangle and some text into canvas at position (x,y).
proc drawInfo { x y color } {
    set size 10
    set tx [expr $x + $size * 2]
    .t.c create rectangle $x $y [expr $x + $size] [expr $y + $size] -fill $color
    .t.c create text $tx $y -anchor nw -fill $color -text "$color box"
}

proc drawTestCanvas { imgVersion} {
    if { [catch {toplevel .t -visual truecolor}] } {
        toplevel .t
    }
    wm title .t "Canvas window"
    wm geometry .t "+0+0"

    canvas .t.c -bg gray -width 300 -height 220
    pack .t.c

    puts "Drawing text and rectangles into canvas .."
    .t.c create rectangle 1 1 299 219 -outline black
    .t.c create rectangle 3 3 297 217 -outline green -width 2

    drawInfo 140  10 black
    drawInfo 140  30 white
    drawInfo 140  50 red
    drawInfo 140  70 green
    drawInfo 140  90 blue
    drawInfo 140 110 cyan
    drawInfo 140 130 magenta
    drawInfo 140 150 yellow

    .t.c create text 160 170 -anchor nw -fill black -text "Created with:"
    .t.c create text 160 190 -anchor nw -fill black -text        "Tcl [info patchlevel] and Img $imgVersion"
    update
}

proc canvas2Photo { canvId } {
    # The following line grabs the contents of the canvas canvId into photo image ph.
    set retVal [catch {image create photo -format window -data $canvId} ph]
    if { $retVal != 0 } {
       puts "\n\tFATAL ERROR: Cannot create photo from canvas window"
       exit 1
    }
    return $ph
}

set retVal [catch {package require Img} version]
if { $retVal } {
    error "Trying to load package Img: $version"
}

if { $tcl_platform(platform) == "windows" } {
    catch { console show }
}

wm geometry . "+320+0"
drawTestCanvas $version
set ph [canvas2Photo .t.c]
puts "Writing canvas as JPG image: test.jpg"
$ph write test.jpg -format JPEG
puts "Writing canvas as GIF image: test.gif"
$ph write test.gif -format GIF
puts "Writing canvas as PNG image: test.png"
$ph write test.png -format PNG

button .b -text "Quit" -command exit
pack .b
update

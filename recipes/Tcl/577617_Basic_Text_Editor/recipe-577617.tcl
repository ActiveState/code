#!/usr/bin/wish
#
# text editor with copy,cut and paste functions.
# licence: G.P.L

frame .menubar -borderwidth 0
      pack .menubar -side top -fill x
      
      menubutton .menubar.file -text File \
           -underline 0 -menu .menubar.file.m
      menubutton .menubar.edit -text Edit \
            -underline 0 -menu .menubar.edit.m
      menubutton .menubar.help -text ~ \
           -menu .menubar.help.m
      
      menu .menubar.file.m -tearoff 0
      menu .menubar.edit.m -tearoff 0
      menu .menubar.help.m -tearoff 0
           pack .menubar.file .menubar.edit -side left
           pack .menubar.help -side right
           
      .menubar.file.m add command -label "Exit" \
           -underline 1 -command exit
      .menubar.edit.m add command -label "Cut" \
            -underline 2 \
            -command {event generate [focus] <<Cut>>}
      .menubar.edit.m add command -label "Copy" \
            -underline 0 \
            -command {event generate [focus] <<Copy>>}
      .menubar.edit.m add command -label "Paste" \
            -command {event generate [focus] <<Paste>>}
      .menubar.help.m add command -label "About"  \
            -command appHelpAbout 
# Text Box      
      text .t -wrap word
      pack .t -side top -fill both -expand y

proc appHelpAbout { } {
     global version licence

     tk_messageBox -message "\n\
     Text editor with copy,cut and paste functions.\n\
     Author: ME."
     
}
#-----------------------------
wm title .  "Editor v0.01"
wm minsize . 255 350

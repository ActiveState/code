#!/bin/sh
# May need to change if not wish8.4 \
exec wish8.4 "$0" "$@"
package require http

# may need to uncomment next line if using a proxy server
#http::config -proxyhost proxy -proxyport 80

proc translate_query {query lang} {
    set url http://babelfish.altavista.com/babelfish/tr?doit=done&urltext=[string map {" " +} $query]&lp=$lang
    #puts "url = $url"
    set token [http::geturl $url]
    set data [http::data $token]
    http::cleanup $token
    #puts $token
    #puts $data
    set results ""
    #regexp {\n[0-9-]+ of ([0-9]+)} $data -> results
    regexp {input type=hidden  name="q" value=[^>]+>} $data  results
    regsub {^(input type=hidden  name="q" value=")} $results {} results
    regsub {(">)$} $results {} results
    
    set results
}

proc go {w} {
    global query lang speak_choice original_output
    
    if {$original_output == "Yes"} {
        $w insert end "$query\n"
    }
    set answer [translate_query $query $lang]
    $w insert end "$answer \n"
    $w see end
    update idletasks
    
    # for the ViaVoice TTS speech synthesis system
    # adjust for the path to cmdlinespeak on your system
    if {$speak_choice == "TTS"} {
        exec /usr/lib/ViaVoiceOutloud/samples/cmdlinespeak/cmdlinespeak "$answer"
    }
    
    # for the Festival speech synthesis system
    # adjust path to the festival program on your system
    if {$speak_choice == "Festival"} {
        set f [open speech_test w]
        puts $f "$answer"
        close $f
        exec /hdc1/festival/bin/festival  --tts speech_test
    }
}

set lang "en_es"
frame .frame
menubutton .frame.lang -text "English -> Spanish" -relief raised -indicatoron \
        true -pady 0 -menu .frame.lang.menu
menu .frame.lang.menu
.frame.lang.menu add radiobutton -label "English -> Spanish" -variable lang \
        -value "en_es" -command {.frame.lang configure -text "English -> Spanish"}
.frame.lang.menu add radiobutton -label "English to Portuguese" -variable lang \
        -value "en_pt" -command {.frame.lang configure -text "English -> Portuguese"}
.frame.lang.menu add radiobutton -label "Spanish -> English" -variable lang \
        -value "es_en" -command {.frame.lang configure -text "Spanish -> English"}
.frame.lang.menu add radiobutton -label "Portuguese -> English" -variable lang \
        -value "pt_en" -command {.frame.lang configure -text "Portuguese -> English"}


set original_output No
.frame.lang.menu add separator
.frame.lang.menu add command  -label "Output Original Text?"
.frame.lang.menu add radiobutton -label "No " -variable original_output -value No
.frame.lang.menu add radiobutton -label "Yes" -variable original_output -value Yes

set speak_choice "None"
menubutton .frame.speak -text "Text -> Speech?" -relief raised -pady 0 -indicatoron true -menu .frame.speak.menu
menu .frame.speak.menu
.frame.speak.menu add radiobutton -label "None        " -variable speak_choice -value None
.frame.speak.menu add radiobutton -label "Festival    " -variable speak_choice -value "Festival"
.frame.speak.menu add radiobutton -label "ViaVoice TTS" -variable speak_choice -value "TTS"


button .frame.print -text "Print" -pady 0 -command {
    set print_data [.frame2.t get 1.0 end]
    set f [open ./print_data.txt w]
    puts $f "\n\n\n\n$print_data"
    close $f
    exec lpr ./print_data.txt
}


entry .e -textvar query -bg white
bind .e <Return> {
    go .frame2.t
    lappend history_list $query
    set history_index [expr [llength $history_list] -1]
}
bind .e <Control-k> {set query ""}
bind .e <Key-Up> {
    if {$history_index >= 1} {
        incr history_index -1
        set query [lindex $history_list $history_index]
    }
}
bind .e <Key-Down> {
    if {$history_index <= "[expr [llength $history_list] - 1]" } {
        incr history_index
        set query [lindex $history_list $history_index]
    }
}

frame .frame2
text .frame2.t -bg white -yscrollcommand {.frame2.scroll set}
scrollbar  .frame2.scroll -command {.frame2.t yview}

pack .frame -fill x -expand 1
pack .frame.lang .frame.speak   .frame.print -side left -fill x -expand 1
pack  .e  -fill x -expand 1
pack .frame2 -fill x -expand 1
pack .frame2.t -side left -fill x -expand 1
pack .frame2.scroll -side left -fill y -expand 1

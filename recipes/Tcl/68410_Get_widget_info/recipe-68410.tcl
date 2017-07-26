toplevel .find

grid [text .find.info -yscrollcommand {.find.scr set} -width 40] -row 0 -column 0 -sticky ns
grid rowconfigure .find 0 -weight 1
grid [scrollbar .find.scr -command {.find.info yview}] -row 0 -column 1 -sticky ns
grid [button .find.find -text "find"] -row 1 -column 0 -columnspan 2
bind .find.find <Button> {
   grab -global .find.find
}
wm geometry .find 290x345

bind .find.find <ButtonRelease> {
   grab release [grab current]
   set what [winfo containing %X %Y]
   if {$what != ""} {
      .find.info delete 1.0 end
      .find.info insert end "$what\n"
      foreach a [$what config] {
         .find.info insert end "\t[lindex $a 0] [$what cget [lindex $a 0]]\n"
      }
   } else {
      .find.info delete 1.0 end
      .find.info insert 1.0 NULL
   }
   update
}

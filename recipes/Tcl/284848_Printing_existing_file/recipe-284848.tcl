 proc WindowsPrintFile {fileName} {
     package require csv

     ##
     ## Get the print command for this type
     ##
     set ext [file extension $fileName]
     set app [registry get [format {HKEY_CLASSES_ROOT\%s} $ext] {}]
     set app [format {HKEY_CLASSES_ROOT\%s\shell\print\command} $app]
     set cmdList {}
     foreach cmdElement [::csv::split [registry get $app {}] { }] {
          lappend cmdList [string map {%1 %1$s} $cmdElement]
     }

     ##
     ## Print the file -- catch is needed because return codes are not Unix ones!!!
     ##
     set cmd [format $cmdList $fileName]
     catch {eval exec $cmd} msg

     ##
     ## All done, so return
     ##
     return;

 }

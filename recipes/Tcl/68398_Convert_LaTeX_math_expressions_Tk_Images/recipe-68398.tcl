namespace eval MathToImg {
   image create photo MathToImgHelperImage

   set tmpdir "/tmp"; # configure for platforms!

   # What LaTeX size should we format at?  This looks good on my workstation
   set latexSize huge; # No backslash!

   # Commands
   set latexCommand "latex '\\nonstopmode\\input{%s.tex}'"
   set dvipsCommand "dvips -E -q -o %s.eps %s.dvi"
   set gsCommand "gs -q -dNOPAUSE -dSAFER -sDEVICE=ppmraw           -sOutputFile=%s.ppm %s.eps"

   # Regular expression for finding bounding box
   set BBre {^%%BoundingBox: ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) *$}

   proc external cmd {
      exec sh -c $cmd 2>@stderr </dev/null
   }

   proc mathToImg {latex {packages {}}} {
      # Keep ourselves current-dir neutral
      set cwd [pwd]
      cd $::MathToImg::tmpdir

      # Put a wrapper round the supplied LaTeX source
      set latexSource "\\documentclass{article}\n"
      if {[llength $packages]} {
         # Add needed packages, converting Tcl list to comma-ed list
         append latexSource "\\usepackage{" [join $packages ,] "}"
      }
      append latexSource "\\begin{document} \\$::MathToImg::latexSize              \\pagestyle{empty} \\begin{displaymath}\n% USER CODE START\n"
      append latexSource $latex "\n% USER CODE END\n"
      append latexSource "\\end{displaymath} \\end{document}\n"

      set basename [file tail [file rootname $::argv0]]_mathToImg_[pid]

      set f [open $basename.tex w]
      puts -nonewline $f $latexSource
      close $f

      # LaTeX -> DVI
      external [format $::MathToImg::latexCommand $basename]
      # DVI -> EPS
      external [format $::MathToImg::dvipsCommand $basename $basename]

      # Grok out the size, which we need later...
      set f [open $basename.eps r]
      while {![eof $f]} {
         gets $f line
         if {[regexp $::MathToImg::BBre $line ? x1 y1 x2 y2]} {
            break
         }
      }
      close $f

      # EPS -> PPM
      external [format $::MathToImg::gsCommand $basename $basename]

      # Make the image - we can't go direct as we need the size of
      # the image to handle the cropping correctly.
      set img [image create photo               -height [expr {$y2-$y1}]               -width  [expr {$x2-$x1}]]
      # PS has (0,0) in bottom left, Tk in top left
      MathToImgHelperImage read $basename.ppm
      set h [image height MathToImgHelperImage]
      $img copy MathToImgHelperImage               -from $x1 [expr {$h-$y1}] $x2 [expr {$h-$y2}]
      MathToImgHelperImage blank; # Ditch the data

      # Try to clean up after ourselves!
      catch {eval file delete [glob $basename.*]}

      cd $cwd
      return $img
   }

   namespace export mathToImg
}
namespace import MathToImg::*

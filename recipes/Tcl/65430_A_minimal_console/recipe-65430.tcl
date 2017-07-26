entry .e -textvar cmd
bind .e <;Key-Return>; {go %W}
text .t -wrap word
proc go {w} {
    global cmd
    .t insert end "% $cmd\n"
    catch {eval $cmd} res
    .t insert end $res\n
    set cmd ""
}
eval pack [winfo children .] -fill both -expand 1
focus .e

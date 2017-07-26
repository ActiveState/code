#! /bin/bash
#  Creator: Kevin L. Sitze
#  Created: March 24, 2010
#  Summary: Perform a command in parallel against multiple arguments.

function syntax()
{
    cat <<EOF 2>&1
usage: $(basename "$0") [-j jobs] command cmd_args...

Run a command with varying arguments in parallel.  Arguments for
each dispatched command are expected to come from stdin.  Without
any other modifiers exactly one argument per dispatched command is
taken from stdin and appended to the end of the argument list
indicated on the initial command line.

For example: issuing the command

    $(basename "$0") mv --target-directory=target --verbose < filelist

where filelist is a list of files one per line would cause all the
files to be transferred using individual mv commands as if the user
had typed the shell command

    while read filename ; do
	mv --target-directory=target --verbose "\$filename" &
    done < filelist

The operational difference between the above while statement and a
command issued via this program is the job control aspect of ensuring
that only a limited number of parallel tasks are actually active at
any particular moment.

Multiple command arguments may be provided per process using the
argument positional modifiers "\$1", "\$2", ...	 A positional modifier
indicates the relative offset of a line from stdin to insert into the
dispatched command.  When positional modifiers are used, the largest
modifier value indicates the number of lines to read from stdin for
each dispatched command (though the -n option can change this value).
Only explicitly indicated modifiers will actually be substituted.

The above mv command could thus be rewritten as follows:

    $(basename "$0") mv --verbose '\$1' target < filelist

The mv command below will take the first and third lines out of every
four lines on STDIN and move the file named in the first argument to
the fourth argument.  The second and fourth lines are discarded.

    $(basename "$0") -n 4 mv --verbose '\$1' '\$3' < filelist

Be sure to escape the dollar sign ('\$') from the shell.

-h	    This help text.
-j JOBS	    Total number of parallel jobs that may be issued at once.
-n ARGC	    Number of lines to read from STDIN for each command.
-v	    Verbose mode: prints a description of each job issued.
-o TARGET   Send output of subprocesses to the indicated file.
	    Output is appended to TARGET only upon completion
	    of the subprocess.

EOF
    exit 1
}

argc=1
jobs=2
verbose=false
while getopts hj:n:o:v ARG
do
    case $ARG in
    h)	syntax
	;;
    j)	jobs=$OPTARG
	;;
    n)	argc=$OPTARG
	;;
    o)	outfile=$OPTARG
	;;
    v)	verbose=true
	;;
    \?) exit 2
	;;
    esac
done
shift `expr $OPTIND - 1`

if [ $# -lt 1 ]
then
    echo "Error: a command to execute is required"
    exit 1
fi

declare -a command		# contains the command template
declare -a source		# index of line to transfer
declare -a target		# index of command argument
for param in "$@"
do
    if [[ "$param" =~ \$[[:digit:]]+$ ]]
    then
	(( argc < ${param#$} )) && argc=${param#$}
	source[${#source[*]}]=$(( ${param#$} - 1 ))
	target[${#target[*]}]=${#command[*]}
    fi
    command[${#command[*]}]="$param"
done

if [[ ${#source[*]} -eq 0 ]]
then
    source[0]=0
    target[0]=${#command[*]}
fi


declare -a argv

####
#  Read $argc lines from stdin
function readlines()
{
    local i
    for (( i = 0; i < argc; ++i ))
    do
	read argv[$i] || return 1
    done
    return 0
}

####
#  Generate the next command
function generator()
{
    local i
    local n=${#source[*]}
    for (( i = 0; i < n; ++i ))
    do
	command[${target[$i]}]="${argv[${source[$i]}]}"
    done
}

function append_output()
{
    if [[ x"${outfile}" != x"" ]]
    then
	if [[ -s "$2" ]]
	then
	    $verbose && echo "$1"
	    cat "$2"
	fi >> "${outfile}"
	rm -f "$2"
    fi
}

running=0
function reaper()
{
    if read -u 3 cpid
    then
        wait $cpid	# harvest the child
        (( --running ))	# and schedule next
        append_output "command line" "${fifoPath}"/cmd_"${cpid}"
        append_output "standard err" "${fifoPath}"/cmd_"${cpid}"_err
        append_output "standard out" "${fifoPath}"/cmd_"${cpid}"_out
    fi
}

####
#  Use a FIFO to determine when to harvest a subprocess.  Each
#  subprocess is evaluated such that a child PID is printed to
#  a FIFO in order to signal subprocess completion.  A
#  replacement subprocess is then dispatched.

fifoPath=${TMPDIR-/tmp}/$(basename "$0" .sh)_${LOGNAME}
fifoName="${fifoPath}"/job_control_$$
[ -d "${fifoPath}" ] || mkdir --mode=0700 "${fifoPath}"
mkfifo --mode=0700 "${fifoName}"

# open FIFO for read/write
exec 3<>"${fifoName}"
rm -f "${fifoName}"

while readlines
do  # perform job control only if a new job is pending
    while (( running >= jobs ))
    do
	reaper
    done
    generator
    $verbose && echo "${command[@]}"
    (
        if [ x"$outfile" == x"" ]
        then
	    "${command[@]}"
	else
	    echo "${command[@]}" > "${fifoPath}"/cmd_"${BASHPID}"
	    stdout="${fifoPath}"/cmd_"${BASHPID}"_out
	    "${command[@]}" 1>"${stdout}" 2>&1
	fi ; result=$?
	echo "${BASHPID}" 1>&3
	exit $result
    ) &

    (( ++running ))
done

while (( running > 0 ))
do
    reaper
done
exit 0

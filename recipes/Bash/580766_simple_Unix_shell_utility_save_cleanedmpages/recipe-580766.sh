# Put the code below into a shell script called m, in one of the 
# directories that are on your Unix PATH.

# Make it executable with:

# chmod u+x m

# Then you can run it with:

# m topic_name ...

# where the ... stands for more (optional) man page topic names.

# E.g.: m fopen fclose

# The cleaned-up man page for each topic specified, will be stored in 
# a text file called <topic_name>.m in your ~/man directory.

# You can then view it any time with the cat, more, or less commands 
# or with your text editor. E.g.: vi ~/man/fopen.m

mkdir -p ~/man
for i
do
    man $i | col -bx > ~/man/$i.m
done

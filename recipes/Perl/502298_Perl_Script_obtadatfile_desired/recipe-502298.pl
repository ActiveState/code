#!/usr/local/bin/perl

##############################################################################
# DESCRIPTION:
#
# This script takes data file, and extra attribute as inputs, and gives output
# data file in a particular format. It also addes extra attribute in beginning
# of each line in the output file. 
# 
# Additionally, if the number of fields in a line in the input file does not 
# match with the number of pre-defined fields, then such lines are filtered 
# and are stored in a discard output file.
# 
# Version: 0.1     13-Feb-2007  Rajkumar Jain          Initial Version

############################################################################

# Input file format is as following.
#
#  ATTRIBUTE03|ATTRIBUTE01|ATTRIBUTE05|ATTRIBUTE02|ATTRIBUTE04|
#  01_attr_03|01_attr_01|01_attr_05|01_attr_02|01_attr_04|
#  02_attr_03|02_attr_01|02_attr_05|02_attr_02||
#  03_attr_03|03_attr_01|03_attr_05|03_attr_02|
#  04_attr_03|04_attr_01|04_attr_05|
#  05_attr_03|05_attr_01|05_attr_05|||05_attr_04|
#  06_attr_03|06_attr_01|06_attr_05|06_attr_02|06_attr_04|
#


$num_args = @ARGV;

# If wrong number of arguments are passed to Perl script, then exit
if ($num_args != 2)
{
        print "Incorrect number of arguments to perl \n";
        exit 1;
}

$inp_file=@ARGV[0];
$extra_attr=@ARGV[1];


# Array containing column names (headers) in pre-defined order
# This can be changed as needed
@col_names = (    "ATTRIBUTE01",
		  "ATTRIBUTE02",
		  "ATTRIBUTE03",
		  "ATTRIBUTE04",
		  "ATTRIBUTE05"
		  );


$file_line_count=1;   

$flag = 0;

# Defining the output data file and discard data file names
$output_file=$inp_file."."."out";
$discard_file=$inp_file."."."discard";

# Defining File handles for input and output files
open (INPUT, "<$inp_file") || die "Can't open file for reading";
open (OUTPUT,">$output_file") || die "Can't open the output file for writing";

# Printing header names in the first line of output file
print OUTPUT "$extra_attr"."|";

foreach $column_name (@col_names) {
			print OUTPUT "$column_name"."|";
}

print OUTPUT "\n";


# Loop to itertate through each line of input file
while(<INPUT>)
{
    
    $elements_count = 0;

    # This processing is for the first line (containing headers).
    # We re-order the columns as per the order defined in array @col_names
    if($file_line_count == 1)
    {
    	@line_items = split(/\|/);
    	$header_count = @line_items;
        $file_line_count=$file_line_count +1;

	# Prepare a hash map between headercolumns in the input file 
	# and its index in the the col array
    	for ($i=0; $i<$header_count - 1;$i++) 
	  {
	        for ($j=0; $j<=$#col_names ;$j++) {
	         	if($line_items[$i] eq $col_names[$j] )	{
	         	         $HashOrder{$col_names[$j]} = $i;
			         
		         }
	         }
	  }
	  
        # Assign "" to all those columns which dont contain values
        for ($j=0; $j<=$#col_names ;$j++) {
        	if ($HashOrder{$col_names[$j]} != 0 && !($HashOrder{$col_names[$j]}) ) {
       			$HashOrder{$col_names[$j]} = "";
         		
         	} 
         }
 	
    	next;
    }

    #Get the current line
    $cur_file_line=$_;
    
    # Remove the spaces from beginning and end of the current line 
    # This is similar to trimming the line 
    $cur_file_line =~ s/^\s//;
    $cur_file_line =~ s/\s$//;
    
    $file_line="";

    if ($cur_file_line ne "") 
    {
          @line_items = split(/\|/);
    	  $elements_count = @line_items;
    	  
  	  # If the number of values in the line matches with the number of headers,
  	  # then we store the line in the output file
  	  if($elements_count ==  $header_count)  
  	  {
         
		 #rearrange according to the column positions
		 for ($j=0; $j<=$#col_names ;$j++) {

			if($HashOrder{$col_names[$j]} ne "")
			{
				$file_line = $file_line.$line_items[$HashOrder{$col_names[$j]}];
			}

			$file_line = $file_line."|";

		 }
	    
		# $extra_attr is prefixed in every line and then line
		# is printed in output file
		$file_line = $extra_attr."|".$file_line."\n";
		print OUTPUT "$file_line";
	  }
	  
	  # If the number of values in the line does not match with the number of headers,
	  # then we store the line in the discard output file
	  else
	  {
	       # The message below (The following.... ) is printed only once in 
	       # the discard output file. This is taken care of by value of $flag.
	       if ($flag == 0)
		  {
			open (DISCARD,">$discard_file") || die "Can't open the discard file for writing";
			print DISCARD "The following lines failed the field count validation \n";
			$flag =1;
		   }
		   
	       
	       # Printing the line of discard data in discard output file   
	       print DISCARD "$cur_file_line"."\n";
	  }
    }  #End of ($cur_file_line ne "") 
   
 }  #End of While 


# Closing file handles
close(OUTPUT);

if($flag == 1)
{
     close(DISCARD);
}

close(INPUT);

AjaxExample.pl

============================================================
#!perl

use DBI qw(:sql_types);
use CGI;
use CGI qw/:standard/;
use CGI::Ajax;

my $cgi = new CGI();
#--------------------------------------------------------------------
# Mapping the Perl subroutine to the triggering function
#--------------------------------------------------------------------
my $ajax = new CGI::Ajax( 'saveStudInfo_JScript' => \&saveStudInfo_PerlScript );

$cgi->header(-charset=>'US-ASCII');
print $ajax->build_html($cgi,\&generateHTML);


#--------------------------------------------------------------------
# Subroutine which generates the HTML
#--------------------------------------------------------------------        
sub generateHTML {
        # Hash which contains existing data
        %Students = get_Student_Info();
        $cnt = 1;
        
        # Write the html code in the form of a string
        $returnHTML .=  "\n<HTML>";
        $returnHTML .=  "\n<HEAD>";
        $returnHTML .=  "\n<TITLE>Student Information</TITLE>";
        $returnHTML .=  "<SCRIPT language=\"javascript\" src=\"/javascript/student.js\" type=\"text/javascript\"></SCRIPT>";
        $returnHTML .=  "\n</HEAD>";
                
        $returnHTML .=  "\n<BODY bgColor=\"#ffffff\">";
        $returnHTML .=  "<FORM  method=\"POST\" enctype=\"multipart/form-data\" name=\"StudentForm\">";
        $returnHTML .= "\n<BR>";
        $returnHTML .= "\n<BR>";
        $returnHTML .= "\n<TABLE cellspacing=\"0\" cellpadding=\"0\" align=\"center\">";
       
        $returnHTML .= "\n<TR><TD>";
        $returnHTML .= "\n<TABLE width=\"100%\" align=\"center\" border=\"1\" cellpadding=\"3\" cellspacing=\"1\" id= \"StudentInfoTable\">";
        $returnHTML .= "\n<TR>";
        $returnHTML .= "\n<TD align=\"center\" >SL No</TD>";
        $returnHTML .= "\n<TD align=\"center\"  nowrap>Name  </TD>";
        $returnHTML .= "\n<TD align=\"center\" nowrap>Marks  </TD>";
        $returnHTML .= "\n<TD align=\"center\" >&nbsp;</TD>";
        $returnHTML .= "\n</TR >";
                
        foreach $key (sort { $a <=> $b }(keys %Students)) {
                #View row 
                $returnHTML .=  "\n<INPUT type=\"hidden\" name=\"SerialNo\" id=\"SerialNo_$key\" value=\"$key\">";
                $returnHTML .= "\n<TR style=\"display:block\">";
                $returnHTML .="\n<TD align=\"center\" >$key</TD>";
                $returnHTML .="\n<TD align=\"center\"  nowrap><Div id=\"Div_Name_$key\">". (($Students{$key}->{Name}) ? $Students{$key}->{Name} : "&nbsp;")."</DIV></TD>";
                $returnHTML .="\n<TD align=\"center\"  nowrap><Div id=\"Div_Marks_$key\">". (($Students{$key}->{Name}) ? $Students{$key}->{Marks} : "&nbsp;")."</DIV></TD>";
                
                $returnHTML .= "\n<TD  align=\"center\"><INPUT type=\"button\" name=\"EditButton\" value=\"Edit\" style=\"cursor: hand; width: 40px\" onClick=\"makeRowEditable($cnt,'StudentInfoTable')\"></TD>";
                $returnHTML .= "\n</TR >";
                
                #Edit row 
                $returnHTML .= "\n<TR style=\"display:none\">";
                $returnHTML .="\n<TD align=\"center\"  nowrap>$key</TD>";
                $returnHTML .="\n<TD align=\"center\"  nowrap><INPUT type=\"text\" size=\"30\" id=\"Student_Name_$key\" value=\"$Students{$key}->{Name}\"  style=\"text-align: center\"></TD>";
                $returnHTML .="\n<TD align=\"center\"  nowrap><INPUT type=\"text\" size=\"10\" id=\"Student_Marks_$key\" value=\"$Students{$key}->{Marks}\"  style=\"text-align: center\"></TD>";
                $returnHTML .= "\n<TD  align=\"center\"><INPUT type=\"button\" name=\"SaveButton\" value=\"Save\" style=\"cursor: hand; width: 40px\" onClick=\"saveStudInfo_JScript(['Student_Name_$key','Student_Marks_$key','SerialNo_$key','NO_CACHE'],['Div_Name_$key','Div_Marks_$key'],'POST');makeRowViewable($cnt,'StudentInfoTable')\"></TD>";
                $returnHTML .= "\n</TR >";
                $cnt += 2;
        
        }
        $returnHTML .= "\n</TABLE>";
        $returnHTML .= "\n</TD></TR>";
        $returnHTML .= "\n</Table>";
                
}



#--------------------------------------------------------------------
# Perl Subroutine which is called aschronously
#--------------------------------------------------------------------
sub saveStudInfo_PerlScript {
        # Accept Input
        my $Name = shift;
        my $Marks = shift;
        my $SerialNo = shift;
        
        # Call subroutine which does database update
        update_Student_Info($SerialNo,$Name,$Marks);

        # Return Output
        return (@Return, ($Name ne "") ? $Name : "&nbsp;",($Marks ne "") ? $Marks : "&nbsp;");
}

#--------------------------------------------------------------------
# Subroutine which fetches the data
#--------------------------------------------------------------------
sub get_Student_Info {
        my %Details;
        my ($sql, $sth, $row);
        
        # DSN with the name "mydsn"  points to the Db
        $DB = "mydsn";
        # User name and password if any need to be specified. Currently no user name and pwd set.";
        $DB_USER = "";
        $DB_PASS= "";
        $dbh = DBI->connect("dbi:ODBC:$DB", $DB_USER, $DB_PASS);
        
        $sql = "SELECT * FROM Student";
        $sth = $dbh->prepare($sql);
        $sth->execute;
        $cnt = 1;
        while ($row = $sth->fetchrow_hashref) {
                $Details{$cnt++} = $row;
        }
        
        $sth->finish();
        return %Details;
}

#--------------------------------------------------------------------
# Subroutine which updates the Student Table in DB
#--------------------------------------------------------------------
sub update_Student_Info   {
        my $SerialNo = shift;  
        my $Name = shift; 
        my $Marks = shift; 
	
        my ($sql, $sth,$row);      
        
        # DSN with the name "mydsn"  points to the Db
        $DB = "mydsn";
        # User name and password if any need to be specified. Currently no user name and pwd set.
        $DB_USER = ""; 
        $DB_PASS= "";
        
        $dbh = DBI->connect("dbi:ODBC:$DB", $DB_USER, $DB_PASS);

        $sql  = "Update Student set Name = '$Name',Marks = $Marks where Sl_No = $SerialNo ";
        $sth = $dbh->prepare($sql);
        $sth->execute;
        $sth->finish();
        return $sql;
}                

============================================================


student.js
============================================================
/*
 * Toggles the rows from EDIT mode to VIEW mode. 
 * Invoked on clicking the 'SAVE' button in last column. 
 */
function makeRowViewable(rowNumber,id) {
        var table = document.all ? document.all[id]  : document.getElementById ? document.getElementById(id) : null;
        var editableRowNumber = rowNumber + 1 ;
        var nonEditableRowNumber = editableRowNumber -1 ;
        table.rows[editableRowNumber].style.display = "none" ;
        table.rows[nonEditableRowNumber].style.display = "block" ;  
}

/*
 * Toggles the rows from view mode to edit mode. 
 * Invoked on clicking the 'EDIT' button in last column. 
 */
function makeRowEditable(rowNumber,id) {
        var table = document.all ? document.all[id]  : document.getElementById ? document.getElementById(id) : null;
        var editableRowNumber = rowNumber + 1 ;
        var nonEditableRowNumber = editableRowNumber -1 ;
        table.rows[editableRowNumber].style.display = "block" ;
        table.rows[nonEditableRowNumber].style.display = "none" ;
}

============================================================

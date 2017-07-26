<?
$conn = new COM("ADODB.Connection") or die("Cannot start ADO"); 

// Microsoft Access connection string.
$conn->Open("DRIVER={Microsoft Access Driver (*.mdb)}; DBQ=C:\\inetpub\\wwwroot\\php\\mydb.mdb");

// SQL statement to build recordset.
$rs = $conn->Execute("SELECT myfield FROM mytable");
echo "<p>Below is a list of values in the MYDB.MDB database, MYABLE table, MYFIELD field.</p>";

// Display all the values in the records set
while (!$rs->EOF) { 
    $fv = $rs->Fields("myfield");
    echo "Value: ".$fv->value."<br>\n";
    $rs->MoveNext();
} 
$rs->Close(); 
?>

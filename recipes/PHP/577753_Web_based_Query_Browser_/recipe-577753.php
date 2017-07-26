// Connect to the database
$conn  = mysql_connect('localhost', 'root'); 

// Select the database to use
$Db = mysql_select_db('Table1',$conn); 
?>
</head>
	
<body>
	 <br />
	 <br />
	 <table  align="center" border="1" width="300px">
		 <tr>
			 <th colspan="3"> Query Browser </th>
			</tr>
	 <tr>
		 <td>SQL Command</td>
			 <td>
				 <form method="post" > 
				 <span class="style1"><input type="text" value="SELECT * FROM `table`" size="100" name="input"></span>
     </td>
<td> 
				 <input  type="submit" name="submit" value="GO"/>
				 </form>
			 </td>
		 </tr>
	 <tr>	
	<td colspan="5">
	
<?php
// Query the database
$input = @$_POST['input'];

$result = mysql_query($input) or die('MySQL Error: ' . mysql_error());
?>
			
<?php
	 // And if called for, iterate over the returned rows displaying information
     while($row = mysql_fetch_array($result))
     {
     // Display the information
     echo $row['ID'] . ' ' . $row['Name']. ' ' .
	 $row['Last'] . ' ' . $row['Middle'];
     } 										
?>
	
	 </td>
	 </tr>	
     <tr>
	
	<td >Error Message</td>
	<td colspan="2">
				
<?php 
     // Error handle things
     if($result)
     // Display error message
	 
	 {
	 echo $result;
	 $result ="No Query!";
	 }
	 
	 else
	 
	 {
     echo 'There was an error executing the MySQL query.  
     MySQL returned error number #' . mysql_error() . ' 
     and this explanation:<br />' . mysql_error();
     } 
?> 
	 </td>
	 </table>
	 </Body>
</Html>

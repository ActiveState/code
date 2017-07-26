<?php

// Two versions of Microsoft Office.  Choose one.
//$db = 'C:\\Program Files\\Microsoft Office\\Office\\Samples\\Northwind.mdb';
$db = 'C:\\Program Files\\Microsoft Office\\Office10\\Samples\\Northwind.mdb';

$conn = new COM('ADODB.Connection') or exit('Cannot start ADO.');

// Two ways to connect. Choose one.
$conn->Open("Provider=Microsoft.Jet.OLEDB.4.0; Data Source=$db") or exit('Cannot open with Jet.');
//$conn->Open("DRIVER={Microsoft Access Driver (*.mdb)}; DBQ=$db") or exit('Cannot open with driver.');

$sql = 'SELECT   ProductName, QuantityPerUnit, UnitPrice
	FROM     Products
	ORDER BY ProductName';
$rs = $conn->Execute($sql);

?>

<table>
<tr>
	<th>Product Name</th>
	<th>Quantity Per Unit</th>
	<th>Unit Price</th>
</tr>
<?php while (!$rs->EOF) { ?>
	<tr>
		<td><?php echo $rs->Fields['ProductName']->Value ?></td>
		<td><?php echo $rs->Fields['QuantityPerUnit']->Value ?></td>
		<td><?php echo $rs->Fields['UnitPrice']->Value ?></td>
	</tr>
	<?php $rs->MoveNext() ?>
<?php } ?>
</table>

<?php

$rs->Close();
$conn->Close();

$rs = null;
$conn = null;

?>

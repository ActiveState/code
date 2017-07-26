<html>
	<head>
		<title>
			Validating Emails
		</title>
		
	</head>
	
	<body>
		<form method="post">
		
		    <!-- Email Inputs - type email to see if they are Validated -->
			Email 1 :<input type="text" name="e1a" value="Enter Email here"/><br /><br />
			Email 2 :<input type="text" name="e2a" /><br /><br />

	        <!-- Submit button -->
			<input type="submit" name="submit" value="Validate"/><br /><br />
			
		</form>
		
		<?php
		function IsValidEmail()
		{
		if(isset($_POST['submit']))
			{
		     // Email imput
			$Email[0] = @$_POST['e1a'];
			$Email[1] = @$_POST['e2a'];
				
			// Checks Eamils to see if the are REAL Emails 
				
			foreach($Email as $Emails)
				{ // checks Emails - .net , .com , .au  & etc
				if(!preg_match("/^[_\.0-9a-zA-Z-]+@([0-9a-zA-Z]
				[0-9a-zA-Z-]+\.)+[a-zA-Z]{2,6}$/i", $Emails))
				{ // checks Emails to see if Validated successfully
                                echo "$Emails
				: Validated successfully !<br /><br />";
				}
				else
				{ // checks Emails to see if Invalid Emails
				echo " $Emails
				: Invalid Email <br /><br />";
				}	
				}	
	     	}
		} 
	?>
</body>

<p> Shows Valid Email </p>
 <?php IsValidEmail() ?>

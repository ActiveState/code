<?
/*
** SelectionBox class
*/

class SelectionBox
{
	function SetName($name)
	{
		$this->myname = $name;
	}
	
	function SetOption($optionvalue,$optionname)
	{
		$this->options[$optionname] = $optionvalue;
	}

	function CreateBox($selected)
	{
		if($this->options)
		{
			print "<SELECT name='".$this->myname."'>\n";
	
			// Create Options
			foreach($this->options as $optionname=>$optionvalue)
			{
				print "<OPTION value='$optionvalue'";
				
				// Check if option should be selected
				if($selected == $optionvalue)
				{
					print " SELECTED";
				}
			
				print ">$optionname</OPTION>\n";
			}
			
			print "</SELECT>";
		}
		else
		{
			print "Error: No options specified";
		}
	}
}

?>

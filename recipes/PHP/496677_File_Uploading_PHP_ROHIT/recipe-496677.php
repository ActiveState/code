<pre>
<form enctype="multipart/form-data" action="index.php" method="POST">
    <!-- MAX_FILE_SIZE must precede the file input field -->
    <input type="hidden" name="MAX_FILE_SIZE" value="30000" />
    <!-- Name of input element determines name in $_FILES array -->
    Send this file: <input name="userfile" type="file" />
     <input type="submit" value="Send File" onClick="return checkfile(this.form);" />
</form>

write this code in the head section of your php in which you have written the above code.

<html>
<head>
<title>
</title>
<script langauge="javascript" >
function checkfile(form)
{

if (form.userfile.value == "")
{
alert('Please Select a File To Upload');

return false;
}
else
{
return true;
}


}
</script>

</head>


Now write this code in the action script i.e in my case it is index.php

$uploaddir = '/home/rohit/upload/';
$uploadfile = $uploaddir . basename($_FILES['userfile']['name']);


if (move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile))
{

  echo "File is valid, and was successfully uploaded.\n";

}
 else

 {
   echo "file upload error\n";
}



Thats all
do mail me ur feedback at rajdsouza@yahoo.com










</pre>

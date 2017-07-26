<?php
$message = new COM('CDO.Message');
$message->To = 'receiver@somplace.com';
$message->From = 'Sender@MyCompany.com';
$message->Subject = 'This is a subject line';
$message->HTMLBody = '<html><body>This is <b>the</b> body!</body></html>';
$message->AddAttachment('http://www.ActiveState.com');
$message->Send();
?>

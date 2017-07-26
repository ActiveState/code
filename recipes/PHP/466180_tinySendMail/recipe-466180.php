<?php
/* Dave Silvia (c) 2006, dsilvia@mchsi.com.  Any usage permitted.  Credit
   where credit is due is appreciated!;)
 */
/*
Synopsis:

	int tinySendMail(from,to,subject,message)
	
	Return of non-zero indicates success.

Examples:

	tinySendMail("me@myisp.com","you@yourisp.com","Sent with tinySendMail",
		"This function does pretty well for a little fella!  What do you think?");
		
	$ret=tinySendMail("me@myisp.com","you@yourisp.com","Sent with tinySendMail",
		"This function does pretty well for a little fella!  What do you think?",
		"yourmailer.yourisp.com",24,"mywork.com");
	if(!$ret)
	{
		print("Oh, pshaw!  It didn't work!<br>");
	}

Description:
   EXTREMELY simple and tiny send mail.  Only 7 states and addresses only 3
   SMTP return codes:
     220 Service Ready
     250 Requested mail action okay, completed
     354 Start mail input; end with <CRLF>.<CRLF>
   Any other response is assumed to be an error, a QUIT is sent, and
   tinySendMail returns with a zero return.  Non-zero return indicates success.
   Arguments:
     $sender:
        traditional 'From:', e.g., you@yourdomain.com
     $receiver:
        traditional 'To:', e.g., them@theirdomain.com
     $subject:
        traditional 'Subject:'
     $message:
        body text.  Folds at 990 characters.  RFC2821 suggests a limit of 1000
        including CRLF.  This is compliant, but you can change the variable
        $textLineLimit to suit your purposes or any specific server.
     $rcvsmtp:
        smtp server of the receiver, e.g., mail.theirdomain.com.
        optional, set to the domain in the receiver's email address with
        'mail.' prepended by default.  If you don't know the receiver's
        smtp server and/or the default doesn't work, you may specify a
        server you know will accept the email for transfer, i.e., your own smtp
        server will probably accommodate.
     $rcvport:
        port to connect to on $rcvsmtp.  default is 25 (SMTP), you may
        optionally set it to another if the receiver uses a special port.
     $sndhost:
        domain of the sending host, e.g., yourdomain.com.  Not necessarily
        the same as the one in $sender, as you may be sending from a different
        host than the one your email is on.
        optional, set to the local host as determined by php_uname('n').
     $verbose:
        optional argument to turn on informational messages.  Off by default.
 */
function tinySendMail($sender,$receiver,$subject,$message
	,$rcvsmtp=0,$rcvport=25,$sndhost=0,$verbose=0)
{
	/* RFC2821 says 1000 including CRLF, so this should be compliant */
	$textLineLimit=990;
	if(!$sndhost)$sndhost=php_uname('n');
	if(!$rcvsmtp)$rcvsmtp="mail.".substr(strstr($receiver,"@"),1);
	$mailState_open=0;
	$mailState_ehlo=1;
	$mailState_rcpt=2;
	$mailState_data=3;
	$mailState_send=4;
	$mailState_quit=5;
	$mailState_return=6;
	$curMailState=$mailState_open;
	if(!($fp=fsockopen($rcvsmtp,$rcvport,$errno,&$errstr)))
	{
		infoPrint($verbose,"Could not open a socket to $rcvsmtp on port $rcvport<br>");
		infoPrint($verbose,"Error#: $errno: $errstr<br>");
		return(0);
	}
	infoPrint($verbose,"Opened connection to $rcvsmtp:$rcvport<br>");
	$returncode=1;
	while($curMailState != $mailState_return)
	{
		$ret=fgets($fp);
		$cod=substr($ret,0,3);
		if($curMailState == $mailState_ehlo)
		{ /* drain the pipe of all EHLO informational lines */
			if($cod == 250)
			{
				$ret=fgets($fp);
				$contChar=substr($ret,3,1);
				infoPrint($verbose,"ret: $ret<br>");
				while($contChar == "-")
				{
					infoPrint($verbose,"ret: $ret<br>");
					$ret=fgets($fp);
					$contChar=substr($ret,3,1);
				}
			}
		}
		infoPrint($verbose,"ret: $ret<br>cod: $cod<br>");
		switch($cod)
		{
			case 220:
				switch($curMailState)
				{
					case $mailState_open:
						$snd="EHLO $sndhost\r\n";
						$curMailState=$mailState_ehlo;
						break;
					default:
						$snd="QUIT\r\n";
						$returncode=0;
						$curMailState=$mailState_return;
				}
				break;
			case 250:
				switch($curMailState)
				{
					case $mailState_ehlo:
						$snd="MAIL FROM:<$receiver>\r\n";
						$curMailState=$mailState_rcpt;
						break;
					case $mailState_rcpt:
						$snd="RCPT TO:<$receiver>\r\n";
						$curMailState=$mailState_data;
						break;
					case $mailState_data:
						$snd="DATA\r\n";
						$curMailState=$mailState_send;
						break;
					case $mailState_quit:
						$snd="QUIT\r\n";
						$curMailState=$mailState_return;
						break;
					default:
						$snd="QUIT\r\n";
						$returncode=0;
						$curMailState=$mailState_return;
				}
				break;
			case 354:
				switch($curMailState)
				{
					case $mailState_send;
						$snd="From: $sender\n";
						$snd.="To: $receiver\n";
						$snd.="Subject: $subject\n";
						$snd.="Date: ".date('r')."\n";
						$snd.="Message-ID: <".
							date('YmdHis').":".
							php_uname('n').":".
							getmypid().
							":$sender>\n\n";
						$snd.=wordwrap($message,$textLineLimit,"\n",1);
						$sndArray=explode("\n",$snd);
						$numLines=count($sndArray);
						for($i=0; $i < $numLines; $i++)
						{
							fputs($fp,$sndArray[$i]."\r\n");
						}
						$snd="\r\n.\r\n";
						$curMailState=$mailState_quit;
						break;
					default:
						$snd="QUIT\r\n";
						$returncode=0;
						$curMailState=$mailState_return;
				}
				break;
			default:
				$snd="QUIT\r\n";
				$returncode=0;
				$curMailState=$mailState_return;
		}
		infoPrint($verbose,"snd: $snd<br>");
		fputs($fp,$snd);
	}
	$ret=fgets($fp);
	infoPrint($verbose,"ret: $ret<br>");
	fclose($fp);
	return($returncode);
}


/* Print informational messages if the $verbose argument is non-zero
 */
function infoPrint($verbose,$msg)
{
	if($verbose)
	{
		print($msg);
	}
}
?>

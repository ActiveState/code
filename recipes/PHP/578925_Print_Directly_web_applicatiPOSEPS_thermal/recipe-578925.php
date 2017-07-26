<?php
/**
Modified by: Imam Ferianto < iferianto@yahoo.com >  at 1 sep 2014
Credit:  Reed's Hardware Projects
http://reed-printer.blogspot.com/2014/04/review-sprt-sp-pos58iv-thermal-receipt.html

this php script will printout barcode label directly from the web by phpscript
I am using cheap mini thermal receipt printer RP80 autocutter from http://www.rongtatech.com
http://www.rongtatech.com/products-look-11.html

I believe this code will work in other RAW PRINTER types

TIPS:
First you need to connect devices as "GENERIC RAW PRINTER" on ubuntu server
And put this script under /var/www  (www-data) apache user
Also you need to execute this command , before run on ubuntu shell to gain permission on lp0 dev: 
bash#   sudo gpasswd -a www-data lp
**/

//constant
$rn=chr(13).chr(10);
$esc=chr(27);
$cutpaper=$esc."m";
$bold_on=$esc."E1";
$bold_off=$esc."E0";
$reset=pack('n', 0x1B30);

 
//printer setup
$printer="/dev/usb/lp0";


//formating data text:
$string = "--test EAN-13 barcode wide--\n";
$string .= "\x1d\x77\x04";   # GS w 4
$string .= "\x1d\x6b\x02";   # GS k 2 
$string .= "5901234123457\x00";  # [data] 00
$string .= "-end-\n";

//cut paper at end
//$string.=$cutpaper;


//send data to USB printer
$fp=fopen($printer, 'w');
fwrite($fp,$string);
fclose($fp);



//formating the 2nd data
$string = "--test EAN-13 barcode wide--\n";
$string .= "\x1d\x77\x04";   # GS w 4
$string .= "\x1d\x6b\x02";   # GS k 2 
$string .= "111114123457\x00";  # [data] 00
$string .= "-end-\n";


//send data via TCP/IP port : the printer has tcp interface
$port = "9100";
$host = "192.168.1.87";
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    echo "socket_create() failed: reason: " . socket_strerror(socket_last_error    ()) . "\n";
} else {
    echo "OK.\n";
}
$result = socket_connect($socket, $host, $port);
if ($result === false) {
    echo "socket_connect() failed.\nReason: ($result) " . socket_strerror    (socket_last_error($socket)) . "\n";
} else {
    echo "OK.\n";
}
socket_write($socket, $string, strlen($string));
socket_close($socket);




?>

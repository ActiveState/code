<?
    header ("Content-type: image/jpeg"); # We will create an *.jpg
    $pic = @imagecreatefromjpeg($url) or die ("Image not found!");
    if ($pic) {
        $width = imagesx($pic);
        $height = imagesy($pic);
        $twidth = 160; # width of the thumb 160 pixel
        $theight = $twidth * $height / $width; # calculate height
        $thumb = @imagecreatetruecolor ($twidth, $theight) or
	    die ("Can't create Image!");
	imagecopyresized($thumb, $pic, 0, 0, 0, 0,
	    $twidth, $theight, $width, $height); # resize image into thumb
	ImageJPEG($thumb,"",75); # Thumbnail as JPEG
    }
?>

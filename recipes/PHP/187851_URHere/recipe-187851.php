<?
/*
Author: Flinn Mueller
Last Updated: 2/26/03
Copyright 2001-2003 ActiveIntra.net, Inc.
Home: http://activeintra.net/php/article.php?id=2
Contact: flinn _AT_ activeintra _DOT_ net
*/
class URHere {
    var $sitename = "My Site";
    var $seperator = "&gt;"; // "&gt;" is ">", "&lt;" is "<", ":", ,"::", "|", "*""
    var $text = "";
    var $link = "";

    function Text($sent_path = "")
    {
        if (strlen($sent_path) > 0)
            $path = explode("/", $sent_path);
        else
            $path = explode("/", $_SERVER[PHP_SELF]);

        $c = 1;
        while (list($key, $val) = each($path)) {
            if ($c > 1) {
                $this->text .= " " . $this->seperator . " ";
                $val = str_replace("_", " ", $val); //Strip underscore
                $val = str_replace("-", " ", $val); //Strip hyphen
                $this->text .= ucwords(ereg_replace("\..*$", "", $val)); //Strip extensions
            } else {
                $this->text = $this->sitename;
            } 
            $c++;
        } 
        return $this->text;
    } 

    function Link($sent_path = "")
    {
        if (strlen($sent_path) > 0)
            $path = explode("/", $sent_path);
        else
            $path = explode("/", $_SERVER[PHP_SELF]);

        $c = 1;
        while (list($key, $val) = each($path)) {
            if ($c > 1) {
                $this->link .= " " . $this->seperator . " ";
                if ($c < count($path))
                    $link .= "$val/";
                else
                    $link .= "$val";
                $val = str_replace("_", " ", $val); //Strip underscore
                $val = str_replace("-", " ", $val); //Strip hyphen
                $this->link .= '<a href="/' . $link . '">' . ucwords(ereg_replace("\..*$", "", $val)) . '</a>'; //Strip extensions
            } else {
                $this->link = '<a href="/">' . $this->sitename . '</a>';
            } 
            $c++;
        } 
        return $this->link;
    } 

} //End Class 

?>

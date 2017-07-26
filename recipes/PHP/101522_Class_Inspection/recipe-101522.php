<?php

// include some file that defines classes, such as PEAR's mail.php
require("Mail.php");

$classes = get_declared_classes();
foreach($classes as $class) {
    echo("<ul>".$class.":<br>\n");
    $vars = get_class_vars($class);
    $methods = get_class_methods($class);
    foreach($vars as $varname=>$value) {
        echo("<li>var \$$varname = $value</li>\n");
    }
    foreach($methods as $method) {
        echo("<li>method $method</li>\n");
    }
    echo "</ul>";
}
?>

// This is Javascript, not PHP!

function js_array_to_php_array (a)
// This converts a javascript array to a string in PHP serialized format.
// This is useful for passing arrays to PHP. On the PHP side you can 
// unserialize this string from a cookie or request variable. For example,
// assuming you used javascript to set a cookie called "php_array"
// to the value of a javascript array then you can restore the cookie 
// from PHP like this:
//    <?php
//    session_start();
//    $my_array = unserialize(urldecode(stripslashes($_COOKIE['php_array'])));
//    print_r ($my_array);
//    ?>
// This automatically converts both keys and values to strings.
// The return string is not URL escaped, so you must call the
// Javascript "escape()" function before you pass this string to PHP.
{
    var a_php = "";
    var total = 0;
    for (var key in a)
    {
        ++ total;
        a_php = a_php + "s:" +
                String(key).length + ":\"" + String(key) + "\";s:" +
                String(a[key]).length + ":\"" + String(a[key]) + "\";";
    }
    a_php = "a:" + total + ":{" + a_php + "}";
    return a_php;
}

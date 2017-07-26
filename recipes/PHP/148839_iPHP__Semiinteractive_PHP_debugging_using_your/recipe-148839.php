<?php
function undo_magic_quotes ( $source )
{
  // in case magic_quotes_gpc is ON, we undo its effect ( "\'" => "'")
  $source = str_replace ( "\\'", "'",  $source );
  // "backslash double quote" becomes "simply double quote"
  $source = str_replace ( "\\\"", "\"",  $source );
  // "backslash backslash" becomes simply "backslash"
  $source = str_replace ( "\\\\", "\\", $source );

  return $source;
}

$actual_code = undo_magic_quotes ( $_POST["code"] );
?>
<html>
  <head>
    <title>
      iPHP
    </title>
  </head>
  <body>
    <form method="post">
      <textarea name="code" cols="80" rows="10" wrap="virtual"><?php
        echo htmlentities ( $actual_code, ENT_QUOTES );
      ?></textarea>
      <input type="submit" value="Execute" />
    </form>
    <hr />
    <pre><?php
      if ( strlen ( trim ( $actual_code ) ) > 0 )
      {
        echo "Results of execution:\n";
        flush ( );
        echo eval ( $actual_code );
      }
    ?>
    </pre>
  </body>
</html>

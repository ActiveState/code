<!DOCTYPE html>
<html>
  <head>
    <title>Is enabled ... ?</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
      table, th, td {
        border: 1px #c0c0c0 solid;
      }
      table {
        width: 50%;
      }
      th, td, p {
        font-family: tahoma;
      }
      th, td {
        text-align: center;
      }
      th {
        background-color: #c0c0c0;
      }
    </style>
  </head>
  <body>
    <table cellpadding="1" cellspacing="0">
      <tr>
        <th>Parameter</th>
        <th>Current state</th>
      </tr>
      <tr>
        <td>Cookie</td>
        <td>
          <script>
            var cookie = navigator.cookieEnabled;
            document.write(cookie ? "Enabled" : "Disabled");
          </script>
          <noscript>X</noscript>
        </td>
      </tr>
      <tr>
        <td>JavaScript</td>
        <td>
          <script>
            document.write("Enabled");
          </script>
          <noscript>Disabled</noscript>
        </td>
      </tr>
      <tr>
        <td>Java</td>
        <td>
          <script>
            var java = navigator.javaEnabled();
            document.write(java ? "Enabled" : "Disabled");
          </script>
          <noscript>X</noscript>
        </td>
      </tr>
    </table>
    <p>Note: X means that parameter cannot be detected without javascript.</p>
  </body>
</html>

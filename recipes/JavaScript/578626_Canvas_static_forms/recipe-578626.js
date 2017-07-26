<!DOCTYPE html>
<html>
  <head>
    <title>Canvas: static forms</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style type="text/css">
      html, body {
        width: 100%;
        height: 100%;
      }
      * {
        margin: 0;
        padding: 0;
      }
      td {
        color: #aa99ff;
        text-align: center;
      }
      #container {
        width: 100%;
        height: 100%;
        vertical-align: middle;
      }
    </style>
  </head>
  <body>
    <table id="container">
      <tr><td><canvas id="canvas">o_Ops!</canvas></td></tr>
    </table>
    <script language="javascript">
      var cnv = document.getElementById("canvas");
      cnv.width = window.innerWidth;
      cnv.height = window.innerHeight;
      
      var ctx = cnv.getContext("2d");
      ctx.clearRect(0, 0, cnv.width, cnv.height);
      $(Math.floor(cnv.width / 2), Math.floor(cnv.height / 2), 7);
      
      function $(cX, cY, vol) {
        var x = 0, y = 0, f;
        ctx.beginPath();
        
        for (var cr = 0; cr <= 360; cr += 0.01) {
          f = vol * (4 + Math.sin(5 * cr) +
                     0.5 * Math.sin(10 * cr) +
                     1 / 6 * Math.sin(60 * cr)
                    ) * (cr / 50 + 1);
          x = Math.floor(f * Math.cos(cr) + cX);
          y = Math.floor(f * Math.sin(cr) + cY);
          
          if (cr == 0) ctx.moveTo(x, y);
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    </script>
  </body>
</html>

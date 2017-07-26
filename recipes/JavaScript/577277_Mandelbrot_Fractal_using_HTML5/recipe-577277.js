<html>
<head><title>Mandelbrot Fractal Using HTML5 Canvas</title></head>
<body>

<canvas id="canvas" width="500" height="500">
Your browser does not support HTML5 Canvas.
</canvas>

<script type="text/javascript">
// FB - 20121227
// Tested only using Firefox

var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var xr = context.canvas.width;
var yr = context.canvas.height;
var imgd = context.createImageData(xr, yr);
var pix = imgd.data;

var xmin = -2.0; var xmax = 1.0;
var ymin = -1.5; var ymax = 1.5;

// these are for coloring the image
var mr0 = 0; var mg0 = 0; var mb0 = 0;
while(mr0 == mg0 || mr0 == mb0 || mg0 == mb0) 
{
    mr0 = Math.pow(2, Math.ceil(Math.random() * 3 + 3));
    mg0 = Math.pow(2, Math.ceil(Math.random() * 3 + 3));
    mb0 = Math.pow(2, Math.ceil(Math.random() * 3 + 3)); 
}
var mr1 = 256 / mr0; var mg1 = 256 / mg0; var mb1 = 256 / mb0;

var maxIt = 256;
var x = 0.0; var y = 0.0;
var zx = 0.0; var zx0 = 0.0; var zy = 0.0;
var zx2 = 0.0; var zy2 = 0.0;

for (var ky = 0; ky < yr; ky++)
{
    y = ymin + (ymax - ymin) * ky / yr;
    for(var kx = 0; kx < xr; kx++)
    {
        x = xmin + (xmax - xmin) * kx / xr;
        zx = x; zy = y;
        for(var i = 0; i < maxIt; i++)
        {
            zx2 = zx * zx; zy2 = zy * zy;
            if(zx2 + zy2 > 4.0) break;
            zx0 = zx2 - zy2 + x;
            zy = 2.0 * zx * zy + y;
            zx = zx0;
        }
        var p = (xr * ky + kx) * 4;
        pix[p] = i % mr0 * mr1;     // red
        pix[p + 1] = i % mg0 * mg1; // green
        pix[p + 2] = i % mb0 * mb1; // blue
        pix[p + 3] = 255;           // alpha
    }
}

context.putImageData(imgd, 0, 0);
</script>
</body>
</html>

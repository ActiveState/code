<html>
<head><title>Interactive Mandelbrot Fractal Using HTML5 Canvas</title></head>
<body>

<canvas id="canvas" width="512" height="512">
Your browser does not support HTML5 Canvas.
</canvas>

<br>
<b>Keys:</b> 
<br>
<b>+: zoom in</b> 
<br>
<b>-: zoom out</b> 
<br>
<b>a: move left</b> 
<br>
<b>d: move right</b> 
<br>
<b>w: move up</b> 
<br>
<b>s: move down</b> 
 
<script type="text/javascript">
// FB36 - 201706050 (0:Monday)
// Tested only using Firefox

document.onkeypress = function(evt) 
{
    evt = evt || window.event;
    var charCode = evt.keyCode || evt.which;
    var charStr = String.fromCharCode(charCode);
    var p = 0.1; // 10 percent
    var d = 0.0;
    // zoom in
    if(charStr == '+')
    {
        d = (xmax - xmin) * p;
        xmin = xmin + d;
        xmax = xmax - d;
        d = (ymax - ymin) * p;
        ymin = ymin + d;
        ymax = ymax - d;
    };
    // zoom out
    if(charStr == '-')
    {
        d = (xmax - xmin) * p;
        xmin = xmin - d;
        xmax = xmax + d;
        d = (ymax - ymin) * p;
        ymin = ymin - d;
        ymax = ymax + d;
    };
    // move left
    if(charStr == 'a') 
    {
        d = (xmax - xmin) * p;
        xmin = xmin - d;
        xmax = xmax - d;
   };
    // move right
    if(charStr == 'd') 
    {
        d = (xmax - xmin) * p;
        xmin = xmin + d;
        xmax = xmax + d;
    };
    // move up
    if(charStr == 'w') 
    {
        d = (ymax - ymin) * p;
        ymin = ymin - d;
        ymax = ymax - d;
    };
    // move down
    if(charStr == 's') 
    {
        d = (ymax - ymin) * p;
        ymin = ymin + d;
        ymax = ymax + d;
    };
    
    DrawMandelbrotFractal(xmin, xmax, ymin, ymax, mr0, mr1, mg0, mg1, mb0, mb1);
};

function DrawMandelbrotFractal(xmin, xmax, ymin, ymax, mr0, mr1, mg0, mg1, mb0, mb1)
{
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var xr = context.canvas.width;
    var yr = context.canvas.height;
    var imgd = context.createImageData(xr, yr);
    var pix = imgd.data;

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
}

// main
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

DrawMandelbrotFractal(xmin, xmax, ymin, ymax, mr0, mr1, mg0, mg1, mb0, mb1);

</script>
</body>
</html>

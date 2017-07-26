<html>
<head><title>Sierpinski Triangle Fractal using HTML5 Canvas</title></head>
<body>

<canvas id="canvas" width="514" height="514">
This text is displayed if your browser does not support HTML5 Canvas.
</canvas>

<script type="text/javascript">
// Sierpinski Triangle Fractal using Line Automaton (1D CA).
// The 1D CA rule used is actually Pascal's Triangle Mod 2.
// FB - 201007051
// Tested only using Firefox 3.5

// globals
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var xr = context.canvas.width;
var yr = context.canvas.height;
var imgd = context.createImageData(xr,yr);
var pix = imgd.data;
var rd = 0;
var gr = 0;
var bl = 0;
var al = 0;

function putpixel(ix, iy, rd, gr, bl, al)
{
    var p = (yr * iy + ix) * 4;
    pix[p]   = rd % 256; // red
    pix[p+1] = gr % 256; // green
    pix[p+2] = bl % 256; // blue
    pix[p+3] = al % 256; // alpha
}

function getpixel(ix, iy)
{
    var p = (yr * iy + ix) * 4;
    rd = pix[p];   // red
    gr = pix[p+1]; // green
    bl = pix[p+2]; // blue
    al = pix[p+3]; // alpha
}

// seed
var rd0 = Math.floor(Math.random() * 128) + 1;
var gr0 = Math.floor(Math.random() * 128) + 1;
var bl0 = Math.floor(Math.random() * 128) + 1;
putpixel(xr - 1, 0, rd0, gr0, bl0, 255);

var rd1 = 0;
var gr1 = 0;
var bl1 = 0;

for(var ky = 1; ky < yr - 1; ky++)
{
    for(var kx = 0; kx < xr - 1; kx++)
    {
        getpixel(kx, ky - 1);
        rd1 = rd;
        gr1 = gr;
        bl1 = bl;
        getpixel(kx + 1, ky - 1);
        if((rd1 == 0 && rd > 0) || (rd1 > 0 && rd == 0)) // XOR
            putpixel(kx, ky, rd0, bl0, gr0, 255);
    }
}

context.putImageData(imgd, 0,0);

</script>
</body>
</html>

// <applet code="SF2DCA" width=500 height=300></applet>
// Snowflake fractal using 2D Cellular Automaton
// FB - 201007165
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;

public class SF2DCA extends Applet
{

    Image img;
    int w, h, pix[][], alpha, flag, ctr;
    int dx[] = {2, 1, -1, -2, -1, 1};
    int dy[] = {0, -1, -1, 0, 1, 1};
  
    public void init()
    {
        setBackground ( Color.black );
        w=getSize().width;
        h=getSize().height;
        alpha=255;
        ctr = 0;
        flag=1;
        pix=new int[2][w * h];
        putpixel(0, w / 2, h / 2, 255, 255, 255); // seed
    }

    public void putpixel(int flag, int x, int y, int red, int green, int blue)
    {
        pix[flag][w * y + x] = (alpha << 24) | (red << 16) | (green << 8) | blue;
    }

    public int getpixel(int flag, int x, int y)
    {
        return ((pix[flag][w * y + x] & 16777215) % 16777216);
    }
    
    public void paint(Graphics g)
    {
        if(ctr < 110) // grow until this size reached
        {   
            flag = 1 - flag;
            ctr++;
            int sum, kx, ky;

            for(int y = 0; y < h; y++)
                for(int x = 0; x < w; x++)
                    if(getpixel(flag, x, y) == 0)
                    {
                        sum = 0; // count the neighbors
                        for(int j = 0; j < 6; j++)
                        {
                            kx = x + dx[j];
                            ky = y + dy[j];
                            if( kx >= 0 && kx < w && ky >= 0 && ky < h )
                                if(getpixel(flag, kx, ky) > 0)
                                    sum++;
                        }
                        if(sum == 1) // add a new pixel only if there is 1 neighbor
                            putpixel(1 - flag, x, y, ctr % 8 * 32, ctr % 16 * 16, ctr % 32 * 8);
                    }
                    else
                        pix[1 - flag][w * y + x] = (alpha << 24) | getpixel(flag, x, y);

            img = createImage(new MemoryImageSource(w, h, pix[1 - flag], 0, w));
            g.drawImage(img, 0, 0, this);
            repaint();
        }
    }

    public void update(Graphics g) { paint(g); }
}

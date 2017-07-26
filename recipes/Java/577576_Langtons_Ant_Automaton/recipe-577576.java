// <applet code="Ant" width=100 height=100>
// <PARAM NAME="refresh" VALUE="60">
// <PARAM NAME="rndPixels" VALUE="100">
// </applet>
// (Generalized) Langton's Ant Automaton
// http://en.wikipedia.org/wiki/Langton%27s_ant
// FB - 201102163
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;
import java.util.Arrays;

public class Ant extends Applet
{
    Image img;
    int pix[],mat[];
    int red[],green[],blue[];
    int w,h;
    long ctm;
    int rep[],dir[]; // byte replacement and direction arrays
    int[] dirx={1,1,0,-1,-1,-1,0,1};
    int[] diry={0,1,1,1,0,-1,-1,-1};
    int x,y; // location of the ant
    int refresh; // refresh period in seconds
    int rndPixels; // # of initial random pixels on the screen

    private void putPixel(int x,int y,int c)
    {
        int alpha=255;
        pix[w*y+x]=(alpha<<24)|(red[c]<<16)|(green[c]<<8)|blue[c];
        mat[w*y+x]=c;
    }
    
    public void init()
    {
        refresh=Integer.parseInt(getParameter("refresh"))*1000;
        rndPixels=Integer.parseInt(getParameter("rndPixels"));
        w=getSize().width;
        h=getSize().height;
        pix=new int[w*h]; 
        mat=new int[w*h];
        Arrays.fill(pix,2147483647);
        
        // create a color palette (RGBY)
        red=new int[256];
        green=new int[256];
        blue=new int[256];
        
        for(int i=0;i<256;i++)
        {
            switch((int)(i/64))
            {
                case 0:
                    red[i]=(i%64)*3+64;
                    green[i]=0;
                    blue[i]=0;
                    break;
                case 1:
                    red[i]=0;
                    green[i]=(i%64)*3+64;
                    blue[i]=0;
                    break;
                case 2:
                    red[i]=0;
                    green[i]=0;
                    blue[i]=(i%64)*3+64;
                    break;
                case 3:
                    red[i]=(i%64)*3+64;
                    green[i]=(i%64)*3+64;
                    blue[i]=0;
                    break;
            }
        }

        // create byte replacement and direction arrays
        rep=new int[256];
        dir=new int[256];
        
        for(int i=0;i<256;i++)
        {
            rep[i]=(int)(Math.random()*256);
            dir[i]=(int)(Math.random()*8);
        }
        
        // put random pixels onto screen and start the ant from the last one
        for(int i=0;i<rndPixels;i++)
        {
            x=(int)(Math.random()*w);
            y=(int)(Math.random()*h);
            putPixel(x,y,(int)(Math.random()*256));
        }

        ctm=System.currentTimeMillis();        
    }

    public void paint(Graphics g)
    {
        // restart the applet periodically
        if((System.currentTimeMillis()-ctm)>=refresh) {init();}

        // run the ant 1 step
        int c=mat[w*y+x];
        putPixel(x,y,rep[c]);
        x+=dirx[dir[c]];
        y+=diry[dir[c]];
        // keep the ant in the screen
        if(x<0) x+=w;
        if(x>w-1) x-=w;
        if(y<0) y+=h;
        if(y>h-1) y-=h;
        
        img=createImage(new MemoryImageSource(w,h,pix,0,w));
        g.drawImage(img,0,0,this);
        repaint();
    }

    public void update(Graphics g) { paint(g); } // to prevent flickering
}

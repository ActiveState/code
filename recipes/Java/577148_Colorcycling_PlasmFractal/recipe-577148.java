// <applet code="Plasma" width=800 height=600></applet>
// FB - 201003265
// Color-Cycling Plasma Fractal
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;

public class Plasma extends Applet
{
  Image img;
  // pix will hold the actual image data
  // mat will hold the image data of palette colors
  int pix[], mat[];
  int red[],green[],blue[];
  int w,h,inc;
  float roughness;
  long ctm;

  public void adjust(int xa,int ya,int x,int y,int xb,int yb)
  {
    int c,d;
    if(mat[w*y+x]==0)
    {
      d=(int)(Math.abs(xa-xb)+Math.abs(ya-yb));
      c=(mat[w*ya+xa]+mat[w*yb+xb])/2+(int)((Math.random()-0.5)*d*roughness);
      c=((int)Math.abs(c))%256;
      mat[w*y+x]=c;
    }
  }

  public void subdivide(int x1,int y1,int x2,int y2)
  {
    int x,y;
    if(!((x2-x1<2) && (y2-y1<2)))
    {
      x=(x1+x2)/2;y=(y1+y2)/2;
      adjust(x1,y1,x,y1,x2,y1);adjust(x2,y1,x2,y,x2,y2);
      adjust(x1,y2,x,y2,x2,y2);adjust(x1,y1,x1,y,x1,y2);
      if(mat[w*y+x]==0)
      {
        mat[w*y+x]=(mat[w*y1+x1]+mat[w*y1+x2]+mat[w*y2+x2]+mat[w*y2+x1])/4;
      }
      subdivide(x1,y1,x,y);subdivide(x,y1,x2,y);
      subdivide(x,y,x2,y2);subdivide(x1,y,x,y2);
    }
  }

  public void init()
  {
    // create a color palette (RGBY)
    red=new int[256];green=new int[256];blue=new int[256];
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

    ctm=System.currentTimeMillis();
    inc=(int)(Math.random()*7+1)*((int)(Math.random()*2)*2-1);
    roughness=(float)Math.random()*6+1;
    w=getSize().width;h=getSize().height;
    pix=new int[w*h]; mat=new int[w*h];

    // put random color pixels to the 4 corners
    for(int y=0;y<2;y++)
      for(int x=0;x<2;x++)
        mat[w*y*(h-1)+x*(w-1)]=(int)(Math.random()*256);
    
    subdivide(0,0,w-1,h-1);
  }

  public void paint(Graphics g)
  {
    int c;
    int alpha=255;

    // restart the applet periodically
    if((System.currentTimeMillis()-ctm)>=10000) init();

    // keep the color-cycling speed constant between different PCs!
    long t=System.currentTimeMillis();
    while((System.currentTimeMillis()-t)<10) {;}

    // rotate the colors (the palette)
    for(int y=0;y<h;y++)
      for(int x=0;x<w;x++)
      {
        mat[w*y+x]=(mat[w*y+x]+inc+256)%256; c=mat[w*y+x];
        // convert image data of palette colors to actual image data
        pix[w*y+x]=(alpha<<24)|(red[c]<<16)|(green[c]<<8)|blue[c];
      }

    img=createImage(new MemoryImageSource(w,h,pix,0,w));
    g.drawImage(img,0,0,this);
    repaint();
  }

  public void update(Graphics g) { paint(g); } // no flickering!
}

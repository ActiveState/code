// <applet code="Plasma" width=800 height=600></applet>
// Plasma.java
// FB - 201003254
// Moving plasma fractal
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;
import java.util.Random;

public class Plasma extends Applet
{
  Image img;int pix[],col[];
  int w,h,alpha,ctr;
  float roughness;
  Random rng=new Random();

  public void putpixel(int x,int y,int c) //c:0 to 767
  {
      c=(c%256)<<((int)(c/256)*8) & 16777215;
      pix[w*y+x]=(alpha<<24)|c;
  }

  public int getpixel(int x,int y) //:0 to 767
  {
      int c=pix[w*y+x] & 16777215;
      if(c>65535) c=(c>>16)+512;
      else if(c>255) c=(c>>8)+256;
      return c;
  }

  public void adjust(int xa,int ya,int x,int y,int xb,int yb)
  {
    int c,d;float v;
    if(getpixel(x,y)==0)
    {
      d=(int)(Math.abs(xa-xb)+Math.abs(ya-yb));
      v=(getpixel(xa,ya)+getpixel(xb,yb))/2+(rng.nextFloat()-0.5f)*d*roughness;
      c=((int)Math.abs(v))%768;putpixel(x,y,c);
    }
  }

  public void subdivide(int x1,int y1,int x2,int y2)
  {
    int x,y;float v;
    if(!((x2-x1<2) && (y2-y1<2)))
    {
      x=(int)((x1+x2)/2);y=(int)((y1+y2)/2);
      adjust(x1,y1,x,y1,x2,y1);adjust(x2,y1,x2,y,x2,y2);
      adjust(x1,y2,x,y2,x2,y2);adjust(x1,y1,x1,y,x1,y2);
      if(getpixel(x,y)==0)
      {
        v=(getpixel(x1,y1)+getpixel(x2,y1)+getpixel(x2,y2)+getpixel(x1,y2))/4;
        putpixel(x,y,(int)v);
      }
      subdivide(x1,y1,x,y);subdivide(x,y1,x2,y);
      subdivide(x,y,x2,y2);subdivide(x1,y,x,y2);
    }
  }

  public void init()
  {
    roughness=rng.nextInt(10)+2; ctr=0;
    w=getSize().width;h=getSize().height;
    alpha=255; pix=new int[w*h]; col=new int[h];
    putpixel(0,0,rng.nextInt(768));
    putpixel(w-1,0,rng.nextInt(768));
    putpixel(w-1,h-1,rng.nextInt(768));
    putpixel(0,h-1,rng.nextInt(768));
    subdivide(0,0,w-1,h-1);
    img=createImage(new MemoryImageSource(w,h,pix,0,w));
  }

  public void paint(Graphics g)
  {
    int sh=w/2;
    
    if(ctr==0)
    {
      g.drawImage(img,0,0,this);

      // shift the image data to the left
      for(int x=sh;x<w;x++)
        for(int y=0;y<h;y++)
        {
          pix[w*y+x-sh]=pix[w*y+x];
          if(x>w-1-sh) pix[w*y+x]=0;
        }
      putpixel(w-1,0,rng.nextInt(768));
      putpixel(w-1,h-1,rng.nextInt(768));
      subdivide(0,0,w-1,h-1);
    }
    else
    {
      // shift the graph area 1 pixel to the left
      g.copyArea(1,0,w-1,h,-1,0);
      for(int y=0;y<h;y++) col[y]=pix[w*y+sh+ctr];
      img=createImage(new MemoryImageSource(1,h,col,0,1));
      g.drawImage(img,w-1,0,this);
    }
    ctr++;ctr%=sh;
    // slowdown the sliding speed
    long ctm=System.currentTimeMillis();
    while((System.currentTimeMillis()-ctm)<10) {;}
    repaint();
  }

  public void update(Graphics g) { paint(g); }
}

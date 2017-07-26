// <applet code="Plasma" width=800 height=600></applet>
// FB - 201003254
// Morphing Plasma Fractal
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;

public class Plasma extends Applet
{
  Image img;
  // pix will hold the actual image data
  // mat will hold the 2 image data of palette colors
  int pix[], mat[][];
  int red[],green[],blue[];
  int w,h,scr; // scr: 0 or 1 will show the morph direction between the images
  float roughness;
  int steps;   // number of morph steps between the 2 images
  int ctr;     // counter for steps of morph between the 2 images

  public void adjust(int xa,int ya,int x,int y,int xb,int yb)
  {
    int c,d;
    if(mat[w*y+x][scr]==0)
    {
      d=(int)(Math.abs(xa-xb)+Math.abs(ya-yb));
      c=(mat[w*ya+xa][scr]+mat[w*yb+xb][scr])/2+(int)((Math.random()-0.5)*d*roughness);
      c=((int)Math.abs(c))%256;
      mat[w*y+x][scr]=c;
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
      if(mat[w*y+x][scr]==0)
      {
        mat[w*y+x][scr]=(mat[w*y1+x1][scr]+mat[w*y1+x2][scr]+mat[w*y2+x2][scr]+mat[w*y2+x1][scr])/4;
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

    roughness=(float)Math.random()*2+1;
    w=getSize().width;h=getSize().height;
    pix=new int[w*h]; mat=new int[w*h][2];
    ctr=0;steps=256;
    // create the 2 plasma images
    for(scr=0;scr<2;scr++)
    {
      // put random color pixels to the 4 corners
      for(int y=0;y<2;y++)
        for(int x=0;x<2;x++)
          mat[w*y*(h-1)+x*(w-1)][scr]=(int)(Math.random()*256);
      subdivide(0,0,w-1,h-1);
    }
    scr=0;
  }

  public void paint(Graphics g)
  {
    int a,b,c;
    int alpha=255;

    // keep the speed constant between different PCs!
    long t=System.currentTimeMillis();
    while((System.currentTimeMillis()-t)<5) {;}

    // create a new image between the 2 images
    for(int y=0;y<h;y++)
      for(int x=0;x<w;x++)
      {
        a=mat[w*y+x][scr];
        b=mat[w*y+x][1-scr];
        c=(int)(a+(b-a)*((float)(ctr)/steps));
        // convert image data of palette colors to actual image data
        pix[w*y+x]=(alpha<<24)|(red[c]<<16)|(green[c]<<8)|blue[c];
      }

    ctr+=1; ctr%=steps;
    if(ctr==0)
    { 
      // update (re-calculate) one of the images

      // first clear the old image
      for(int y=0;y<h;y++)
        for(int x=0;x<w;x++)
          mat[w*y+x][scr]=0;

      // put random color pixels to the 4 corners
      for(int y=0;y<2;y++)
        for(int x=0;x<2;x++)
          mat[w*y*(h-1)+x*(w-1)][scr]=(int)(Math.random()*256);
      subdivide(0,0,w-1,h-1); // create the new plasma image
      scr=1-scr; // reverse the morph direction
    }

    img=createImage(new MemoryImageSource(w,h,pix,0,w));
    g.drawImage(img,0,0,this);
    repaint();
  }

  public void update(Graphics g) { paint(g); } // no flickering!
}

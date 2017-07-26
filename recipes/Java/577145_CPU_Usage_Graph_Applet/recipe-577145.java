// <applet code="CPU_usage" width=800 height=600></applet>
// FB - 201003254 
// CPU_usage.java
// The graph will become more and more accurate with time.

import java.applet.Applet;
import java.awt.*;

public class CPU_usage extends Applet
{
    int w,h,red[],green[],blue[];
    int maxctr=0;
  
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

        w=getSize().width;h=getSize().height; // get the applet window size
    }

    public void paint(Graphics g) 
    {
        for(int interval=0;interval<10;interval++)
        {
            // measure the number of loops per time unit (100 ms)
            long ctm=System.currentTimeMillis(); int ctr=0;
            while((System.currentTimeMillis()-ctm)<100) ctr++;
            if(ctr>maxctr) maxctr=ctr;
    
            double bar=(double)(maxctr-ctr)/maxctr;

            // shift the graph area 1 pixel to the left
            g.copyArea(1,0,w-1,h,-1,0);

            int y=(int)(h*bar);

            int col=(int)(bar*255);
            Color cl=new Color(red[col],green[col],blue[col]);
            g.setColor(cl);
            g.drawLine(w-1,0,w-1,y);
            col=(int)((1-bar)*255);
            Color cl2=new Color(red[col],green[col],blue[col]);
            g.setColor(cl2);
            g.drawLine(w-1,y,w-1,h-1);    
        }
        repaint();
    }

    // turn off image clearing each time before repaint to stop the flickering
    // by overriding update() method
    public void update(Graphics g)
    {
        paint(g);
    }
}

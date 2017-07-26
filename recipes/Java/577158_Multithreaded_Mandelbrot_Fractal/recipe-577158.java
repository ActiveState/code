// <applet code="MandelbrotFractal" width=800 height=600></applet>
// MandelbrotFractal.java (FB - 201003276)
// N Multi-threaded!

import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;
import java.lang.Thread;

public class MandelbrotFractal extends Applet
{

    Image img;
    volatile int pix[];    // will be shared by all threads
    int w,h,alpha;
    final int maxThr = 10; // number of threads to run

    // drawing area (must be xa<xb and ya<yb)
    final double xa = -2.0;
    final double xb = 1.0;
    final double ya = -1.5;
    final double yb = 1.5;
    
    public void init()
    {
        w=getSize().width;
        h=getSize().height;
        alpha=255;
        pix=new int[w*h];

        manfr();

        img=createImage(new MemoryImageSource(w,h,pix,0,w));
    }

    public void manfr()
    {
        long startTime = System.currentTimeMillis();
        
        ManFrThread[] m = new ManFrThread[maxThr];
        for(int i=0;i<maxThr;i++)
        {
            m[i]=new ManFrThread(i);
            m[i].start();
        }
        
        // wait until all threads finished
        boolean stop;
        do
        {
            stop=true;
            for(int j=0;j<maxThr;j++)
            {
                if (m[j].isAlive()) 
                {
                    stop=false;
                }
            }
        }while(!stop);
        
        System.out.println("Number of threads: " + maxThr);
        long timeInMillis = System.currentTimeMillis() - startTime;
        System.out.println("Run Time in Millis: " + timeInMillis);
    }

    public void paint(Graphics g)
    {
        g.drawImage(img,0,0,this);
    }

    class ManFrThread extends Thread 
    {
        int k; // id number of this thread
        
        ManFrThread(int k) 
        {
            this.k=k;
        }

        public void run() 
        {
            double x0,x,y,a,b;
            int red,green,blue;
            int i,kx,ky,kc;
            int imax=w*h;

            // Each thread only calculates its own share of pixels!
            for(i=k;i<imax;i+=maxThr)
            {
                kx=i%w;
                ky=(i-kx)/w;
                a=(double)kx/w*(xb-xa)+xa;
                b=(double)ky/h*(yb-ya)+ya;
                x=a;
                y=b;
                
                for(kc=0;kc<256;kc++)
                {
                    x0=x*x-y*y+a;
                    y=2*x*y+b;
                    x=x0;
                    
                    if(x*x+y*y > 4)
                    {
                        // various color palettes can be created here!
                        red=255-(kc%16)*16;
                        green=(16-kc%16)*16;
                        blue=(kc%16)*16;
                        
                        pix[w*ky+kx]=(alpha<<24)|(red<<16)|(green<<8)|blue;
                        break;
                    }
                }
            }
        }
    }
}

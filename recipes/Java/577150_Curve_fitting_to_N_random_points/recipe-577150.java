// <applet code="Curve" width=512 height=512></applet>
// FB 201003265
// Create a curve that passes thru N randomly selected points.
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;
import java.util.Random;

public class Curve extends Applet
{
    Image img;
    int w,h,x,y,pix[],red,green,blue,alpha;
    Random rng=new Random();

    int n=rng.nextInt(10)+5; // n random points
    int[] arx=new int[n];
    int[] ary=new int[n];
    
    public void init()
    {
        w=getSize().width;
        h=getSize().height;
        alpha=255;
        pix=new int[w*h];
        img = createImage(new MemoryImageSource(w, h, pix, 0, w));

        // n random points
        for(int i=0;i<n;i++)
        {
            arx[i]=rng.nextInt(w);
            ary[i]=rng.nextInt(h);
        }

        double wgh;
        int y;
        double sum;
        double sumw;
        boolean flag;

        for(x=0;x<w;x++)
        {
            flag=false;
            sum=0.0;
            sumw=0.0;
            y=0;
            for(int i=0;i<n;i++)
            {
                if(x!=arx[i])
                {
                    //wgh=1.0/Math.pow(Math.abs((double)(x-arx[i])),1.0); // linear
                    wgh=1.0/Math.pow(Math.abs((double)(x-arx[i])),2.0); // quadratic
                    //wgh=1.0/Math.pow(Math.abs((double)(x-arx[i])),3.0); // cubic
                    sumw+=wgh;
                    sum+=(ary[i]*wgh);
                }
                else
                {
                    flag=true;
                    y=ary[i];
                    break;
                }
            }
            if(flag==false)
            {
                y=(int)(sum/sumw);
            }
            
            red=36;
            green=76;
            blue=16;
            pix[w*y+x]=(alpha<<24)|(red<<16)|(green<<8)|blue;

        }
            
        img = createImage(new MemoryImageSource(w, h, pix, 0, w));
    }

    public void paint(Graphics g)
    {
        g.drawImage(img,0,0,this);
        
        // show the n points on the curve
        for(int i=0;i<n;i++)
        {
            g.drawOval(arx[i]-5,ary[i]-5,10,10);
        }

        long ctm=System.currentTimeMillis();
        while((System.currentTimeMillis()-ctm)<3000) {;}
        init();
    }
}

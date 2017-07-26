// <applet code="GravitySim" width=800 height=600></applet>
// GravitySim.java (200810094) FB
import java.applet.Applet;
import java.awt.*;
import java.awt.image.*;

public class GravitySim extends Applet 
{
    Image img;
    int wd,ht,pix[],alpha;

    public void init()
    {
        wd=getSize().width;ht=getSize().height;alpha=255;
        pix=new int[wd*ht];
        gr();
        img=createImage(new MemoryImageSource(wd,ht,pix,0,wd));
    }

    public void paint(Graphics g)
    {
        g.drawImage(img,0,0,this);

        // Refresh Periodically
        long t=System.currentTimeMillis();
        while((System.currentTimeMillis()-t)<5000) {;}

        // delete the old graph
        for(int i=0;i<wd*ht;++i) pix[i]=0;
        gr();
        img=createImage(new MemoryImageSource(wd,ht,pix,0,wd));
        repaint();
    }
/*
    public void update(Graphics g) // to stop refresh flickering
    {
        paint(g);
    }
*/
    public void gr()
    {
        // number of gravity sources
        int n = (int)(Math.random() * 5)+2;

        boolean fl;
        double G = 1.0; // general gravity constant
        double h = 0.0025; // time step (real solution; lim h->0)
        double dmin = 40.0; // min allowed distance between objects
        int mx, my, k, j;mx = wd-1;my = ht-1;
        double ang, v, dx, dy, d, a, ax, ay;
        double x[], y[], xnew[], ynew[], m[], vx[], vy[];
        int rd[], gr[], bl[];
        m=new double[n];x=new double[n];y=new double[n];
        xnew=new double[n];ynew=new double[n];
        vx=new double[n];vy=new double[n];
        rd=new int[n];gr=new int[n];bl=new int[n];
        double Sx, Sy, Svx, Svy, Sm;
        Sx = Sy = Svx = Svy = Sm = 0;
        
        for(k=0;k<n;++k)
        {
            x[k] = (double)((Math.random()*2-1) * mx/8+mx/2);
            y[k] = (double)((Math.random()*2-1) * my/8+my/2);
            m[k] = (double)(Math.random() * 30) + 10;
            m[k] = (m[k]*m[k]*m[k])*10;
            ang = (double)(Math.random() * 2 * Math.PI); 
            v = (double)(Math.random() * 200);
            vx[k] = (double)(v * Math.cos(ang));
            vy[k] = (double)(v * Math.sin(ang));
            rd[k] = (int)(Math.random() * 256);
            gr[k] = (int)(Math.random() * 256);
            bl[k] = (int)(Math.random() * 256);
            
			Sx      = Sx  + m[k] * x[k];
			Sy      = Sy  + m[k] * y[k];
			Svx     = Svx + m[k] * vx[k];
			Svy     = Svy + m[k] * vy[k];
			Sm      = Sm  + m[k];
            
        }

		for (k = 0; k < n; k++) 
        {
			x[k]    = x[k]  - (Sx  / Sm) + (mx  / 2.0);
			y[k]    = y[k]  - (Sy  / Sm) + (my / 2.0);
			vx[k]   = vx[k] - (Svx / Sm);
			vy[k]   = vy[k] - (Svy / Sm);
		}
        
        //
        do
        {
            fl=false;
            for(k=0;k<n;++k)
            {
                ax = 0; ay = 0;
                for(j=0;j<n;++j)
                {
                    if(k!=j)
                    {
                        dx = x[j] - x[k]; dy = y[j] - y[k];
                        d = (double)Math.sqrt(dx * dx + dy * dy);
                        d = Math.max(dmin, d);
                        dx = dx / d; dy = dy / d;
                        a = G * m[j] / (d * d);
                        ax = ax + a * dx; ay = ay + a * dy;
                    }
                }
                xnew[k] = x[k] + vx[k] * h;
                ynew[k] = y[k] + vy[k] * h;
                vx[k] = vx[k] + ax * h; vy[k] = vy[k] + ay * h;
            }
            for(k=0;k<n;++k)
            {
                x[k] = xnew[k]; y[k] = ynew[k];
                if(!(x[k]<0 || x[k]>mx || y[k]<0 || y[k]>my))
                {
                    pix[wd*(int)y[k]+(int)x[k]]=(alpha<<24)|(rd[k]<<16)|(gr[k]<<8)|bl[k];
                    fl=true;
                }
            }
        }
        while(fl);
    }
}

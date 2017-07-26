import ij

class Inverter_py(ij.plugin.filter.PlugInFilter):
    def setup(self,arg, imp):
        """@sig public int setup(String arg, ij.ImagePlus imp)"""
        return ij.plugin.filter.PlugInFilter.DOES_8G

    def run(self,ip):
        """@sig public void run(ij.process.ImageProcessor ip)"""
        pixels = ip.getPixels()
        width = ip.getWidth()
        r = ip.getRoi()
        for y in range(r.y,r.y+r.height):
            for x in range(r.x,r.x+r.width):
                i = y*width + x;
                pixels[i] = 255-pixels[i]

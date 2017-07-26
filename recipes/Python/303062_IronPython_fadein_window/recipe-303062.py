from System.Windows.Forms import *
from System.Drawing import *
from System.Drawing.Imaging import *

form = Form(Text="Window Fade-ins with IronPython",
         HelpButton=False,
         MinimizeBox=True, MaximizeBox=True,
         WindowState=FormWindowState.Maximized,
         FormBorderStyle = FormBorderStyle.Sizable,
         StartPosition = FormStartPosition.CenterScreen,
         Opacity = 0)

# create a checker background pattern image
box_size = 25
image = Bitmap(box_size * 2, box_size * 2)
graphics = Graphics.FromImage(image);
graphics.FillRectangle(Brushes.Black, 0, 0, box_size, box_size);
graphics.FillRectangle(Brushes.White, box_size, 0, box_size, 50);
graphics.FillRectangle(Brushes.White, 0, box_size,box_size, box_size);
graphics.FillRectangle(Brushes.Black, box_size, box_size, box_size, box_size);
form.BackgroundImage = image

# create a control to allow the opacity to be adjusted
opacity_tracker = TrackBar(Text="Transparency",
              Height = 20,
              Dock = DockStyle.Bottom,
              Minimum = 0, Maximum = 100, Value = 0,
              TickFrequency = 10,
              Enabled = False)

def track_opacity_change(sender, event):
    form.Opacity = opacity_tracker.Value / 100.0
opacity_tracker.ValueChanged += track_opacity_change

form.Controls.Add(opacity_tracker)

# create a timer to animate the initial appearance of the window
timer = Timer()
timer.Interval = 15

def tick(sender, event):
    val = opacity_tracker.Value + 1
    if val >= opacity_tracker.Maximum:
        # ok, we're done, set the opacity to maximum, stop the 
        # animation, and let the user play with the opacity manually
        opacity_tracker.Value = opacity_tracker.Maximum
        opacity_tracker.Minimum = 20 # don't let the user hurt themselves
        opacity_tracker.Enabled = True

        timer.Stop()
    else:
        opacity_tracker.Value = val
        
timer.Tick += tick
timer.Start()

form.ShowDialog()

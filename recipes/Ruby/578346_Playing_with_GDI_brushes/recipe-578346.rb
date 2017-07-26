require 'mscorlib'
require 'System.Drawing, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'
require 'System.Windows.Forms, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'

Application         = System::Windows::Forms::Application
BorderStyle         = System::Windows::Forms::BorderStyle
Bitmap              = System::Drawing::Bitmap
Button              = System::Windows::Forms::Button
Color               = System::Drawing::Color
ColorDialog         = System::Windows::Forms::ColorDialog
ComboBox            = System::Windows::Forms::ComboBox
Convert             = System::Convert
Decimal             = System::Decimal
DialogResult        = System::Windows::Forms::DialogResult
Enum                = System::Enum
EventArgs           = System::EventArgs
Font                = System::Drawing::Font
FontStyle           = System::Drawing::FontStyle
Form                = System::Windows::Forms::Form
FormBorderStyle     = System::Windows::Forms::FormBorderStyle
FormStartPosition   = System::Windows::Forms::FormStartPosition
HatchBrush          = System::Drawing::Drawing2D::HatchBrush
HatchStyle          = System::Drawing::Drawing2D::HatchStyle
Icon                = System::Drawing::Icon
Label               = System::Windows::Forms::Label
LinearGradientBrush = System::Drawing::Drawing2D::LinearGradientBrush
LinearGradientMode  = System::Drawing::Drawing2D::LinearGradientMode
MainMenu            = System::Windows::Forms::MainMenu
MenuItem            = System::Windows::Forms::MenuItem
MessageBox          = System::Windows::Forms::MessageBox
MessageBoxButtons   = System::Windows::Forms::MessageBoxButtons
MessageBoxIcon      = System::Windows::Forms::MessageBoxIcon
NumericUpDown       = System::Windows::Forms::NumericUpDown
PathGradientBrush   = System::Drawing::Drawing2D::PathGradientBrush
Pen                 = System::Drawing::Pen
PictureBox          = System::Windows::Forms::PictureBox
PictureBoxSizeMode  = System::Windows::Forms::PictureBoxSizeMode
Point               = System::Drawing::Point
Rectangle           = System::Drawing::Rectangle
Size                = System::Drawing::Size
Shortcut            = System::Windows::Forms::Shortcut
SolidBrush          = System::Drawing::SolidBrush
StatusBar           = System::Windows::Forms::StatusBar
TextBox             = System::Windows::Forms::TextBox
TextureBrush        = System::Drawing::TextureBrush
WrapMode            = System::Drawing::Drawing2D::WrapMode

class Frm < Form
  def initialize
    #for texture brush only
    @pic = Bitmap.new('D:\source\Clouds.jpg')
    #for other brushes
    @col1 = Color.Blue
    @col2 = Color.White
    #initialization
    self.InitializeComponent()
  end

  def InitializeComponent()
    @mnuMain = MainMenu.new()
    @mnuFile = MenuItem.new()
    @mnuExit = MenuItem.new()
    @mnuHelp = MenuItem.new()
    @mnuInfo = MenuItem.new()
    @lblLabel0 = Label.new()
    @lblLabel1 = Label.new()
    @lblLabel2 = Label.new()
    @lblLabel3 = Label.new()
    @lblLabel4 = Label.new()
    @lblLabel5 = Label.new()
    @lblLabel6 = Label.new()
    @lblLabel7 = Label.new()
    @lblLabel8 = Label.new()
    @lblLabel9 = Label.new()
    @cboBrushType = ComboBox.new()
    @cboDrawing = ComboBox.new()
    @txtColor1 = TextBox.new()
    @txtColor2 = TextBox.new()
    @btnColor1 = Button.new()
    @btnColor2 = Button.new()
    @cboBrushSize = ComboBox.new()
    @cboWrapMode = ComboBox.new()
    @cboHatchStyle = ComboBox.new()
    @nudRotation = NumericUpDown.new()
    @nudGradBlend = NumericUpDown.new()
    @cboGradMode = ComboBox.new()
    @picDemoArea = PictureBox.new()
    @sbStatusBar = StatusBar.new()
    @cdlg = ColorDialog.new()
    #
    #mnuMain
    #
    [@mnuFile, @mnuHelp].each {|item| @mnuMain.MenuItems.Add item}
    #
    #mnuFile
    #
    @mnuFile.MenuItems.Add @mnuExit
    @mnuFile.Text = '&File'
    #
    #mnuExit
    #
    @mnuExit.Shortcut = Shortcut.CtrlX
    @mnuExit.Text = 'E&xit'
    @mnuExit.Click {|sender, e| mnuExit_Click(sender, e)}
    #
    #mnuHelp
    #
    @mnuHelp.MenuItems.Add @mnuInfo
    @mnuHelp.Text = '&Help'
    #
    #mnuInfo
    #
    @mnuInfo.Text = 'About'
    @mnuInfo.Click {|sender, e| mnuInfo_Click(sender, e)}
    #
    #lblLabel0
    #
    @lblLabel0.Location = Point.new(8, 16)
    @lblLabel0.Size = Size.new(96, 23)
    @lblLabel0.Text = 'Brush Type:'
    #
    #lblLabel1
    #
    @lblLabel1.Location = Point.new(8, 40)
    @lblLabel1.Size = Size.new(96, 23)
    @lblLabel1.Text = 'Drawing:'
    #
    #lblLabel2
    #
    @lblLabel2.Location = Point.new(8, 80)
    @lblLabel2.Size = Size.new(96, 23)
    @lblLabel2.Text = 'Color 1:'
    #
    #lblLabel3
    #
    @lblLabel3.Location = Point.new(8, 104)
    @lblLabel3.Size = Size.new(96, 23)
    @lblLabel3.Text = 'Color 2:'
    #
    #lblLabel4
    #
    @lblLabel4.Location = Point.new(8, 152)
    @lblLabel4.Size = Size.new(96, 23)
    @lblLabel4.Text = 'Brush Size:'
    #
    #lblLabel5
    #
    @lblLabel5.Location = Point.new(8, 184)
    @lblLabel5.Size = Size.new(96, 23)
    @lblLabel5.Text = 'Wrap Mode:'
    #
    #lblLabel6
    #
    @lblLabel6.Location = Point.new(8, 216)
    @lblLabel6.Size = Size.new(96, 23)
    @lblLabel6.Text = 'Hatch Style:'
    #
    #lblLabel7
    #
    @lblLabel7.Location = Point.new(8, 248)
    @lblLabel7.Size = Size.new(96, 23)
    @lblLabel7.Text = 'Rotation:'
    #
    #lblLabel8
    #
    @lblLabel8.Location = Point.new(8, 280)
    @lblLabel8.Size = Size.new(104, 23)
    @lblLabel8.Text = 'Gradient Blend:'
    #
    #lblLabel9
    #
    @lblLabel9.Location = Point.new(8, 312)
    @lblLabel9.Size = Size.new(104, 23)
    @lblLabel9.Text = 'Gradient Mode:'
    #
    #cboBrushType
    #
    ['Solid', 'Hatch', 'Texture', 'LinearGradient',
     'PathGradient'].each {|item| @cboBrushType.Items.Add item}
    @cboBrushType.Location = Point.new(112, 13)
    @cboBrushType.Size = Size.new(176, 24)
    @cboBrushType.SelectedItem = 'Solid'
    @cboBrushType.SelectedIndexChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #cboDrawing
    #
    ['Fill', 'Ellipses', 'Lines'].each {|item| @cboDrawing.Items.Add item}
    @cboDrawing.Location = Point.new(112, 40)
    @cboDrawing.Size = Size.new(176, 24)
    @cboDrawing.SelectedItem = 'Fill'
    @cboDrawing.SelectedIndexChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #txtColor1
    #
    @txtColor1.BackColor = @col1
    @txtColor1.Location = Point.new(112, 77)
    @txtColor1.Size = Size.new(144, 23)
    @txtColor1.Text = 'Color [Blue]'
    @txtColor1.TextChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #txtColor2
    #
    @txtColor2.BackColor = @col2
    @txtColor2.Location = Point.new(112, 104)
    @txtColor2.Size = Size.new(144, 23)
    @txtColor2.Text = 'Color [White]'
    @txtColor2.TextChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #btnColor1
    #
    @btnColor1.Location = Point.new(256, 76)
    @btnColor1.Size = Size.new(32, 25)
    @btnColor1.Text = '...'
    @btnColor1.Click {|sender, e| btnColor1_Click(sender, e)}
    #
    #btnColor2
    #
    @btnColor2.Location = Point.new(256, 103)
    @btnColor2.Size = Size.new(32, 25)
    @btnColor2.Text = '...'
    @btnColor2.Click {|sender, e| btnColor2_Click(sender, e)}
    #
    #cboBrushSize
    #
    ['Large', 'Medium', 'Small'].each {|item| @cboBrushSize.Items.Add item}
    @cboBrushSize.Location = Point.new(112, 149)
    @cboBrushSize.Size = Size.new(176, 24)
    @cboBrushSize.SelectedItem = 'Large'
    @cboBrushSize.SelectedIndexChanged {|sender, e| cboBrushSize_SelectedIndexChanged(sender, e)}
    #
    #cboWrapMode
    #
    @cboWrapMode.Location = Point.new(112, 181)
    @cboWrapMode.Size = Size.new(176, 24)
    @cboWrapMode.SelectedIndexChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #cboHatchStyle
    #
    @cboHatchStyle.Location = Point.new(112, 213)
    @cboHatchStyle.Size = Size.new(176, 24)
    @cboHatchStyle.SelectedIndexChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #nudRotation
    #
    @nudRotation.Increment = Decimal.new(5)
    @nudRotation.Location = Point.new(112, 245)
    @nudRotation.Maximum = Decimal.new(180)
    @nudRotation.Size = Size.new(176, 23)
    @nudRotation.ValueChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #nudGradBlend
    #
    @nudGradBlend.DecimalPlaces = 2
    @nudGradBlend.Increment = Decimal.new(0.10)
    @nudGradBlend.Location = Point.new(112, 277)
    @nudGradBlend.Maximum = Decimal.new(1)
    @nudGradBlend.Size = Size.new(176, 23)
    @nudGradBlend.Value = Decimal.new(1)
    @nudGradBlend.ValueChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #cboGradMode
    #
    @cboGradMode.Location = Point.new(112, 309)
    @cboGradMode.Size = Size.new(176, 24)
    @cboGradMode.SelectedIndexChanged {|sender, e| RedrawPicture(sender, e)}
    #
    #picDemoArea
    #
    @picDemoArea.BorderStyle = BorderStyle.FixedSingle
    @picDemoArea.Location = Point.new(304, 16)
    @picDemoArea.Size = Size.new(312, 320)
    #
    #sbStatusBar
    #
    @sbStatusBar.SizingGrip = false
    #
    #Frm
    #
    self.ClientSize = Size.new(626, 371)
    [@lblLabel0, @lblLabel1, @lblLabel2, @lblLabel3, @lblLabel4, @lblLabel5,
     @lblLabel6, @lblLabel7, @lblLabel8, @lblLabel9, @cboBrushType, @cboDrawing,
     @txtColor1, @txtColor2, @btnColor1, @btnColor2, @cboBrushSize, @cboWrapMode,
     @cboHatchStyle, @nudRotation, @nudGradBlend, @cboGradMode, @picDemoArea,
     @sbStatusBar].each {|item| self.Controls.Add item}
    self.Font = Font.new('Microsoft Sans Serif', 10)
    self.FormBorderStyle = FormBorderStyle.FixedSingle
    self.MaximizeBox = false
    self.Menu = @mnuMain
    self.StartPosition = FormStartPosition.CenterScreen
    self.Text = 'Brushes'
    self.Load {|sender, e| frmMain_Load(sender, e)}
  end

  def mnuExit_Click(sender, e)
    Application.exit
  end

  def mnuInfo_Click(sender, e)
    FrmA.new().ShowDialog()
  end

  def btnColor1_Click(sender, e)
    if @cdlg.ShowDialog() == DialogResult.OK
      @col1 = @cdlg.Color
      @txtColor1.Text = @cdlg.Color.to_s
      @txtColor1.BackColor = @cdlg.Color
    end
  end

  def btnColor2_Click(sender, e)
    if @cdlg.ShowDialog() == DialogResult.OK
      @col2 = @cdlg.Color
      @txtColor2.Text = @cdlg.Color.to_s
      @txtColor2.BackColor = @cdlg.Color
    end
  end

  def cboBrushSize_SelectedIndexChanged(sender, e)
    case @cboBrushSize.Text
      when 'Large'
        @rec = Rectangle.new(0, 0, @picDemoArea.Width, @picDemoArea.Height)
      when 'Medium'
        @rec = Rectangle.new(0, 0, @picDemoArea.Width / 2, @picDemoArea.Height / 2)
      when 'Small'
        @rec = Rectangle.new(0, 0, @picDemoArea.Width / 4, @picDemoArea.Height / 4)
    end
    RedrawPicture(@cboBrushSize, EventArgs.new())
  end

  def RedrawPicture(sender, e)
    @picDemoArea.CreateGraphics().Clear(@col2)
    @picDemoArea.Refresh()

    #brush selector
    case @cboBrushType.Text
      when 'Solid'
        @txtColor2.Enabled = false
        @btnColor2.Enabled = false
        @cboBrushSize.Enabled = false
        @cboWrapMode.Enabled = false
        @cboHatchStyle.Enabled = false
        @nudRotation.Enabled = false
        @nudGradBlend.Enabled = false
        @cboGradMode.Enabled = false
        @brush = SolidBrush.new(@col1)
      when 'Hatch'
        @sbStatusBar.Text = ''
        @txtColor1.Enabled = true
        @txtColor2.Enabled = true
        @btnColor1.Enabled = true
        @btnColor2.Enabled = true
        @cboBrushSize.Enabled = false
        @cboWrapMode.Enabled = false
        @cboHatchStyle.Enabled = true
        @nudRotation.Enabled = false
        @nudGradBlend.Enabled = false
        @cboGradMode.Enabled = false
        @brush = HatchBrush.new(@cboHatchStyle.SelectedItem, @col1, @col2)
      when 'Texture'
        @txtColor1.Enabled = false
        @txtColor2.Enabled = false
        @btnColor1.Enabled = false
        @btnColor2.Enabled = false
        @cboBrushSize.Enabled = true
        @cboWrapMode.Enabled = true
        @cboHatchStyle.Enabled = false
        @nudRotation.Enabled = true
        @nudGradBlend.Enabled = false
        @cboGradMode.Enabled = false
        begin
          tb = TextureBrush.new(@pic, @rec)
          tb.WrapMode = @cboWrapMode.SelectedItem
          tb.RotateTransform(Convert.ToSingle(@nudRotation.Value))
          @brush = tb
        rescue Exception => e
          @sbStatusBar.Text = e.Message
        end
      when 'LinearGradient'
        @sbStatusBar.Text = ''
        @txtColor1.Enabled = true
        @txtColor2.Enabled = true
        @btnColor1.Enabled = true
        @btnColor2.Enabled = true
        @cboBrushSize.Enabled = true
        @cboWrapMode.Enabled = false
        @cboHatchStyle.Enabled = false
        @nudGradBlend.Enabled = true
        @cboGradMode.Enabled = true
        lgb = LinearGradientBrush.new(@rec, @col1, @col2, @cboGradMode.SelectedItem)
        lgb.RotateTransform(Convert.ToSingle(@nudRotation.Value))
        lgb.SetBlendTriangularShape(Convert.ToSingle(@nudGradBlend.Value))
        @brush = lgb
      when 'PathGradient'
        @cboWrapMode.Enabled = true
        @cboGradMode.Enabled = false
        points = System::Array[Point].new([Point.new(0, @rec.Height),
                                           Point.new(@rec.Width, @rec.Height),
                                           Point.new(@rec.Width, 0)])
        pgb = PathGradientBrush.new(points)
        pgb.CenterColor = @col1
        pgb.SurroundColors = System::Array[Color].new([@col2])
        pgb.WrapMode = @cboWrapMode.SelectedItem
        pgb.RotateTransform(Convert.ToSingle(@nudRotation.Value))
        pgb.SetBlendTriangularShape(Convert.ToSingle(@nudGradBlend.Value))
        @brush = pgb
    end

    #drawing images
    gfx = @picDemoArea.CreateGraphics()

    case @cboDrawing.Text
      when 'Fill'
        gfx.FillRectangle(@brush, 0, 0, @picDemoArea.Width, @picDemoArea.Height)
      when 'Ellipses'
        gfx.FillEllipse(@brush, @picDemoArea.Width / 10, @picDemoArea.Height / 10,
                                  @picDemoArea.Width / 2, @picDemoArea.Height / 2)
        gfx.FillEllipse(@brush, @picDemoArea.Width / 3, @picDemoArea.Height / 3,
                                @picDemoArea.Width / 2, @picDemoArea.Height / 2)
      when 'Lines'
        pen = Pen.new(@brush, 40)
        gfx.DrawLine(pen, 0, 0, @picDemoArea.Width, @picDemoArea.Height)
        gfx.DrawLine(pen, 0, 0, 0, @picDemoArea.Height)
        gfx.DrawLine(pen, 0, 0, @picDemoArea.Width, 0)
        gfx.DrawLine(pen, @picDemoArea.Width, 0, @picDemoArea.Width, @picDemoArea.Height)
        gfx.DrawLine(pen, 0, @picDemoArea.Height, @picDemoArea.Width, @picDemoArea.Height)
        gfx.DrawLine(pen, @picDemoArea.Width, 0, 0, @picDemoArea.Height)
    end
  end

  def frmMain_Load(sender, e)
    @rec = Rectangle.new(0, 0, @picDemoArea.Width, @picDemoArea.Height)
    #cboWrapMode filling
    Enum.GetValues(WrapMode.to_clr_type).each {|i| @cboWrapMode.Items.Add i}
    @cboWrapMode.SelectedIndex = 0
    #cboHatchStyle filling
    Enum.GetValues(HatchStyle.to_clr_type).each {|i| @cboHatchStyle.Items.Add i}
    @cboHatchStyle.SelectedIndex = 0
    #cboGradMode filling
    Enum.GetValues(LinearGradientMode.to_clr_type).each {|i| @cboGradMode.Items.Add i}
    @cboGradMode.SelectedIndex = 0
  end
end

class FrmA < Form
  def initialize
    self.InitializeComponent()
  end

  def InitializeComponent()
    @pbImage = PictureBox.new()
    @lblName = Label.new()
    @lblCopy = Label.new()
    @btnExit = Button.new()
    #
    #pbImage
    #
    @pbImage.Location = Point.new(16, 16)
    @pbImage.Size = Size.new(32, 32)
    @pbImage.SizeMode = PictureBoxSizeMode.StretchImage
    #
    #lblName
    #
    @lblName.Font = Font.new('Microsoft Sans Serif', 9, FontStyle.Bold)
    @lblName.Location = Point.new(53, 19)
    @lblName.Size = Size.new(360, 18)
    @lblName.Text = 'Brushes v1.00'
    #
    #lblCopy
    #
    @lblCopy.Location = Point.new(55, 37)
    @lblCopy.Size = Size.new(360, 23)
    @lblCopy.Text = '(C) 2012 Grigori Zakharov gregzakh@gmail.com'
    #
    #btnExit
    #
    @btnExit.Location = Point.new(135, 67)
    @btnExit.Text = 'OK'
    #
    #FrmA
    #
    self.AcceptButton = @btnExit
    self.CancelButton = @btnExit
    self.ClientSize = Size.new(350, 110)
    [@pbImage, @lblName, @lblCopy, @btnExit].each {|item| self.Controls.Add item}
    self.ControlBox = false
    self.FormBorderStyle = FormBorderStyle.FixedSingle
    self.ShowInTaskbar = false
    self.StartPosition = FormStartPosition.CenterParent
    self.Text = 'About...'
    self.Load {|sender, e| frmAbout_Load(sender, e)}
  end

  def frmAbout_Load(sender, e)
    begin
      icon = Icon
      @pbImage.Image = self.icon.ToBitmap()
    rescue Exception => e
      MessageBox.Show(e.Message, self.Text, MessageBoxButtons.OK, MessageBoxIcon.Stop)
    end
  end
end

Application.enable_visual_styles
Application.run Frm.new()

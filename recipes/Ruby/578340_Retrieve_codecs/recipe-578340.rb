require 'mscorlib'
require 'System.Drawing, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'
require 'System.Windows.Forms, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'

Application        = System::Windows::Forms::Application
Button             = System::Windows::Forms::Button
ColumnHeader       = System::Windows::Forms::ColumnHeader
DockStyle          = System::Windows::Forms::DockStyle
Font               = System::Drawing::Font
FontStyle          = System::Drawing::FontStyle
Form               = System::Windows::Forms::Form
FormBorderStyle    = System::Windows::Forms::FormBorderStyle
FormStartPosition  = System::Windows::Forms::FormStartPosition
Icon               = System::Drawing::Icon
Label              = System::Windows::Forms::Label
ListView           = System::Windows::Forms::ListView
MainMenu           = System::Windows::Forms::MainMenu
MenuItem           = System::Windows::Forms::MenuItem
MessageBox         = System::Windows::Forms::MessageBox
MessageBoxBittons  = System::Windows::Forms::MessageBoxButtons
MessageBoxIcon     = System::Windows::Forms::MessageBoxIcon
PictureBox         = System::Windows::Forms::PictureBox
PictureBoxSizeMode = System::Windows::Forms::PictureBoxSizeMode
Point              = System::Drawing::Point
Registry           = Microsoft::Win32::Registry
Shortcut           = System::Windows::Forms::Shortcut
Size               = System::Drawing::Size
SortOrder          = System::Windows::Forms::SortOrder
StatusBar          = System::Windows::Forms::StatusBar
View               = System::Windows::Forms::View

class Frm < Form
  def initialize
    #this path keeps codecs CLSIDs and names
    @reg = 'CLSID\{083863F1-70DE-11d0-BD40-00A0C911CE86}\Instance'
    self.InitializeComponent()
  end

  def InitializeComponent()
    @mnuMain = MainMenu.new()
    @mnuFile = MenuItem.new()
    @mnuScan = MenuItem.new()
    @mnuExit = MenuItem.new()
    @mnuView = MenuItem.new()
    @mnuSBar = MenuItem.new()
    @mnuHelp = MenuItem.new()
    @mnuInfo = MenuItem.new()
    @lvCodec = ListView.new()
    @chNames = ColumnHeader.new()
    @chClsid = ColumnHeader.new()
    @chItems = ColumnHeader.new()
    @sbCount = StatusBar.new()
    #
    #mnuMain
    #
    [@mnuFile, @mnuView, @mnuHelp].each {|item| @mnuMain.MenuItems.Add item}
    #
    #mnuFile
    #
    [@mnuScan, @mnuExit].each {|item| @mnuFile.MenuItems.Add item}
    @mnuFile.Text = '&File'
    #
    #mnuScan
    #
    @mnuScan.Shortcut = Shortcut.F5
    @mnuScan.Text = '&Scan...'
    @mnuScan.Click {|sender, e| mnuScan_Click(sender, e)}
    #
    #mnuExit
    #
    @mnuExit.Shortcut = Shortcut.CtrlX
    @mnuExit.Text = 'E&xit'
    @mnuExit.Click {|sender, e| mnuExit_Click(sender, e)}
    #
    #mnuView
    #
    @mnuView.MenuItems.Add @mnuSBar
    @mnuView.Text = '&View'
    #
    #mnuSBar
    #
    @mnuSBar.Checked = true
    @mnuSBar.Text = '&Show Status Bar'
    @mnuSBar.Click {|sender, e| mnuSBar_Click(sender, e)}
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
    #lvCodec
    #
    @lvCodec.AllowColumnReorder = true
    [@chNames, @chClsid, @chItems].each {|item| @lvCodec.Columns.Add item}
    @lvCodec.Dock = DockStyle.Fill
    @lvCodec.FullRowSelect = true
    @lvCodec.GridLines = true
    @lvCodec.MultiSelect = false
    @lvCodec.Sorting = SortOrder.Ascending
    @lvCodec.View = View.Details
    #
    #chNames
    #
    @chNames.Text = 'Name'
    @chNames.Width = 183
    #
    #chClsid
    #
    @chClsid.Text = 'CLSID'
    @chClsid.Width = 239
    #
    #chItems
    #
    @chItems.Text = 'Module'
    @chItems.Width = 250
    #
    #sbCount
    #
    @sbCount.SizingGrip = false
    #
    #Frm
    #
    self.ClientSize = Size.new(573, 217)
    [@lvCodec, @sbCount].each {|item| self.Controls.Add item}
    self.Menu = @mnuMain
    self.StartPosition = FormStartPosition.CenterScreen
    self.Text = 'Codecs'
    self.Load {|sender, e| frmMain_Load(sender, e)}
  end

  def mnuScan_Click(sender, e)
    #clear before each scanning
    @lvCodec.Items.Clear()
    #loading info
    rk = Registry.ClassesRoot
    rk.OpenSubKey(@reg).GetSubKeyNames().each do |sub|
      #name(s) of codec(s)
      item = @lvCodec.Items.Add(rk.OpenSubKey(@reg + '\\' + sub).GetValue('FriendlyName'))
      #CLSID
      item.SubItems.Add(sub)
      #looking for module(s) of codec(s)
      item.SubItems.Add(rk.OpenSubKey('CLSID\\' + sub + '\\InprocServer32').GetValue(''))
    end
    #totaly
    @sbCount.Text = @lvCodec.Items.Count.ToString() + ' item(s)'
  end

  def mnuExit_Click(sender, e)
    Application.exit
  end

  def mnuSBar_Click(sender, e)
    bln =! @mnuSBar.Checked
    @mnuSBar.Checked = bln
    @sbCount.Visible = bln
  end

  def mnuInfo_Click(sender, e)
    FrmA.new().ShowDialog()
  end

  def frmMain_Load(sender, e)
    @sbCount.Text = '0 item(s)'
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
    @lblName.Text = 'Codecs v1.00'
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

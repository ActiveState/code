#-- dndtester.glade --

<?xml version="1.0" standalone="no"?> <!--*- mode: xml -*-->
<!DOCTYPE glade-interface SYSTEM "http://glade.gnome.org/glade-2.0.dtd">

<glade-interface>

<widget class="GtkWindow" id="DNDTester">
  <property name="visible">True</property>
  <property name="title" translatable="yes">D'N'D Tester</property>
  <property name="type">GTK_WINDOW_TOPLEVEL</property>
  <property name="window_position">GTK_WIN_POS_NONE</property>
  <property name="modal">False</property>
  <property name="resizable">True</property>
  <property name="destroy_with_parent">False</property>
  <property name="decorated">True</property>
  <property name="skip_taskbar_hint">False</property>
  <property name="skip_pager_hint">False</property>
  <property name="type_hint">GDK_WINDOW_TYPE_HINT_NORMAL</property>
  <property name="gravity">GDK_GRAVITY_NORTH_WEST</property>
  <signal name="destroy" handler="on_dndtester_destroy" />

  <child>
    <widget class="GtkScrolledWindow" id="scrolledwindow1">
      <property name="visible">True</property>
      <property name="can_focus">True</property>
      <property name="hscrollbar_policy">GTK_POLICY_ALWAYS</property>
      <property name="vscrollbar_policy">GTK_POLICY_ALWAYS</property>
      <property name="shadow_type">GTK_SHADOW_IN</property>
      <property name="window_placement">GTK_CORNER_TOP_LEFT</property>

      <child>
	    <widget class="GtkTextView" id="log">
	      <property name="visible">True</property>
	      <property name="can_focus">True</property>
	      <property name="editable">True</property>
	      <property name="overwrite">False</property>
	      <property name="accepts_tab">True</property>
	      <property name="justification">GTK_JUSTIFY_LEFT</property>
	      <property name="wrap_mode">GTK_WRAP_NONE</property>
	      <property name="cursor_visible">True</property>
	      <property name="pixels_above_lines">0</property>
	      <property name="pixels_below_lines">0</property>
	      <property name="pixels_inside_wrap">0</property>
	      <property name="left_margin">0</property>
	      <property name="right_margin">0</property>
	      <property name="indent">0</property>
	      <property name="text" translatable="yes"></property>
	      <signal name="drag_data_received" handler="on_log_drag_data_received"/>
	    </widget>
      </child>
    </widget>
  </child>
</widget>
</glade-interface>

#-- / dndtester.glade --

# dndtester.py

import pygtk
pygtk.require("2.0")

import gtk
import gtk.glade

class DNDTester(object):
    def __init__(self):
        filename = 'dndtester.glade'
        windowname = 'DNDTester'
        self.wTree = gtk.glade.XML(filename, windowname)
        self.log_buffer = gtk.TextBuffer()
        self.setupWidgets()
        
    def setupWidgets(self):
        HANDLERS_AND_METHODS = {
            "on_dndtester_destroy": self.destroy,
            "on_drag_data_received": self.on_log_drag_data_received
            }

        log = self.wTree.get_widget("log")
        log.set_buffer(self.log_buffer)
        self.wTree.signal_autoconnect(HANDLERS_AND_METHODS)

    def on_log_drag_data_received(self, data):
        self.log_buffer.insert_at_cursor(data+'\n', len(data))

    def destroy(self, data):
        gtk.mainquit()

if __name__ == "__main__":
    app = DNDTester()
    gtk.mainloop()

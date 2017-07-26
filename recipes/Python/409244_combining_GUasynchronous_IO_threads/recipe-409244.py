#!/usr/bin/python
import gtk
import gtk.glade
import sys   
import threading
import Queue
import time
import random


class aJob:
    """this is a container for jobs"""

    def __init__(self,id,label):
        """
          instance variables:
          id: a unique job id
          label: a label (url to fect, file to read, whatever)
          result: this will store the result (content of the file, whatever)
        """
        self.id=id
        self.label=label
        self.result=None
    

class GuiPart:
    """ this is the gui class, that is called in the main thread"""

    def __init__(self,qIn,qOut):
        """
        qIn in a Queue.Queue that store jobs to be done
        qOut is a Queue.Queue that store result of completed jobs
        The GuiPart is supposed to push stuff in qIn ,and regularly check
        if new result are available in qOut
        """
        self.qIn=qIn
        self.qOut=qOut
        self.jobCounter=0
        self.currentJobId=None
        self.xml=gtk.glade.XML("threadExample.glade")
        self.timeoutHandler=gtk.timeout_add(100,self.processOutcoming)
        
        dic={"on_quitButton_clicked":self.quitButton_clicked,
             "on_goButton_clicked":self.goButton_clicked,
             "on_entry1_activate":self.goButton_clicked,
             "on_window1_destroy_event":self.endApplication,
             "on_window1_delete_event":self.window1_delete
             }
        self.xml.signal_autoconnect(dic)


        self.treeview1=self.xml.get_widget('treeview1')
        #TreeStore column: job id, job label, status
        self.treestore1=gtk.TreeStore(int,str,str)
        self.treeview1.set_model(self.treestore1)
        
        cellLabel=gtk.CellRendererText()
        colLabel=gtk.TreeViewColumn('job')
        colLabel.pack_start(cellLabel,True)
        colLabel.add_attribute(cellLabel,'text',1)
        self.treeview1.append_column(colLabel)


        cellStatus=gtk.CellRendererText()
        colStatus=gtk.TreeViewColumn('status')
        colStatus.pack_start(cellStatus,True)
        colStatus.add_attribute(cellStatus,'text',2)
        self.treeview1.append_column(colStatus)

        self.progressbar1=self.xml.get_widget('progressbar1')
        
    def processOutcoming(self):
        """Handle all jobs currently in qOut, if any"""
        
        #        print "processOutcoming called"
        if self.currentJobId!=None:
            path=str(self.currentJobId)
            treeiter=self.treestore1.get_iter(path)
            self.treestore1.set_value(treeiter,2,'processing')

        
        if self.qIn.qsize() or self.currentJobId!=None:
            #self.progressbar1=self.xml.get_widget('progressbar1')
            self.progressbar1.show()
            self.progressbar1.pulse()
        else:
            self.progressbar1.hide()

        while self.qOut.qsize():
            try:
                job=self.qOut.get(0)
#                print "We have to deal with job",job.label
                self.processResult(job)
            except Queue.Empty:
                print "qOut is empty"
                pass

        return gtk.TRUE
   
    def processResult(self,job):
        """a new job has been processed, we have to display the result"""
        id=job.id
        path=str(id)
        treeiter=self.treestore1.get_iter(path)
        self.treestore1.set_value(treeiter,2,'done')


    def goButton_clicked(self,widget):
        label=self.xml.get_widget('entry1').get_text()
        self.xml.get_widget('entry1').set_text('')
        id=self.jobCounter
        self.jobCounter+=1
        job=aJob(id,label)
        self.treestore1.append(None,[id,label,'pending'])
        self.qIn.put(job)
    


    def quitButton_clicked(self,widget):
        self.endApplication()

    def window1_delete(self,widget,event):
        self.endApplication()



    def endApplication(self):
        print "time to die"
        gtk.timeout_remove(self.timeoutHandler)
        gtk.main_quit()
        
class ThreadedClient:
    """
    This class launch the GuiPart and the worker thread.
    """

    def __init__(self):
        """
        This start the gui in a asynchronous thread. We are in the "main" thread of the application, wich will later be used by the gui as well. We spawn a new thread for the worker.
        
        """
        gtk.threads_init()
        self.qIn=Queue.Queue()
        self.qOut=Queue.Queue()
        self.gui=GuiPart(self.qIn,self.qOut)
        self.running=True
        self.incomingThread=threading.Thread(target=self.processIncoming)
        #print "plop=",self.incomingThread
        self.incomingThread.setDaemon(True)
        self.incomingThread.start()
         #print "pika=",pika
        #gtk.threads_enter()
        gtk.main()
        self.running=False
        #gtk.threads_leave()



    def processIncoming(self):
       """
       This is where the blocking I/O job is being done.
       """
       while self.running:
           while self.qIn.qsize():
#               print "There are stuff in qIn"
               try:
                   job=self.qIn.get(0)
                   self.gui.currentJobId=job.id
#                   print "Let s process job",job.label
                   time.sleep(random.random()*6)
                   job.result='we would store the resutl here'
                   self.gui.currentJobId=None
                   self.qOut.put(job)
               except Queue.Empty:
                   pass
           time.sleep(2)   

    def endApplication(self):
        self.running=False

plop=ThreadedClient()

#######################
here comes the glade file:
#######################
<?xml version="1.0" standalone="no"?> <!--*- mode: xml -*-->
<!DOCTYPE glade-interface SYSTEM "http://glade.gnome.org/glade-2.0.dtd">

<glade-interface>

<widget class="GtkWindow" id="window1">
  <property name="visible">True</property>
  <property name="title" translatable="yes">window1</property>
  <property name="type">GTK_WINDOW_TOPLEVEL</property>
  <property name="window_position">GTK_WIN_POS_NONE</property>
  <property name="modal">False</property>
  <property name="default_width">250</property>
  <property name="default_height">300</property>
  <property name="resizable">True</property>
  <property name="destroy_with_parent">False</property>
  <property name="decorated">True</property>
  <property name="skip_taskbar_hint">False</property>
  <property name="skip_pager_hint">False</property>
  <property name="type_hint">GDK_WINDOW_TYPE_HINT_NORMAL</property>
  <property name="gravity">GDK_GRAVITY_NORTH_WEST</property>
  <signal name="destroy_event" handler="on_window1_destroy_event" last_modification_time="Sun, 10 Apr 2005 09:05:18 GMT"/>
  <signal name="delete_event" handler="on_window1_delete_event" last_modification_time="Sun, 10 Apr 2005 11:53:19 GMT"/>

  <child>
    <widget class="GtkVBox" id="vbox1">
      <property name="visible">True</property>
      <property name="homogeneous">False</property>
      <property name="spacing">0</property>

      <child>
	<widget class="GtkHBox" id="hbox1">
	  <property name="visible">True</property>
	  <property name="homogeneous">False</property>
	  <property name="spacing">0</property>

	  <child>
	    <widget class="GtkButton" id="goButton">
	      <property name="visible">True</property>
	      <property name="can_focus">True</property>
	      <property name="label" translatable="yes">go</property>
	      <property name="use_underline">True</property>
	      <property name="relief">GTK_RELIEF_NORMAL</property>
	      <property name="focus_on_click">True</property>
	      <signal name="clicked" handler="on_goButton_clicked" last_modification_time="Sun, 10 Apr 2005 09:09:28 GMT"/>
	    </widget>
	    <packing>
	      <property name="padding">0</property>
	      <property name="expand">False</property>
	      <property name="fill">False</property>
	      <property name="pack_type">GTK_PACK_END</property>
	    </packing>
	  </child>

	  <child>
	    <widget class="GtkEntry" id="entry1">
	      <property name="visible">True</property>
	      <property name="can_focus">True</property>
	      <property name="editable">True</property>
	      <property name="visibility">True</property>
	      <property name="max_length">0</property>
	      <property name="text" translatable="yes"></property>
	      <property name="has_frame">True</property>
	      <property name="invisible_char" translatable="yes">*</property>
	      <property name="activates_default">False</property>
	      <signal name="activate" handler="on_entry1_activate" last_modification_time="Sun, 10 Apr 2005 14:27:45 GMT"/>
	    </widget>
	    <packing>
	      <property name="padding">0</property>
	      <property name="expand">True</property>
	      <property name="fill">True</property>
	      <property name="pack_type">GTK_PACK_END</property>
	    </packing>
	  </child>
	</widget>
	<packing>
	  <property name="padding">0</property>
	  <property name="expand">True</property>
	  <property name="fill">True</property>
	</packing>
      </child>

      <child>
	<widget class="GtkScrolledWindow" id="scrolledwindow1">
	  <property name="visible">True</property>
	  <property name="can_focus">True</property>
	  <property name="hscrollbar_policy">GTK_POLICY_ALWAYS</property>
	  <property name="vscrollbar_policy">GTK_POLICY_ALWAYS</property>
	  <property name="shadow_type">GTK_SHADOW_NONE</property>
	  <property name="window_placement">GTK_CORNER_TOP_LEFT</property>

	  <child>
	    <widget class="GtkTreeView" id="treeview1">
	      <property name="visible">True</property>
	      <property name="can_focus">True</property>
	      <property name="headers_visible">True</property>
	      <property name="rules_hint">False</property>
	      <property name="reorderable">False</property>
	      <property name="enable_search">True</property>
	    </widget>
	  </child>
	</widget>
	<packing>
	  <property name="padding">0</property>
	  <property name="expand">True</property>
	  <property name="fill">True</property>
	</packing>
      </child>

      <child>
	<widget class="GtkHBox" id="hbox2">
	  <property name="visible">True</property>
	  <property name="homogeneous">False</property>
	  <property name="spacing">0</property>

	  <child>
	    <widget class="GtkProgressBar" id="progressbar1">
	      <property name="visible">True</property>
	      <property name="orientation">GTK_PROGRESS_LEFT_TO_RIGHT</property>
	      <property name="fraction">0</property>
	      <property name="pulse_step">0.1</property>
	    </widget>
	    <packing>
	      <property name="padding">0</property>
	      <property name="expand">True</property>
	      <property name="fill">True</property>
	    </packing>
	  </child>

	  <child>
	    <widget class="GtkButton" id="quitButton">
	      <property name="visible">True</property>
	      <property name="can_focus">True</property>
	      <property name="label">gtk-quit</property>
	      <property name="use_stock">True</property>
	      <property name="relief">GTK_RELIEF_NORMAL</property>
	      <property name="focus_on_click">True</property>
	      <signal name="clicked" handler="on_quitButton_clicked" last_modification_time="Sun, 10 Apr 2005 09:10:40 GMT"/>
	    </widget>
	    <packing>
	      <property name="padding">0</property>
	      <property name="expand">False</property>
	      <property name="fill">False</property>
	      <property name="pack_type">GTK_PACK_END</property>
	    </packing>
	  </child>
	</widget>
	<packing>
	  <property name="padding">0</property>
	  <property name="expand">False</property>
	  <property name="fill">True</property>
	</packing>
      </child>
    </widget>
  </child>
</widget>

</glade-interface>

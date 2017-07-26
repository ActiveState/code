from wxPython.wx import *

class MainFrame(wxFrame):

        .
        .
        .

        def __init__(self, parent, id, title):

                .
                .
                .


                # Create the Notebook

                self.nb = wxNotebook(self, -1, wxPoint(0,0), wxSize(0,0), wxNB_FIXEDWIDTH)

                # Make PANEL_1 (filename: panel1.py)

                self.module = __import__("panel1", globals())
                self.window = self.module.runPanel(self, self.nb)

                if self.window:

                        self.nb.AddPage(self.window, "PANEL_1")


                # Make PANEL_2 (filename: panel2.py)

                self.module = __import__("panel2", globals())
                self.window = self.module.runPanel(self, self.nb)

                if self.window:

                        self.nb.AddPage(self.window, "PANEL_2")


                # Make PANEL_3 (filename: panel3.py)

                self.module = __import__("panel3", globals())
                self.window = self.module.runPanel(self, self.nb)

                if self.window:

                        self.nb.AddPage(self.window, "PANEL_3")

                .
                .
                .

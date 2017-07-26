# DemoTag.py

from javax.servlet.jsp.tagext import TagSupport

class DemoTag(TagSupport):

    def __init__(self):
        self.context = None
        self.parentTag = None

    def doStartTag(self):
        out = self.context.out
        out.print("Hello World from Jython Tag.")
        return self.SKIP_BODY

    def setPageContext(self, context):
        self.context = context

    def setParent(self, parent):
        self.parentTag = parent

    def getParent(self):
        return self.parentTag

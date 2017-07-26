## store this into classes/jython/get.java

package jython;

import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.*;
import org.python.util.PythonInterpreter;
import org.python.core.*;

public class get extends TagSupport{
    public PythonInterpreter interp;
    public String cmd;
    protected PageContext pageContext;

    public get(){super();}
    public void setVar(String cmd){this.cmd=cmd;}
    public void setPageContext(PageContext pageContext) {
        this.pageContext = pageContext;
    }
    public int doEndTag() throws javax.servlet.jsp.JspTagException{
        try{
            if(pageContext.getAttribute("jythonInterp")==null){
                interp = new PythonInterpreter();
              pageContext.setAttribute("jythonInterp",interp,PageContext.PAGE_SCOPE);
            } else {
                interp=(PythonInterpreter)pageContext.getAttribute("jythonInterp");
            }

            String res=interp.eval(cmd).toString();
            pageContext.getOut().write(res);
        }catch(java.io.IOException e){
            throw new JspTagException("IO Error: " + e.getMessage());
            }
        return EVAL_PAGE;
    }
}


## store this into classes/jython/exec.java

package jython;

import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.*;
import org.python.util.PythonInterpreter;
public class exec extends BodyTagSupport{
    public PythonInterpreter interp;

    public void setParent(Tag parent) {
        this.parent = parent;
    }

    public void setBodyContent(BodyContent bodyOut) {
        this.bodyOut = bodyOut;
    }

    public void setPageContext(PageContext pageContext) {
        this.pageContext = pageContext;
    }

    public Tag getParent() {
        return this.parent;
    }

    public int doStartTag() throws JspException {
        return EVAL_BODY_TAG;
    }


    public int doEndTag() throws JspException {
        return EVAL_PAGE;
    }


    // Default implementations for BodyTag methods as well
    // just in case a tag decides to implement BodyTag.
    public void doInitBody() throws JspException {
    }

    public int doAfterBody() throws JspException {
            String cmd = bodyOut.getString();
            if(pageContext.getAttribute("jythonInterp")==null){
                interp = new PythonInterpreter();
                interp.set("pageContext",pageContext);
                pageContext.setAttribute("jythonInterp",interp,PageContext.PAGE_SCOPE);
            } else {
                interp=(PythonInterpreter)pageContext.getAttribute("jythonInterp");
            }
            interp.exec(cmd);
            return SKIP_BODY;
    }

    public void release() {
        bodyOut = null;
        pageContext = null;
        parent = null;
    }

    protected BodyContent bodyOut;
    protected PageContext pageContext;
    protected Tag parent;
}

## store this into jsp/jython.tld

<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE taglib PUBLIC "-//Sun Microsystems, Inc.//DTD JSP Tag Library 1.1//EN" "http://java.sun.com/j2ee/dtds/web-jsptaglibrary_1_1.dtd">

<taglib>
  <tlibversion>1.0</tlibversion>
  <jspversion>1.1</jspversion>
  <shortname>jython</shortname>
  <info>
  A simple Jython tag library
  </info>
  <tag>
    <name>exec</name>
    <tagclass>jython.exec</tagclass>
  </tag>
  <tag>
    <name>get</name>
    <tagclass>jython.get</tagclass>
    <bodycontent>empty</bodycontent>
    <attribute>
        <name>var</name>
        <required>true</required>
    </attribute>
  </tag>
</taglib>


## add this to the web.xml file

<taglib>
  <taglib-uri>http://www.jython.org</taglib-uri>
  <taglib-location>/WEB-INF/jsp/jython.tld</taglib-location>
</taglib>

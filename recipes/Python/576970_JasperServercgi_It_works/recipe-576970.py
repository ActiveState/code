                                  JasperServer.cgi

#!python
# -*- coding: utf-8 -*-

"""
Reports Generator.
"""
import MySQLdb
def getJRXML(reportPath):
  mycon= MySQLdb.connect(host='localhost',port=3306, db='jasperserver', user='root', passwd='')
  mycur= mycon.cursor()
  mycur.execute("select id from JIResourceFolder where uri='%s_files'" % reportPath)
  id1= mycur.fetchone()[0]
  mycur.execute("select id from JIResource where childrenFolder=%d" % id1)
  id1= mycur.fetchone()[0]
  mycur.execute("select mainReport from JIReportUnit where id=%d" % id1)
  id1= mycur.fetchone()[0]
  mycur.execute("select data from JIFileResource where id=%d" % id1)
  jrxml= mycur.fetchone()[0]
  return jrxml
#
params= {}
import os, sys, time
import cgi
cgiform= cgi.FieldStorage()
if len(cgiform)>0:
  import cgitb; cgitb.enable()
for item in cgiform.keys():
  params[item]= cgiform[item].value
#
reportUnit= params['reportUnit']; del params['reportUnit']
s1= getJRXML(reportUnit)
s2= reportUnit.split('/')[-1]

inttime= int(time.time())
tempDir= "%s\\temp" % os.path.abspath("%s\\..\\.." % os.path.dirname(sys.argv[0]))
JRXMLfile= "%s\\%s.%d.jrxml" % (tempDir, s2, inttime)

contentDir= "%s\\airscontent" % os.path.abspath("%s\\..\\.." % tempDir)
output= params['output']
reportFILE= "%s\\%s.%d.%s" % (contentDir,s2,inttime,output)
reportURI= "/airscontent/%s.%d.%s" % (s2,inttime, output)

jrxml= open(JRXMLfile,'w')
jrxml.write(s1)
jrxml.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import JasperReports
JR= JasperReports.JasperReports()
JR.startJVM()
connection= ("com.mysql.jdbc.Driver","jdbc:mysql://localhost:3306/airs","airs","airs")
JR.JasperReports(JRXMLfile,connection,params,reportFILE)
JR.shutdownJVM()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

if os.path.exists(reportFILE):
  print """Content-type: text/html

  <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
  <script language='javascript' type='text/javascript'>
    window.location='%s';
  </script>
  """ % reportURI
else:
  print """Content-type: text/html;charset=utf-8

<H1>Report '%s' failed</H1>""" % reportURI
#

                       JasperReports.py
#!pyhon
# -*- coding: utf-8 -*-
"""
JasperReports wrapper:
"""

class JasperReports():
  import jpype
  JasperCompileManager= JasperFillManager= JasperExportManager= None
  JRPdfExporter= JRRtfExporter= JRHtmlExporter= JRXlsExporter= None
  JRExporterParameter= JRPdfExporterParameter= JRXlsExporterParameter= None
  JRLoader= JRParameter= JRXmlDataSource= JRXPathQueryExecuterFactory= JRXmlUtils= None

  def startJVM(self):
    JVMPath= self.jpype.getDefaultJVMPath()
    pathToJRLibs= "c:\\Program Files\\jasperserver-3.0\\apache-tomcat\\webapps\\jasperserver\\WEB-INF\\lib\\"

    _jvmArgs = ["-ea"] # enable assertions
    _jvmArgs.append("-Djava.ext.dirs=%s" % pathToJRLibs)
    self.jpype.startJVM(JVMPath, *_jvmArgs)
    #
    self.JasperCompileManager= self.jpype.JClass("net.sf.jasperreports.engine.JasperCompileManager")
    self.JasperFillManager= self.jpype.JClass("net.sf.jasperreports.engine.JasperFillManager")
    self.JasperExportManager= self.jpype.JClass("net.sf.jasperreports.engine.JasperExportManager")
  
    self.JRPdfExporter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRPdfExporter")
    self.JRRtfExporter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRRtfExporter")
    self.JRHtmlExporter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRHtmlExporter")
    self.JRXlsExporter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRXlsExporter")
    #
    self.JRParameter= self.jpype.JClass("net.sf.jasperreports.engine.JRParameter")
    self.JRExporterParameter= self.jpype.JClass("net.sf.jasperreports.engine.JRExporterParameter")
    self.JRPdfExporterParameter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRPdfExporterParameter")
    self.JRXlsExporterParameter= self.jpype.JClass("net.sf.jasperreports.engine.export.JRXlsExporterParameter")
  
    self.JRLoader= self.jpype.JClass("net.sf.jasperreports.engine.util.JRLoader")
    self.JRXmlDataSource= self.jpype.JClass("net.sf.jasperreports.engine.data.JRXmlDataSource")
    self.JRXPathQueryExecuterFactory= self.jpype.JClass("net.sf.jasperreports.engine.query.JRXPathQueryExecuterFactory")
    self.JRXmlUtils= self.jpype.JClass("net.sf.jasperreports.engine.util.JRXmlUtils")
  #:
  def shutdownJVM(self):
    self.jpype.shutdownJVM()
#
  def JasperReports(self,jrxml,connection,parameters, report):
    def JDBCconnection(conpars):
      jdbcDriver= self.jpype.JClass(conpars[0])
      dm= self.jpype.JClass("java.sql.DriverManager")
      conn= dm.getConnection(conpars[1], conpars[2], conpars[3])
      conn.setAutoCommit(self.jpype.JBoolean(False))
      return conn
    #}def JDBCconnection
    s1= '.'.join(jrxml.split('.')[:-1])
    output= parameters["output"]
    jasper= "%s.jasper" % s1
    jrprint= "%s.jrprint" % s1
  
    #
    self.JasperCompileManager.compileReportToFile(jrxml,jasper)
    #
    jdbc= JDBCconnection(connection)
    jasperParameters= self.jpype.JClass("java.util.HashMap")()
    if output in ['xls']:#,'html']:
      jasperParameters.put(JRParameter.IS_IGNORE_PAGINATION, True)
    for item in parameters.keys():
      jasperParameters.put(item, parameters[item].decode("utf-8"))  
    self.JasperFillManager.fillReportToFile(jasper, jrprint, jasperParameters, jdbc)
    #
    if output=="pdf":
      exporter = self.JRPdfExporter()
      exporter.setParameter(self.JRPdfExporterParameter.IS_CREATING_BATCH_MODE_BOOKMARKS, True)
    elif output=="rtf":
      exporter= self.JRRtfExporter()
      #
    elif output=="xls":
      exporter= self.JRXlsExporter()
      exporter.setParameter(self.JRXlsExporterParameter.IS_REMOVE_EMPTY_SPACE_BETWEEN_ROWS, True);
    elif output=="html":
      exporter= self.JRHtmlExporter()
    else:
      return
    exporter.setParameter(self.JRExporterParameter.INPUT_FILE_NAME, jrprint)
    exporter.setParameter(self.JRExporterParameter.OUTPUT_FILE_NAME, report)
    exporter.exportReport()
# ------------------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JasperReports wrapper:
"""

import jpype

JVMPath= jpype.getDefaultJVMPath()
pathToJRLibs= "c:\\Program Files\\jasperserver-3.0\\apache-tomcat\\webapps\\jasperserver\\WEB-INF\\lib\\"

JasperCompileManager= JasperFillManager= JasperExportManager= None
JRPdfExporter= JRRtfExporter= JRHtmlExporter= JRXlsExporter= None
JRExporterParameter= JRPdfExporterParameter= JRXlsExporterParameter= None
JRLoader= JRParameter= JRXmlDataSource= JRXPathQueryExecuterFactory= JRXmlUtils= None
def startJVM():
  global JasperCompileManager, JasperFillManager, JasperExportManager, \
    JRPdfExporter, JRRtfExporter, JRHtmlExporter, JRXlsExporter, \
    JRExporterParameter, JRPdfExporterParameter, JRrtfExporterParameter, JRXlsExporterParameter, \
    JRLoader, JRParameter,JRXmlDataSource, JRXPathQueryExecuterFactory, JRXmlUtils

  _jvmArgs = ["-ea"] # enable assertions
  _jvmArgs.append("-Djava.ext.dirs=%s" % pathToJRLibs)
  jpype.startJVM(JVMPath, *_jvmArgs)
  #
  JasperCompileManager= jpype.JClass("net.sf.jasperreports.engine.JasperCompileManager")
  JasperFillManager= jpype.JClass("net.sf.jasperreports.engine.JasperFillManager")
  JasperExportManager= jpype.JClass("net.sf.jasperreports.engine.JasperExportManager")
  
  JRPdfExporter= jpype.JClass("net.sf.jasperreports.engine.export.JRPdfExporter")
  JRRtfExporter= jpype.JClass("net.sf.jasperreports.engine.export.JRRtfExporter")
  JRHtmlExporter= jpype.JClass("net.sf.jasperreports.engine.export.JRHtmlExporter")
  JRXlsExporter= jpype.JClass("net.sf.jasperreports.engine.export.JRXlsExporter")
  #
  JRParameter= jpype.JClass("net.sf.jasperreports.engine.JRParameter")
  JRExporterParameter= jpype.JClass("net.sf.jasperreports.engine.JRExporterParameter")
  JRPdfExporterParameter= jpype.JClass("net.sf.jasperreports.engine.export.JRPdfExporterParameter")
  JRXlsExporterParameter= jpype.JClass("net.sf.jasperreports.engine.export.JRXlsExporterParameter")
  
  JRLoader= jpype.JClass("net.sf.jasperreports.engine.util.JRLoader")
  JRXmlDataSource=jpype.JClass("net.sf.jasperreports.engine.data.JRXmlDataSource")
  JRXPathQueryExecuterFactory=jpype.JClass("net.sf.jasperreports.engine.query.JRXPathQueryExecuterFactory")
  JRXmlUtils=jpype.JClass("net.sf.jasperreports.engine.util.JRXmlUtils")
#:
def shutdownJVM():
  jpype.shutdownJVM()
#
def JasperReports(jrxml,connection,parameters, report):
  def JDBCconnection(conpars):
    jdbcDriver= jpype.JClass(conpars[0])
    dm= jpype.JClass("java.sql.DriverManager")
    conn= dm.getConnection(conpars[1], conpars[2], conpars[3])
    conn.setAutoCommit(jpype.JBoolean(False))
    return conn
  #}def JDBCconnection
  s1= '.'.join(jrxml.split('.')[:-1])
  output= parameters["output"]
  jasper= "%s.jasper" % s1
  jrprint= "%s.jrprint" % s1
  
  #
  JasperCompileManager.compileReportToFile(jrxml,jasper)
  #
  jdbc= JDBCconnection(connection)
  jasperParameters= jpype.JClass("java.util.HashMap")()
  if output in ['xls']:#,'html']:
    jasperParameters.put(JRParameter.IS_IGNORE_PAGINATION, True)
  for item in parameters.keys():
    jasperParameters.put(item, parameters[item].decode("utf-8"))  
  JasperFillManager.fillReportToFile(jasper, jrprint, jasperParameters, jdbc)
  #
  if output=="pdf":
    exporter = JRPdfExporter()
    exporter.setParameter(JRPdfExporterParameter.IS_CREATING_BATCH_MODE_BOOKMARKS, True)
  elif output=="rtf":
    exporter= JRRtfExporter()
    #
  elif output=="xls":
    exporter= JRXlsExporter()
    exporter.setParameter(JRXlsExporterParameter.IS_REMOVE_EMPTY_SPACE_BETWEEN_ROWS, True);
  elif output=="html":
    exporter= JRHtmlExporter()
  else:
    return
  exporter.setParameter(JRExporterParameter.INPUT_FILE_NAME, jrprint)
  exporter.setParameter(JRExporterParameter.OUTPUT_FILE_NAME, report)
  exporter.exportReport()
# ------------------------------------------------------------------------------------------

## Http client to POST using multipart/form-data  
Originally published: 2002-08-23 07:56:39  
Last updated: 2002-08-23 07:56:39  
Author: Wade Leftwich  
  
A scripted web client that will post data to a site as if from a form using ENCTYPE="multipart/form-data". This is typically used to upload files, but also gets around a server's (e.g. ASP's) limitation on the amount of data that can be accepted via a standard POST (application/x-www-form-urlencoded).
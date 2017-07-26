## Enumerated values by name or numberOriginally published: 2004-09-13 16:10:21 
Last updated: 2004-09-13 16:10:21 
Author: Samuel Reynolds 
 
This enumerated-values class is intended for use in module-level constants, such as an employee type or a status value. It allows simple attribute notation (e.g., employee.Type.Serf or employee.Type.CEO), but also supports simple bidirectional mapping using dictionary notation (e.g., employee.Type['CEO']-->1 or employee.Type[1]-->'CEO').
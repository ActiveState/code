####################################################################
# Reads a property file using the java properties object and returns 
# a property object.
####################################################################
proc hashMap { propertiesFile } {

   putsLog "proc - [info level 0 ]"

   java::import java.util.Properties
   java::import java.util.Hashtable
   java::import java.util.Map
   java::import java.io.FileInputStream

   set FileInputStreamI [ java::new FileInputStream $propertiesFile ]
   set PropertiesI      [ java::new Properties ]  

   $PropertiesI load $FileInputStreamI 

   #puts $hashTableList 

   return $PropertiesI

}

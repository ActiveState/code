# Import statements
from xml.dom.ext.reader.Sax2 import FromXmlStream
from xml.xpath import Evaluate
import os, shutil, sys, pickle, threading, random, time, logging, ftplib

global logger, timer_start_dict, timer_end_dict, download_status

def make_backup(module_id):
	""" Function: Move the directory to  a backup location
	"""
	backup_location = config.find_location_for_module(module_id, 'backup_location') 
	stage_location = config.find_location_for_module(module_id, 'stage_location') 
	logger.info("["+module_id+"] Moving files " + stage_location + " to " + backup_location )
	try:
		if os.path.exists(backup_location):
			shutil.rmtree( backup_location, True )
		else:
			#This is to ensure that backup folder's path exists
			#and this path is reachable
			os.makedirs(backup_location)
			shutil.rmtree(backup_location, True )			
		if os.path.exists(stage_location):	
			shutil.move( stage_location , backup_location)
		else:
			logger.info("Location " + stage_location + " not present, no backup taken")
	except:
		logger.error("[" + module_id + "] Failed to remove:" + backup_location)
		logger.error("[" + module_id + "] Failed to remove Error:" + str(sys.exc_info()[0])+ " " + str(sys.exc_info()[1]))
		raise 
	else:
		os.makedirs(stage_location)
	

def copy_to_machine(machine_name, module_id, config):
	""" Function: Move a module installer files to a remote mahine from local location
	""" 
	remote_location = config.find_location_on_remote_machine(module_id, machine_name)
	local_module_location = config.find_location_for_module(module_id, 'stage_location')
	logger.info( "[" + module_id + "] Copying from " + local_module_location + " to " + remote_location)
	
	try:
		if os.path.isdir(remote_location):
			shutil.rmtree(remote_location, True )
	except:
		logger.error("[" + module_id + "] Failed to remove:" + remote_location + "on machine " + machine_name)
		logger.error("[" + module_id + "] Failed to remove Error:" + str(sys.exc_info()[0])+ " " + str(sys.exc_info()[1]))
	
	try:
		shutil.copytree(local_module_location, remote_location)
	except:
		logger.info("FAILURE: Copy of module " + module_id + "Failed on machine " + machine_name )
		logger.error("[" + module_id + "] Failed to copy:" + remote_location)
		logger.error("[" + module_id + "] Failed to copy Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
		
def recur_get(ftp, ftp_loc, local_loc, module_id, config, ftp_pool):
    """ Function: Recursive function to get everything under the remote location ftp_loc 
    	and transfer these to the local location local_loc for module module_id
    	ftp_loc is the absolute location on the remove server however local_loc is the
    	absolute location on the local machine where the files/directories are to be created
    """ 
    local_ftp_loc = ftp_loc
    logger.debug( "Parameters for  recur_get ftp_loc: " + local_ftp_loc  )
    logger.debug( "Parameters for  recur_get local_loc: " + local_loc  )
    logger.debug( "FTP' CDing to location: " + local_ftp_loc  )
    ftp.cwd("/")		
    ftp.cwd(local_ftp_loc)
    for file in ftp.nlst():
        if file == "." or file == "..":
            continue
        try:
            logger.debug( "current position is " + ftp.pwd())
            logger.debug( "Taking up position at " + local_ftp_loc)
            ftp.cwd("/") 
            ftp.cwd(local_ftp_loc) 	
            logger.debug("Try CDing to directory :" + file  + "from" + local_ftp_loc)
            ftp.cwd(file)
            ftp.cwd('..')
            # A rather weired method to see if a file or directory exists on the remote server
            # Since unix and windows has different conventions for directory name, this is the only
            # platform independent method I could think of, suggestions welcome
            logger.debug( "Success, this is a directory: " + file  )
            stage_location_tmp =  os.path.join(local_loc, file)
            logger.debug( "Creating a local folder : " + stage_location_tmp  )
            try:
               os.makedirs(stage_location_tmp)
            except:
               logger.debug( "Already Exists: " + file + " [" + str(sys.exc_info()[1])+ "]"  )
            #The local_ftp_loc string is saved so that it does not get corrupted
            #when the function gets into the recursive loop
            str_for_ftp = local_ftp_loc
            recur_get(ftp, str_for_ftp + "/" + file , os.path.join(local_loc, file), module_id, config, ftp_pool)
            #original position of the ftp object is restored here
            ftp.cwd("/") 
            ftp.cwd(local_ftp_loc)              
        except ftplib.error_perm :
                logger.info( "File: " + file )
                logger.debug("[" + str(sys.exc_info()[1])+ "]")
                localfile = os.path.join(local_loc, file)
            	try:
                    ftp_pool.asynchronous_ftp_get( local_ftp_loc + "/" + file,localfile)
                except:
                    logger.error("Error reading from remote machine")
                    logger.error("Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
                    raise                   
        except:	
            logger.info( "Other error " + file + " " + " [" + str(sys.exc_info()[1])+ "]"  )
            raise

def get_build(module_id, config):
    """  Function to get the module from the FTP Server
    """ 
    if config.find_keep_original(module_id).lower() == "yes":
	    make_backup(module_id)
    logger.info("["+module_id+"]FTP for this module started")
    machine_name = config.find_ftp_info_machine_name_for_module(module_id)
    uid = config.find_ftp_info_for_module(module_id, 'ftp_uid')
    pwd = config.find_ftp_info_for_module(module_id, 'ftp_password')
    ftp_loc = config.find_ftp_info_for_module(module_id, 'ftp_location')
    local_loc = config.find_location_for_module(module_id, 'stage_location')
    logger.debug("[" + module_id + "] Connecting to machine " + machine_name)
    ftp_pool = FTP_pool(module_id,config)
    local_loc = os.path.join(local_loc,os.path.basename(ftp_loc))
    os.makedirs(local_loc)
     
    try:
        ftp = ftplib.FTP(machine_name)
        ftp.login(uid, pwd)
        recur_get(ftp, ftp_loc, local_loc, module_id, config, ftp_pool)
        ftp.quit()
        ftp_pool.close_all()
    except:
        ftp_pool.close_all()
        logger.error("[" + module_id + "]Unable to access FTP location")
        logger.error("[" + module_id + "]Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
        download_status[module_id] = "FAILED"
        raise
    else:
        logger.info("[" + module_id + "] FTP for module completed")
        download_status[module_id] = "SUCCESS"


def download_distribute(module_id, machine_list,config):
    """ Function to move the module to the list of machines
    """
    global timer_start_dict, timer_end_dict
    timer_start_dict[module_id] = time.time()
    get_build(module_id,config)
    timer_end_dict[module_id] = time.time()
    for machine_name in machine_list:
        copy_to_machine(machine_name, module_id,config )
	

class module_thread(threading.Thread):
    """ For each module that is downloaded a thread of this class is invoked, so 
        that each of the module that is to be downloaded is done in parallel
    """
    def __init__(self, module):
        self.module=module
        self.config=config
        self.machine_list=config.find_subscribed_machines_for_module(module)
        self.location=config.find_location_for_module( module, 'stage_location')
        threading.Thread.__init__(self)

    def run(self):
        try: 
          download_distribute(self.module, self.machine_list, self.config)    
        except: 
          logger.error("[" +self.module + "]FTP Process for this module terminated as error")
          logger.error("Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
          download_status[module_id] = "FAILED"

class config_file_util:
    """ The class to handle all the configiration file related infornation
    """

    def __init__(self, config_file):
        fp = open(config_file,'r')
        self.dom = FromXmlStream(fp)
        fp.close()
        self.config_file=config_file
		
    def find_all_modules(self):
		module_id_list = []
		for t in Evaluate('module_list/module[@id]', self.dom.documentElement):
				module_id_list.append(str(Evaluate('@id', t)[0].nodeValue).strip())
		return module_id_list
        
    def find_keep_original(self, module_id):
        module_id_list = []
        t = Evaluate('module_list/module[@id=\''+module_id+'\']', self.dom.documentElement)
        return (str(Evaluate('@keep_original', t[0])[0].nodeValue).strip())
		
    def find_subscribed_machines_for_module(self,module_id):
        machine_name_list = []
        xpath = 'machine_list/machine/distribute_module/module_name[@id=\'' + module_id + '\']'
        for t in Evaluate(xpath, self.dom.documentElement):
        	m =  Evaluate('parent::*/parent::*', t)
        	machine_name_list.append(str(Evaluate('@machine_name', m[0])[0].nodeValue).strip())
        return machine_name_list
    
    def find_location_for_module(self, module_id, location):
    	xpath = 'module_list/module[@id=\'' + module_id + '\']'+'/'+location+'/text()'
    	return (Evaluate(xpath, self.dom.documentElement)[0].nodeValue).strip()

    def find_ftp_info_machine_name_for_module(self, module_id):
    	xpath = 'module_list/module[@id=\'' + module_id + '\']'+'/ftp_info'
    	m =  Evaluate(xpath, self.dom.documentElement)[0]
    	return (Evaluate('@machine_name', m)[0].nodeValue).strip()
		
    def find_ftp_info_for_module(self, module_id,info_tag):
    	xpath = 'module_list/module[@id=\'' + module_id + '\']'+'/ftp_info/' + info_tag + '/text()'
    	return (Evaluate(xpath, self.dom.documentElement)[0].nodeValue).strip()
                
    def find_location_on_remote_machine(self, module_id, machine_name):
    	xpath = 'machine_list/machine[@machine_name=\"' + machine_name + '\"]'+'/distribute_module/module_name[@id=\"' \
    	        + module_id +'\"]' 
    	m = Evaluate(xpath, self.dom.documentElement)
    	return (Evaluate('parent::*/local_location/text()', m[0])[0].nodeValue).strip()
		
    def find_config(self, config_id):
        xpath = 'config_list/config_item[@id=\"' + config_id + '\"]/text()' 
        m = Evaluate(xpath, self.dom.documentElement)
        return (m[0].nodeValue).strip()
        
# A thread class that would perform the ftp get asyncbronously.
class ftp_thread(threading.Thread):
    """ This thread that is invoked to FTP a single file.
    """
    global logger
    def __init__(self, ftp_session, ftp_session_id, remote_file, localfile, thread_pool_object ):
        self.ftp_session=ftp_session
        self.remote_file=remote_file
        self.localfile=localfile
        self.thread_pool_object = thread_pool_object
        self.ftp_session_id = ftp_session_id
        threading.Thread.__init__(self)

    def run(self):
        try:
            local_file = open(self.localfile, 'wb')
            logger.debug("[Session#"+str(self.ftp_session_id)+"]-Getting file " + self.localfile)
        except:
            logger.error("Error writing to local file")
            logger.error("Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
            raise
        try: 
            buffer_size = int(config.find_config("BUFFER_SIZE"))*1024
            self.ftp_session.retrbinary('RETR ' + self.remote_file, local_file.write, buffer_size)   
        except: 
          logger.error("[Session#"+str(self.ftp_session_id)+"]-Error from remote location for file " + self.remote_file )
          logger.error("Error:" + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
        self.thread_pool_object.release_ftp_session_id(self.ftp_session_id)
        local_file.close()
        
class FTP_pool:
    """
    	Class  for maintaining a Pool of Open FTP sessions
    """
    def __init__(self, module_id, config):
        self.number_of_connections = int(config.find_config("NUM_CONNECTION"))
        self.wait_for_connnection_time = int(config.find_config("FTP_TIMEOUT"))
        self.ftp_session_pool = []
        self.ftp_pool_lock = []
        self.module_id = module_id
        self.machine_name = config.find_ftp_info_machine_name_for_module(module_id)
        self.uid = config.find_ftp_info_for_module(module_id, 'ftp_uid')
        self.pwd = config.find_ftp_info_for_module(module_id, 'ftp_password')
        self.thread_list = []
        for i in range(self.number_of_connections):
            logger.debug("Creating FTP session " + str(i) +" "+ self.machine_name+" "+ self.uid+" "+self.pwd)
            ftp_session = ftplib.FTP(self.machine_name)
            ftp_session.login(self.uid, self.pwd)
            self.ftp_session_pool.append(ftp_session)
            self.ftp_pool_lock.append(threading.Lock())
          
    def __get_ftp_session_id_(self):
        """ Returns an unsued FTP session from the pool
        """
        wait_time = 0
        while True:
            for i in range(self.number_of_connections):
                if self.ftp_pool_lock[i].locked() == False:
                    self.ftp_pool_lock[i].acquire()
                    logger.debug("Request for ftp session got session #" + str(i) )
                    return i
            time.sleep(3)
            wait_time = wait_time + 3
            if wait_time < self.wait_for_connnection_time:
               logger.debug("No ftp sessions available..re-checking after wait..." )
               continue
            else:
               raise NameError, "TimeOut for FTP"
               
    def release_ftp_session_id(self, ftp_session_id):
        """ Method to release the FTP session back to the common pool 
        """
        self.ftp_pool_lock[ftp_session_id].release()

               
    def asynchronous_ftp_get(self,remote_file,localfile):
        """ This function is called to invoke a thread that will download the file
        """
        ftp_session_id = self.__get_ftp_session_id_()
        logger.debug("session allocated " + str(ftp_session_id))
        thread_id = ftp_thread( self.ftp_session_pool[ftp_session_id],ftp_session_id,remote_file, localfile, self)
        thread_id.start()
        self.thread_list.append(thread_id)
        
    def close_all(self):
        """ Close all FTP connections and threads
        """
        for tid in self.thread_list:
            logger.debug("Waiting for thread" + str(tid) )
            tid.join()
            logger.debug("thread" + str(tid) + " terminated")
        for i in range(self.number_of_connections):
            self.ftp_session_pool[i].quit()
        
            
"""
    End of Functions and Class definitions
"""
def main(command_line):
    """
    	Function invoked my __main__
    """
    usage = """
    myFTP : A tool to download files and directories from remote location
    Usage : myftp <config.xml>   
    """
    if len(command_line) < 2 :
        print usage
        sys.exit(1)
    else:
        config_file = command_line[1]
        
    # Read the configurations
    print "Reading config file :" + config_file
    global config, logger, timer_start_dict, timer_end_dict, download_status

    try:
        config = config_file_util(config_file)
    except:
        print "Configuration file may be corrupted, Quiting..."
        print str(sys.exc_info()[0])+ " " + str(sys.exc_info()[1])
        sys.exit(1)  
    
    # Execute the FTP Process for all modules
    thread_id_list = []
    timer_end_dict = {}
    timer_start_dict = {}
    download_status = {}
    logger_status = {"DEBUG":logging.DEBUG, "ERROR":logging.ERROR, \
                     "INFO":logging.INFO, "WARNING":logging.WARNING}
                     
    # Creating the Logging Mechanism
    try:
        logger = logging.getLogger('ftpbuild')
        hdlr = logging.FileHandler(config.find_config("LOG"),"wb")
        stderr_hdlr = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.addHandler(stderr_hdlr) 
        logger.setLevel(logger_status[config.find_config("LOG_LEVEL")])
        logger.info("========================================================")
        logger.info("=========== START OF FTP PROCESS  ======================")
        logger.info("========================================================")
    except:
        print "Unable to start logging, Quiting..."
        print str(sys.exc_info()[0])+ " " + str(sys.exc_info()[1])
        sys.exit(1)  

       
    for module_id in config.find_all_modules():
        timer_start_dict[module_id] = 0
        timer_end_dict[module_id] = 0
        download_status[module_id] = "SUCCESS"
        thread_id = module_thread(module_id)
        thread_id_list.append(thread_id)
        thread_id.start() 
        
    for tid in thread_id_list:
        tid.join()
    
    for module_id in config.find_all_modules():
        if download_status[module_id] == "SUCCESS":
            download_time = time.strftime("%d-%H:%M:%S",time.gmtime(timer_end_dict[module_id] - timer_start_dict[module_id]))
            logger.info(">>>>>>>>["+module_id + "] DOWNLOAD SUCCESSFUL<<<<<<<")
            logger.info(">>>>>>>>Download time for module ["+module_id + "] is " + download_time)
        else:
            logger.info("<<<<<<<<<<["+module_id + "] DOWNLOAD FAILED>>>>>>>")
            
    logger.info("========================================================")
    logger.info("=========== END OF FTP PROCESS  ========================")
    logger.info("========================================================")

if __name__ == "__main__":
    main(sys.argv)

        
------------------------------------------------------------------------
Sample XML file
-------------------
<?xml version="1.0"?>

<!DOCTYPE download [
<!ELEMENT download (config_list, module_list, machine_list )>
<!ELEMENT config_list (config_item+)>
<!ELEMENT config_item (#PCDATA)>
<!ELEMENT module_list (module+)>
<!ELEMENT machine_list (machine*)>
<!ELEMENT machine (distribute_module+)>
<!ELEMENT distribute_module (module_name, local_location)>
<!ELEMENT module_name (#PCDATA)>
<!ELEMENT local_location (#PCDATA)>
<!ELEMENT module (alias_name_list, ftp_info, stage_location, backup_location)>
<!ELEMENT alias_name_list (alias_name)>
<!ELEMENT alias_name (#PCDATA)>
<!ELEMENT ftp_info (ftp_uid,ftp_password,ftp_location)>
<!ELEMENT ftp_uid (#PCDATA)>
<!ELEMENT ftp_password (#PCDATA)>
<!ELEMENT ftp_location (#PCDATA)>
<!ELEMENT backup_location (#PCDATA)>
<!ELEMENT stage_location (#PCDATA)>

<!ATTLIST module id CDATA #REQUIRED common_name CDATA #REQUIRED install_depot_name CDATA #REQUIRED keep_original CDATA #REQUIRED keep_history CDATA #REQUIRED>
<!ATTLIST module_name id CDATA #REQUIRED>
<!ATTLIST machine machine_name CDATA #REQUIRED>
<!ATTLIST ftp_info machine_name CDATA #REQUIRED>
<!ATTLIST config_item id CDATA #REQUIRED description CDATA #REQUIRED>
<!ATTLIST ftp_password encryption (plaintext|base64) #IMPLIED>
]> 
<download>
<!-- List of configiurations items, these are self explanatory-->
<config_list>
	<config_item id = "LOG" description="The location and file where the log file for this process is stored">
		c:\docume~1\sasdemo\locals~1\temp\ftp.log
	</config_item>
	<config_item id = "NUM_CONNECTION" description="number of connections to be maintained in the pool">
		35
	</config_item>
	<config_item id = "FTP_TIMEOUT" description="number of seconds to wait for a FTP session">
		21600
	</config_item>
	<!-- Logging levels "DEBUG" "ERROR""INFO""WARNING" -->
	<config_item id = "LOG_LEVEL" description="What is the level of logging required INFO/ERROR/WARNING">
			INFO
	</config_item>	
	<config_item id = "BUFFER_SIZE" description="Size of the file buffer size used by the FTP in kilo bytes">
			16
	</config_item>	
	
</config_list>
<!-- module_list: Describes the module(s) ( directory structure on your server machine) to be downloaded -->
<module_list>
<!-- module_id: A unique name for the module
     install_depit_name: the directory name of this module in the server
     keep_original: if this module is already present on your local machine,'yes' would move this directory to 
                    .org folder
     keep_history: not yet implemented-->

	<module id = "TEST" common_name= "test" install_depot_name = "test" keep_original = "yes" keep_history = "no">
		<!--List of alias names that you can specify for this module name, not yet implemented -->
		<alias_name_list>
			<alias_name>
			</alias_name>
		</alias_name_list>
		<!--Name of the machine you are trying to FTP the module from -->
		<ftp_info machine_name = "remte_server_name.domain.com">
			<ftp_uid>my_user_id</ftp_uid>
			<ftp_password>my_password</ftp_password>
			<!-- Location on the remote machine where the module is located-->
			<ftp_location>/Work</ftp_location>
		</ftp_info>
		<!--stage_location: location in the local machine where the module will be downloaded -->
		<stage_location>c:\docume~1\sasdemo\locals~1\temp\target</stage_location>
		<!--backup_location: if the module TEST is already downloaded at the stage_location, backup_location
		                     refers to which location the already downloaded module should be moved-->
		<backup_location>c:\docume~1\sasdemo\locals~1\temp\backup</backup_location>
	</module>
	<module id = "TEST2" common_name= "test" install_depot_name = "test" keep_original = "yes" keep_history = "no">
		<!--List of alias names that you can specify for this module name, not yet implemented -->
		<alias_name_list>
			<alias_name>
			</alias_name>
		</alias_name_list>
		<!--Name of the machine you are trying to FTP the module from -->
		<ftp_info machine_name = "remte_server_name.domain.com">
			<ftp_uid>my_user_id</ftp_uid>
			<ftp_password>my_password</ftp_password>
			<!-- Location on the remote machine where the module is located i.e. on the remote machine the 
			     files are located at /worl/TEST2 so under ftp_location the location is mentioned as /work-->
			<ftp_location>/Work</ftp_location>
		</ftp_info>
		<!--stage_location: location in the local machine where the module will be downloaded -->
		<stage_location>c:\docume~1\sasdemo\locals~1\temp\target</stage_location>
		<!--backup_location: if the module TEST is already downloaded at the stage_location, backup_location
												 refers to which location the already downloaded module should be moved-->
		<backup_location>c:\docume~1\sasdemo\locals~1\temp\backup</backup_location>
	</module>

</module_list>
<!-- Machine_list: the list of machines on which the modules downloaded above is to be copied -->
<machine_list>
	<!-- machine_name: refers to the machine(s) on which this module is to be copied-->
	<machine machine_name= "one_machine_on_my_network">
	  <!-- distribute_module: the list of module(s) ( mentioned under module_name ) that beeds to be transfered-->
		<distribute_module >
			<module_name id = "TEST"/>
			<!-- local_location: the location on the machine to copy the files to.-->
			<local_location>\\one_machine_on_my_network\location_to_copy_test</local_location>
		</distribute_module>
		<distribute_module >
			<module_name id = "TEST2"/>
			<!-- local_location: the location on the machine to copy the files to.-->
			<local_location>\\one_machine_on_my_network\location_to_copy_test</local_location>
		</distribute_module>
	</machine>
	<machine machine_name= "two_machine_on_my_network">
	  <!-- distribute_module: the list of module(s) ( mentioned under module_name ) that beeds to be transfered-->
		<distribute_module >
			<module_name id = "TEST"/>
			<!-- local_location: the location on the machine to copy the files to.-->
			<local_location>\\one_machine_on_my_network\location_to_copy_test</local_location>
		</distribute_module>
		<distribute_module >
			<module_name id = "TEST2"/>
			<!-- local_location: the location on the machine to copy the files to.-->
			<local_location>\\two_machine_on_my_network\location_to_copy_test</local_location>
		</distribute_module>
	</machine>
</machine_list>
</download>        
        

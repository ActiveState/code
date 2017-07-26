import os
import re
from urllib2 import urlopen

base_url_qacandrot = "https://qacand.sflab.ondemand.com/sf-version.properties"
base_url_qapatch = "http://qapatch.successfactors.com/sf-version.properties"
base_url_qacand = "http://qacand.successfactors.com/sf-version.properties"

# get test environment
print "Before use this tool, please make sure you connect to VPN!"
env = raw_input("Please enter your test env: qacand, qacandrot or qapatch (Non case sensitive): ")

if env.strip().lower() == "qacand":
    html_resource = urlopen(base_url_qacand).read()
elif env.strip().lower() == "qapatch":
    html_resource = urlopen(base_url_qapatch).read()
elif html_resource == "qacandrot":
    html_resource = urlopen(base_url_qacandrot).read()

module_svn_map = {}

pattern = "(.*?)-(.*?)-(.*?)sion=(\d+$)"
p = re.compile(pattern)

for strofmodule in html_resource.split():
    if re.match(pattern, strofmodule):
        results = re.findall(pattern, strofmodule)
        module = results[0][1]
        svn_number = results[0][3]
        module_svn_map[module] = svn_number
        
build_num_pattern = "com.successfactors.sf-packages.version="
build_num_len = html_resource.index(build_num_pattern) + len(build_num_pattern)
build_version = html_resource[build_num_len:]

print "build version is " + build_version, "please make sure it is same as that on " + env.strip().lower() + "."


while 1:
    build_by_module = raw_input("Is your module build by module: (y or n, Non case sensitive) ")

    if build_by_module.strip().lower() == "n":
        your_module = "V4"
        your_svn_number = raw_input("Please enter your svn number (6 digit): ")
        if int(your_svn_number) <= int(module_svn_map[your_module]):
            print "Your svn number is included in current build on " + env.strip().lower() + "."
        else:
            print "Your svn number is NOT included on " +env.strip().lower() + "."
        os.system("pause")    
    elif build_by_module.strip().lower() == "y":
        print "Please make sure your input is exactly same as one of module above!"
        your_module = raw_input("Please enter your module name: ")
        your_svn_number = raw_input("Please enter your svn number (6 digit): ")
        if your_module.strip().lower() in module_svn_map.keys():
            if int(your_svn_number) <= int(module_svn_map[your_module]):
                print "Your svn number is included in current build on " + env.strip().lower() + "."
            else:
                print "Your svn number is NOT included on " + env.strip().lower() + "."
        os.system("pause")

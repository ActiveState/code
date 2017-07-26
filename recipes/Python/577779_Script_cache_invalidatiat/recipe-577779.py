#/usr/bin/python2.6

import sys
import os
import os.path
import hashlib

from boto.cloudfront import CloudFrontConnection

################################################################################

AWS_ACCESS_KEY          = 'AKIAIPN42DSDDJ3354DSDS'
AWS_SECRET_ACCESS_KEY   = 'iu4d2QoU+kJFSfghfghfghfghfghfghl'
AWS_CF_DISTRIBUTION_ID  = 'ERKDWKOK23346LDD2'

IGNORE = ['.svn','.php','.py','staticData']

################################################################################

def get_files_from_dir(base_dir):
    file_list = []
    for root, subFolders, files in os.walk(base_dir):
        next = False
        for it in IGNORE:
            if it in root:
                next = True
                break
        if next:
            continue
        next = False
        for filename in files:
            for it in IGNORE:
                if it in filename:
                    next = True
            if next:
                continue
            file_list.append(os.path.join(root,filename).replace(base_dir,''))
    return file_list
    
def get_modified_files(base_dir,all_files,index,dir_prefix):
    new_files = []
    new_files_raw = []
    
    for filename in all_files:
        next = False
        for it in IGNORE:
            if it in filename:
                next = True
        if next:
            continue
        fc = file(base_dir+filename).read()
        if index.has_key(filename) and \
           hashlib.md5(fc).hexdigest() == index[filename]:
            continue
        else:
            new_files.append(os.path.join(dir_prefix,filename.strip('/')))
            new_files_raw.append(filename)
            
    return new_files,new_files_raw
    

def clear_cloudfront_cache(base_dir,index_file,dir_prefix='',passn=0):
    
    base_dir  = os.path.abspath(base_dir)
    all_files = get_files_from_dir(base_dir)
    
    if(os.path.exists(index_file)):
        data = file(index_file).read()
        os.unlink(index_file+'.back')
        file(index_file+'.back','w').write(data)
    else:
        data = ''
        file(index_file+'.back','w').write('')
        
    index = {}
    data = data.split('\n')
    for line in data:
        if not line: 
            continue
        path,md5 = line.split('\t#\t')
        index[path] = md5
    
    new_files,new_files_raw = get_modified_files(base_dir,all_files,index,dir_prefix)
    
    for filename in index.iterkeys():
        if filename not in all_files:
            next = False
            for it in IGNORE:
                if it in filename:
                    next = True
            if next:
                continue
            new_files.append(os.path.join(dir_prefix,filename.strip('/')))
            new_files_raw.append(filename)
    
    if new_files:
        for filename in new_files:
            print 'Modified: %s' % filename
    else:
        print 'No files were modified.\n'
        sys.exit()
		
    print '\nUploading %s files\n' % len(new_files) 
        
    inp = ''
    while (inp != 'y' and inp != 'n'):
        inp = raw_input('Upload changes to CloudFront(y/n): ')
        
        
    if inp == 'y':
        try:
            conn = CloudFrontConnection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
            k = 0
            for i in xrange(0,len(new_files),800):
                if k < passn:
                    k += 1
                    continue
                res = True
                res = conn.create_invalidation_request(AWS_CF_DISTRIBUTION_ID, new_files[i:i+900]) 
                if res:
                    print '\nInvalidation request created'
                    for filename in new_files_raw[i:i+800]:
                        fc = file(base_dir+filename).read()
                        index[filename] = hashlib.md5(fc).hexdigest()
                if k >= (passn+2):
                    print '\nToo many files. Repeat update after 15 minutes.' 
                    break
                k += 1
        except Exception,e:
            save_index(index_file,index)
            sys.exit('\nError: %s' % e)
        
        save_index(index_file,index)            
            
    
def save_index(index_file,index):
    if(os.path.exists(index_file)):
        os.unlink(index_file)
    index_fp = file(index_file,'w')
    for filename,md5 in index.iteritems():
        index_fp.write('\t#\t'.join([filename,md5])+'\n')
    index_fp.close()  
    

if __name__ == '__main__':
    print ''
    if(len(sys.argv)>1):
        base_dir = sys.argv[1]
        try:
            index_file = sys.argv[2]
        except:
            index_file = 'cloudfront_cache.ind'
        
        try:
            dir_prefix = sys.argv[3]
        except:
            dir_prefix = ''
			
        try:
            passn = int(sys.argv[4])
        except:
            passn = 0
            
        clear_cloudfront_cache(base_dir,index_file,dir_prefix,passn)
        print ''
    else:
        print 'Usage: %s data_dir [index_file] [dir_prefix]' % sys.argv[0]

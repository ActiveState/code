import arcpy as ap, os, sys, time, Tkinter as Tk, tkFileDialog
from arcpy import env

def SelectFolder(req = 'Please select a fgdb:'):
    """ Customizable folder selection dialogue, changes current directory to and returns mypath. """
    try:
        root = Tk.Tk(); root.withdraw(); mypath = tkFileDialog.askdirectory(initialdir="C:\\", title=req); root.destroy()
        os.chdir(mypath)
        return mypath
    except:
        print "Error in folder selection:", sys.exc_info()[1]; time.sleep(5);  sys.exit()

# Set workspace
gdb_type = raw_input('Do you want to open a fgdb or dbf (f/d): ')

if gdb_type == 'd':
    import glob
    dbf_folder = SelectFolder("Please select a folder or dbf's:")
    tic = time.clock()
    print dbf_folder, "DBF's:"
    for table in glob.iglob(dbf_folder+"/*.dbf"):
        numrec = int(ap.GetCount_management(table).getOutput(0))
        if numrec > 0:  print ' -{0}: {1} records'.format(table.split('\\')[1], numrec)
    print 'This arcpy cataloging took {} sec.'.format(str(time.clock()-tic)[:8])
else:
    env.workspace = SelectFolder()
    tic = time.clock()
    # Loop through root fc's:
    print "{}\nRoot FC's:".format(env.workspace)
    for fc in ap.ListFeatureClasses():
        numrec = int(ap.GetCount_management(fc).getOutput(0))
        if numrec > 0:  print ' -FC: {0}: {1} features'.format(fc, numrec)

    print 'Root tables:'
    # Loop through root tables:
    for table in ap.ListTables():
        numrec = int(ap.GetCount_management(table).getOutput(0))
        if numrec > 0:  print ' -Table: {0}: {1} records'.format(table, numrec)

    # Loop through feature datasets:
    for dataset in ap.ListDatasets():
        print 'Feature Dataset: {}'.format(dataset)
        env.workspace = dataset
        for fc in ap.ListFeatureClasses():
            numrec = int(ap.GetCount_management(fc).getOutput(0))
            if numrec > 0:  print ' -FC: {0}: {1} features'.format(fc, numrec)
    print 'This arcpy cataloging took {} sec.'.format(str(time.clock()-tic)[:8])
yorn = raw_input('Copy the lines above and paste into your document/log-file before pressing a key to quit...')

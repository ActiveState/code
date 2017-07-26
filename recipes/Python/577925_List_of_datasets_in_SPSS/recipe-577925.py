def GetListOfDatasets(): #this is because the spss fuctnion getDatasets did not work
    """Return list with opened datasets.
    """
    
    cmd = """DATASET DISPLAY."""
    handle,failcode=spssaux.CreateXMLOutput(cmd,'Dataset Display','Datasets',False)
    if failcode<>0:
        return None #something went wrong
    listDS = spssaux.GetValuesFromXMLWorkspace(tag=handle,tableSubtype='Datasets',hasCols=False)
    
    spss.DeleteXPathHandle(handle)
    return listDS

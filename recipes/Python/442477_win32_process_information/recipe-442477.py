import win32pdh
def get_processes():
    win32pdh.EnumObjects(None, None, win32pdh.PERF_DETAIL_WIZARD)
    junk, instances = win32pdh.EnumObjectItems(None,None,'Process', win32pdh.PERF_DETAIL_WIZARD)

    proc_dict = {}
    for instance in instances:
        if proc_dict.has_key(instance):
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance]=0

    proc_ids = []
    for instance, max_instances in proc_dict.items():
        for inum in xrange(max_instances+1):
            hq = win32pdh.OpenQuery() # initializes the query handle 
            try:
                path = win32pdh.MakeCounterPath( (None, 'Process', instance, None, inum, 'ID Process') )
                counter_handle=win32pdh.AddCounter(hq, path) #convert counter path to counter handle
                try:
                    win32pdh.CollectQueryData(hq) #collects data for the counter 
                    type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
                    proc_ids.append((instance, val))
                except win32pdh.error, e:
                    #print e
                    pass

                win32pdh.RemoveCounter(counter_handle)

            except win32pdh.error, e:
                #print e
                pass
            win32pdh.CloseQuery(hq) 

    return proc_ids

import win32com.client

DEBUG = 0

class MSOutlook:
    def __init__(self):
        self.outlookFound = 0
        try:
            self.oOutlookApp = \
                win32com.client.gencache.EnsureDispatch("Outlook.Application")
            self.outlookFound = 1
        except:
            print "MSOutlook: unable to load Outlook"
        
        self.records = []


    def loadContacts(self, keys=None):
        if not self.outlookFound:
            return

        # this should use more try/except blocks or nested blocks
        onMAPI = self.oOutlookApp.GetNamespace("MAPI")
        ofContacts = \
            onMAPI.GetDefaultFolder(win32com.client.constants.olFolderContacts)

        if DEBUG:
            print "number of contacts:", len(ofContacts.Items)

        for oc in range(len(ofContacts.Items)):
            contact = ofContacts.Items.Item(oc + 1)
            if contact.Class == win32com.client.constants.olContact:
                if keys is None:
                    # if we were't give a set of keys to use
                    # then build up a list of keys that we will be
                    # able to process
                    # I didn't include fields of type time, though
                    # those could probably be interpreted
                    keys = []
                    for key in contact._prop_map_get_:
                        if isinstance(getattr(contact, key), (int, str, unicode)):
                            keys.append(key)
                    if DEBUG:
                        keys.sort()
                        print "Fields\n======================================"
                        for key in keys:
                            print key
                record = {}
                for key in keys:
                    record[key] = getattr(contact, key)
                if DEBUG:
                    print oc, record['FullName']
                self.records.append(record)


if __name__ == '__main__':
    if DEBUG:
        print "attempting to load Outlook"
    oOutlook = MSOutlook()
    # delayed check for Outlook on win32 box
    if not oOutlook.outlookFound:
        print "Outlook not found"
        sys.exit(1)

    fields = ['FullName',
                'CompanyName', 
                'MailingAddressStreet',
                'MailingAddressCity', 
                'MailingAddressState', 
                'MailingAddressPostalCode',
                'HomeTelephoneNumber', 
                'BusinessTelephoneNumber', 
                'MobileTelephoneNumber',
                'Email1Address',
                'Body'
                ]

    if DEBUG:
        import time
        print "loading records..."
        startTime = time.time()
    # you can either get all of the data fields
    # or just a specific set of fields which is much faster
    #oOutlook.loadContacts()
    oOutlook.loadContacts(fields)
    if DEBUG:
        print "loading took %f seconds" % (time.time() - startTime)

    print "Number of contacts: %d" % len(oOutlook.records)
    print "Contact: %s" % oOutlook.records[0]['FullName']
    print "Body:\n%s" % oOutlook.records[0]['Body']

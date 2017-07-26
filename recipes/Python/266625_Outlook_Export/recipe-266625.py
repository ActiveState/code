"""
Copyright 2004 Mike Owens
Export data from MS Outlook using COM automation to ZODB database format.

"""

from win32com.client import Dispatch, constants
from ZODB import FileStorage, DB
import os.path

CWD = os.getcwd()
class Exporter(object):
    db = None
    app = None
    root = None
    conn = None
    def __init__ (self, filename = "out.fs"):
        storage = FileStorage.FileStorage(filename)
        self.db = DB(storage)
        self.app = Dispatch("Outlook.Application")
        self.conn = self.db.open()
        self.root = self.conn.root()
        if not self.app <> None:
            raise Exception, "Unable to create an Outlook application object"

        if not self.db <> None:
            raise Exception, "Unable to create a database instance."
            
        if not self.root <> None:
            raise Exception, "Unable to get the root of the database instance."
            
        return

    def ExportContacts (self, Folder):
        if Folder.DefaultItemType <> constants.olContactItem:
            raise Exception, "This is not a contact folder."

        contacts = []
        cnt = len(Folder.Items)
        print "Found %s contacts"%cnt
        for i in range(1, cnt + 1):
            #print i
            item = Folder.Items.Item(i)
            contact = {}
            contact["Account"] = item.Account
            #contact["Anniversary"] = item.Anniversary
            contact["assistantname"] = item.AssistantName
            contact["body"] = item.Body
            contact["business2 telephonenumber"] = item.Business2TelephoneNumber
            contact["business address"] = item.BusinessAddress
            contact["business address city"] = item.BusinessAddressCity
            contact["business address country"] = item.BusinessAddressCountry
            contact["business address postal code"] = item.BusinessAddressPostalCode
            contact["business addresspost office box"] = item.BusinessAddressPostOfficeBox
            contact["business address state"] = item.BusinessAddressState
            contact["business address street"] = item.BusinessAddressStreet
            contact["business fax number"] = item.BusinessFaxNumber
            contact["business homepage"] = item.BusinessHomePage
            contact["bussiness telephone number"] = item.BusinessTelephoneNumber
            contact["callback telephone number"] = item.CallbackTelephoneNumber
            contact["categories"] = item.Categories
            contact["companies"] = item.Companies
            contact["company last first no space"] = item.CompanyLastFirstNoSpace
            contact["company last first space only"] = item.CompanyLastFirstSpaceOnly
            contact["company main telephone number"] = item.CompanyMainTelephoneNumber
            contact["company name"] = item.CompanyName
            contact["computer network name"] = item.ComputerNetworkName
            contact["conversation index"] = item.ConversationIndex
            contact["conversation topic"] = item.ConversationTopic
            contact["customer id"] = item.CustomerID
            contact["department"] = item.Department
            contact["email1 address"] = item.Email1Address
            contact["email1 address type"] = item.Email1AddressType
            contact["email1 display name"] = item.Email1DisplayName
            contact["email1 entry id"] = item.Email1EntryID
            contact["email2 address"] = item.Email2Address
            contact["email2 address type"] = item.Email2AddressType
            contact["email2 display name"] = item.Email2DisplayName
            contact["email2 entry id"] = item.Email2EntryID
            contact["email3 address"] = item.Email3Address
            contact["email3 address type"] = item.Email3AddressType
            contact["email3 display name"] = item.Email3DisplayName
            contact["email3 entry id"] = item.Email3EntryID
            contact["entry id"] = item.EntryID
            contact["file as"] = item.FileAs
            contact["first name"] = item.FirstName
            contact["ftp site"] = item.FTPSite
            contact["full name"] = item.FullName
            contact["full name and company"] = item.FullNameAndCompany
            contact["gender"] = item.Gender
            contact["government id number"] = item.GovernmentIDNumber
            contact["hobby"] = item.Hobby
            contact["home2 telephone number"] = item.Home2TelephoneNumber
            contact["home address"] = item.HomeAddress
            contact["home address city"] = item.HomeAddressCity
            contact["home address country"] = item.HomeAddressCountry
            contact["home address postal code"] = item.HomeAddressPostalCode
            contact["home address postoffice box"] = item.HomeAddressPostOfficeBox
            contact["home address state"] = item.HomeAddressState
            contact["home address street"] = item.HomeAddressStreet
            contact["home fax number"] = item.HomeFaxNumber
            contact["home telephone number"] = item.HomeTelephoneNumber
            contact["initials"] = item.Initials
            contact["internet free busy address"] = item.InternetFreeBusyAddress
            contact["isdn number"] = item.ISDNNumber
            contact["job title"] = item.JobTitle
            contact["language"] = item.Language
            contact["lastfirst and suffix"] = item.LastFirstAndSuffix
            contact["lastfirst no space"] = item.LastFirstNoSpace
            contact["lastfirst space only"] = item.LastFirstSpaceOnly
            contact["lastfirst space only company"] = item.LastFirstSpaceOnlyCompany
            contact["lastname"] = item.LastName
            contact["lastname and first name"] = item.LastNameAndFirstName
            contact["mailing address"] = item.MailingAddress
            contact["mailing address city"] = item.MailingAddressCity
            contact["mailing address country"] = item.MailingAddressCountry
            contact["mailing address postalcode"] = item.MailingAddressPostalCode
            contact["mailing address postoffice box"] = item.MailingAddressPostOfficeBox
            contact["mailing address state"] = item.MailingAddressState
            contact["mailing address street"] = item.MailingAddressStreet
            contact["manager name"] = item.ManagerName
            contact["middle name"] = item.MiddleName
            contact["mileage"] = item.Mileage
            contact["mobile telephone number"] = item.MobileTelephoneNumber
            contact["netmeeting alias"] = item.NetMeetingAlias
            contact["nickname"] = item.NickName
            contact["netmeeting server"] = item.NetMeetingServer
            contact["office location"] = item.OfficeLocation
            contact["organization id number"] = item.OrganizationalIDNumber
            contact["other address"] = item.OtherAddress
            contact["other address city"] = item.OtherAddressCity
            contact["other address county"] = item.OtherAddressCountry
            contact["other address postal code"] = item.OtherAddressPostalCode
            contact["other address postoffice box"] = item.OtherAddressPostOfficeBox
            contact["other address street"] = item.OtherAddressStreet
            contact["other fax number"] = item.OtherFaxNumber
            contact["other telephonenumber"] = item.OtherTelephoneNumber
            contact["pager number"] = item.PagerNumber
            contact["personal homepage"] = item.PersonalHomePage
            contact["primary telephone number"] = item.PrimaryTelephoneNumber
            contact["profession"] = item.Profession
            contact["radio telephone number"] = item.RadioTelephoneNumber
            contact["referred by"] = item.ReferredBy
            contact["spouse"] = item.Spouse
            contact["subject"] = item.Subject
            contact["suffix"] = item.Suffix
            contact["telex number"] = item.TelexNumber
            contact["tty tdd Telephone number"] = item.TTYTDDTelephoneNumber
            contact["Title"] = item.Title
            contact["user1"] = item.User1
            contact["user2"] = item.User2
            contact["user3"] = item.User3
            contact["user4"] = item.User4
            contact["user certificate"] = item.UserCertificate
            contact["webpage"] = item.WebPage
            contact["yomi Company Name"] = item.YomiCompanyName
            contact["yomi first name"] = item.YomiFirstName
            contact["yomi last name"] = item.YomiLastName
            
            contacts.append(contact)
            
        foldername = Folder.Name.lower()
        self.root[foldername] = contacts
        get_transaction().commit()
        return
        
    def ExportMessages (self, Folder):
        if Folder.DefaultItemType <> constants.olMailItem:
            raise Exception, "Folder is not a mail folder."
        maillist = [] 
        cnt = len(Folder.Items)
        print "Fount %s Mail items"%cnt  
        for i in range(1, cnt + 1):
            #print i
            item = Folder.Items.Item(i)
            if not hasattr(item, "To"):
                print "Skipped non-mail message."
                continue
            message = {}
            attlist = []
            cnt = len(item.Attachments)
            if cnt:
                for i in range(1, cnt + 1):
                    try:
                        a = item.Attachments.Item(i)
                        att = {}
                        att["name"] = a.FileName
                        tpath = CWD + "\\tempfile"
                        a.SaveAsFile(tpath)
                        f = open(tpath, "r")
                        att["contents"] = f.read()
                        f.close()
                        attlist.append(att)
                    except:
                        pass
                
            message["attachments"] = attlist
            message["body"] = item.Body
            if hasattr(item, "CC"):
                message["cc"] = item.CC
            message["categories"] = item.Categories
            message["companies"] = item.Companies
            if hasattr(item, "HTMLBody"):
                message["html body"] = item.HTMLBody
            message["sender name"] = item.SenderName
            message["subject"] = item.Subject

            message["to"] = item.To
            maillist.append(message)
            
        foldername = Folder.Name.lower()
        self.root[foldername] = maillist

        get_transaction().commit()
        return
     
    def ExportNotes(self, Folder):
        if Folder.DefaultItemType <> constants.olNoteItem:
            raise Exception, "Folder is not a Notes folder."
        
        notelst = []
        cnt = len(Folder.Items)
        print "Found %s notes"%cnt
        for i in range(1, cnt + 1):
            #print i
            item = Folder.Items.Item(i)
            note = {}
            note["subject"] = item.Subject
            note["categories"] = item.Categories
            note["body"] = item.Body
            notelst.append(note)
            
        foldername = Folder.Name.lower()
        self.root[foldername] = notelst

        get_transaction().commit()
        return
    def __call__ (self, *args, **kwargs):
        ns = self.app.GetNamespace("MAPI")
        contlst = kwargs["contacts"]
        maillst = kwargs["mail"]
        notelst = kwargs["notes"]
        Folders = ns.Folders.Item(1).Folders#Usually the users folders
        if contlst:
            print "Contacts: %s"%len(contlst)
            for foldername in contlst:
                print foldername
                Folder = Folders.Item(foldername)
                if Folder:
                    self.ExportContacts(Folder)
        if maillst:
            print "Mail messages: %s"%len(maillst)
            for foldername in maillst:
                print foldername
                Folder = Folders.Item(foldername)
                if Folder:
                    self.ExportMessages(Folder)

        if notelst:
            print "Notes: %s"%len(notelst)
            for foldername in notelst:
                print foldername
                Folder = Folders.Item(foldername)
                if Folder:
                    self.ExportNotes(Folder)
        return
    def __del__ (self):
        self.root = None
        self.conn.close()
        self.conn = None
        self.db = None
        self.app = None
        return

def main ():
    export = Exporter("out.fs")
    export(contacts=["Contacts"], mail=["Inbox"], notes=["Notes"])
    return

    
if __name__ == "__main__":
    main();

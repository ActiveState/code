import webbrowser
import wmi

base_url = "http://www-307.ibm.com/pc/support/site.wss/"
support_url = base_url + "quickPath.do?sitestyle=lenovo&quickPathEntry=%s"
warranty_url = base_url + "warrantyLookup.do?sitestyle=lenovo&country=897&type=%s&serial=%s"

for csproduct in wmi.WMI().Win32_ComputerSystemProduct():
    # show information
    print "%s %s" % (csproduct.Vendor, csproduct.Version)
    print "%s %s" % (csproduct.Name, csproduct.IdentifyingNumber)
    
    # open support and warranty pages
    webbrowser.open(support_url % csproduct.Name)
    webbrowser.open(warranty_url % (csproduct.Name[:4], csproduct.IdentifyingNumber))

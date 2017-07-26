# machine.py
# ==========

import wmi
import win32net
import win32com.client
from BeautifulSoup import BeautifulSoup
from string import replace, digits, ascii_letters
import urllib, urllib2

DELL_SVCTAG_URI = 'http://support.dell.com/support/topics/global.aspx/support/my_systems_info/en/details?c=us'
DELL_SVCTAG_PARTS_URI = DELL_SVCTAG_URI + '&l=en&s=gen&~tab=2&~wsf=tabs'
DELL_UA = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]

class InvalidServiceTagException(Exception): pass

def machines_in_default_domain():
    domain_controller = win32net.NetGetDCName(None, None)
    domain_name = win32net.NetUserModalsGet(domain_controller, 2)['domain_name']
    return machines_in_domain(domain_name)

def machines_in_domain(domain_name):
    adsi = win32com.client.Dispatch("ADsNameSpaces")
    nt = adsi.GetObject('', 'WinNT:')
    result = nt.OpenDSObject('WinNT://%s' % domain_name, '', '', 0)
    result.Filter = ['computer']
    for machine in result:
        yield machine.Name

class Machine(object):

    def __init__(self, machine_name):
        self.machine = machine_name
        try:
            self.wmi_conn = wmi.WMI(self.machine)
            self.active = True
        except:
            self.active = False

    def __safe_encode(self, val):
        return ''.join([c for c in val if (c in digits or c in ascii_letters)])
    
    @property
    def _enclosure(self):
        if not hasattr(self, '__enclosure_query'):
            self.__enclosure_query = self.wmi_conn.query('Select * from Win32_SystemEnclosure')
        return self.__enclosure_query

    @property
    def _system(self):
        if not hasattr(self, '__system_query'):
            self.__system_query = self.wmi_conn.query('Select * from Win32_ComputerSystem')
        return self.__system_query

    def query_results(self, query):
        return self.wmi_conn.query(query)
    
    @property
    def service_tags(self):
        tags = [self.__safe_encode(e.SerialNumber.strip()) for e in self._enclosure]
        if not tags:
            return None
        return tags

    @property
    def model(self):
        m = [self.__safe_encode(c.Model.strip()) for c in self._system]
        if not m:
            return None
        return m[0]

    @property
    def manufacturer(self):
        mfs = [self.__safe_encode(e.Manufacturer.strip()) for e in self._enclosure]
        if not mfs:
            return None
        return mfs[0]

    @property
    def name(self):
        return self.machine
        
    @property
    def is_dell(self):
        return 'dell' in self.manufacturer.lower()

    @property
    def has_valid_dell_service_tags(self):
        tag = self.service_tags[0]
        if len(tag) == 7:
            return True

    def __normalize_dell_charset(self, page_content):
        page_content = replace(page_content, "<sc'+'ript", '')
        page_content = replace(page_content, "</sc'+'ript", '')
        t = ''.join(map(chr, range(256)))
        d = ''.join(map(chr, range(128, 256)))
        page_content = page_content.translate(t, d)
        return page_content
    
    def __retrieve_tag_information(self):
        if not self.has_valid_dell_service_tags:
            raise InvalidServiceTagException
        if not hasattr(self, '_dell_connection'):
            self._dell_cookie_jar = urllib2.HTTPCookieProcessor()
            self._dell_connection = urllib2.build_opener(self._dell_cookie_jar)
            self._dell_connection.addheaders = DELL_UA
            urllib2.install_opener(self._dell_connection)
        params = urllib.urlencode({'ServiceTag': self.service_tags[0]})
        f = self._dell_connection.open(DELL_SVCTAG_URI, params)
        page_content = f.read()
        # clean up the page
        soup = BeautifulSoup(self.__normalize_dell_charset(page_content))
        # Determine if we're still under warranty
        self._service_contracts = []
        for _contract in soup.find('table', {'class': 'contract_table'}).findAll('tr'):
            try:
                parts = _contract.findAll('td')
                if any([('contract_header' in m['class']) for m in parts]):
                    continue
                self._service_contracts.append({
                    'name': parts[0].first().string,
                    'provider': parts[1].string,
                    'start_date': parts[2].string,
                    'end_date': parts[3].string,
                    'days_remaining': int(parts[4].find(text=True)),
                })
            except:
                pass
        
        # Determine original parts
        f = self._dell_connection.open(DELL_SVCTAG_PARTS_URI)
        page_content = self.__normalize_dell_charset(f.read())
        soup = BeautifulSoup(page_content)
        self._parts = []
        for _part in soup.find('a', {'name': 'grid_1'}).nextSibling:
            try:
                fields = _part.findAll('td')
                if any([('gridTitle' in m['class']) for m in fields]):
                    continue
                self._parts.append({
                    'quantity': int(fields[0].string),
                    'part_number': fields[1].string,
                    'description': fields[2].string,
                })
            except:
                pass

    @property
    def service_contracts(self):
        if self.is_dell and not hasattr(self, '_service_contracts'):
            self.__retrieve_tag_information()
        return self._service_contracts

    @property
    def parts(self):
        if self.is_dell and not hasattr(self, '_parts'):
            self.__retrieve_tag_information()
        return self._parts
    
    @property
    def is_under_warranty(self):
        if self.is_dell:
            return any([(m['days_remaining'] > 0) for m in self.service_contracts])
        return None

# warranty_report.py

import csv
from machine import Machine, InvalidServiceTagException, machines_in_default_domain

class MachineNotDell(Exception):pass
class MachineNotActive(Exception):pass

BASE_INDENT = 4

def validate_machine(m):
    """
    We're only searching for Dell machines, so filter
    everything else out.
    """
    if not m.active:
        raise MachineNotActive
    elif not m.is_dell:
        raise MachineNotDell
    else:
        return m

def indent(spaces, text):
    return ' ' * BASE_INDENT + text

def main():
    output_writer = csv.writer(open('MachinesList.csv', 'w'))

    # write header
    output_writer.writerow([
        'Machine Name',
        'Model',
        'Service Tag(s)',
        'Under Warranty?',
        'Contract days remaining',
    ])

    for hostname in machines_in_default_domain():
        try:
            # Print Identification
            print 'Retrieving machine information for host: %s' % hostname
            m = validate_machine(Machine(hostname))
            print indent(1, '%s (%s) discovered.' % (m.model, ', '.join(m.service_tags)))

            # Print Service Contracts
            print indent(1, 'Found %d service contracts:' % len(m.service_contracts))
            for contract in m.service_contracts:
                print indent(2, '> %s (%d days remain)' % (contract['name'], contract['days_remaining']))

            # Prettify (put newline after each record)
            print ''

            # Write Output to CSV
            output_writer.writerow([
                hostname,
                m.model,
                ', '.join(m.service_tags),
                ['N','Y'][int(m.is_under_warranty)],
                max([c['days_remaining'] for c in m.service_contracts])
            ])

        # handle failures
        except MachineNotActive:
            print indent(1, 'No WMI response from %s. Continuing.\n' % hostname)
            continue
        except MachineNotDell:
            print indent(1, 'Machine was not manufactured by Dell. Continuing.\n')
            continue
        except InvalidServiceTagException:
            print indent(1, 'Machine provided an invalid service tag.')
            print indent(1, 'Unable to retrieve details. Continuing.\n')
            continue

    print 'Network scan complete.'

if __name__ == '__main__':
    main()

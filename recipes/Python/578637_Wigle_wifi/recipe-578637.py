from uuid import getnode
import re

import requests


class WigleAgent():
    
    def __init__(self, username, password):
        self.agent(username, password)
        self.mac_address()
        
    def get_lat_lng(self, mac_address=None):
        if mac_address == None:
            mac_address = self.mac_address
        if '-' in mac_address:
            mac_address = mac_address.replace('-', ':')
        try:
            self.query_response = self.send_query(mac_address)
            response = self.parse_response()
        except IndexError:
            response = 'MAC location not known'
        return response
        
    def agent(self, username, password):
        self.agent = requests.Session()
        self.agent.post('https://wigle.net/api/v1/jsonLogin',
                   data={'credential_0': username,
                         'credential_1': password,
                         'destination': '/https://wigle.net/'})
        
    def mac_address(self):
        mac = hex(getnode())
        mac_bytes = [mac[x:x+2] for x in xrange(0, len(mac), 2)]
        self.mac_address = ':'.join(mac_bytes[1:6])    
    
    def send_query(self, mac_address):
        response = self.agent.post(url='https://wigle.net/api/v1/jsonLocation',
                       data={'netid': mac_address,
                             'Query2': 'Query'})
        return response.json()
    
    def parse_response(self):
        lat = self.get_lat()
        lng = self.get_lng()
        return lat, lng
    
    def get_lat(self):
        resp_lat = self.query_response['result'][0]['locationData'][0]['latitude']
        return float(resp_lat)
    
    def get_lng(self):
        resp_lng = self.query_response['result'][0]['locationData'][0]['longitude']
        return float(resp_lng)

if __name__ == "__main__":
    wa = WigleAgent('your-username', 'your-key')
    print wa.get_lat_lng('00:1C:0E:42:79:43')

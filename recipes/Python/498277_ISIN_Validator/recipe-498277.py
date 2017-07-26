"""ISIN Validation Class

The class ISIN accepts an ISIN code and stores it - if valid - as countrycode, 
code and checkdigit.
Issuing agency and country are stored in the agencies dictionary"""

__encoding__ = "utf-16"

import string

#ISO_3166_1 coutnry codes and numbering agencies
agencies = {'BE': (u'Euronext - Brussels', u'Belgium'), 
'FR': (u'Euroclear France', u'France'), 
'BG': (u'Central Depository of Bulgaria', u'Bulgaria'), 
'VE': (u'Bolsa de Valores de Caracas, C.A.', u'Venezuela'), 
'DK': (u'VP Securities Services', u'Denmark'), 
'HR': (u'SDA - Central Depository Agency of Croatia', u'Croatia'), 
'DE': (u'Wertpapier-Mitteilungen', u'Germany'), 
'JP': (u'Tokyo Stock Exchange', u'Japan'), 
'HU': (u'KELER', u'Hungary'), 
'HK': (u'Hong Kong Exchanges and Clearing Ltd', u'Hong Kong'), 
'JO': (u'Securities Depository Center of Jordan', u'Jordan'), 
'BR': (u'Bolsa de Valores de Sao Paulo - BOVESPA', u'Brazil'), 
'XS': (u'Clearstream Banking', u'Clearstream'), 
'FI': (u'Finnish Central Securities Depository Ltd', u'Finland'), 
'GR': (u'Central Securities Depository S.A.', u'Greece'), 
'IS': (u'Icelandic Securities Depository', u'Iceland'), 
'RU': (u'The National Depository Center, Russia', u'Russia'), 
'LB': (u'Midclear S.A.L.', u'Lebanon'), 
'PT': (u'Interbolsa - Sociedade Gestora de Sistemas de Liquida\xc3\xa7\xc3\xa3o e Sistemas Centralizados de Valores', u'Portugal'), 
'NO': (u'Verdipapirsentralen (VPS) ASA', u'Norway'), 
'TW': (u'Taiwan Stock Exchange Corporation', u'Taiwan, Province of China'), 
'UA': (u'National Depository of Ukraine', u'Ukraine'), 
'TR': (u'Takasbank', u'Turkey'), 
'LK': (u'Colombo Stock Exchange', u'Sri Lanka'), 
'LV': (u'OMX - Latvian Central Depository', u'Latvia'), 
'LU': (u'Clearstream Banking', u'Luxembourg'), 
'TH': (u'Thailand Securities Depository Co., Ltd', u'Thailand'), 
'NL': (u'Euronext Netherlands', u'Netherlands'), 
'PK': (u'Central Depository Company of Pakistan Ltd', u'Pakistan'), 
'PH': (u'Philippine Stock Exchange, Inc.', u'Philippines'), 
'RO': (u'The National Securities Clearing Settlement and Depository Corporation', u'Romania'), 
'EG': (u'Misr for Central Clearing, Depository and Registry (MCDR)', u'Egypt'), 
'PL': (u'National Depository for Securities', u'Poland'), 
'AA': (u'ANNA Secretariat', u'ANNAland'), 
'CH': (u'Telekurs Financial Ltd.', u'Switzerland'), 
'CN': (u'China Securities Regulatory Commission', u'China'), 
'CL': (u'Deposito Central de Valores', u'Chile'), 
'EE': (u'Estonian Central Depository for Securities', u'Estonia'), 
'CA': (u'The Canadian Depository for Securities Ltd', u'Canada'), 
'IR': (u'Tehran Stock Exchange Services Company', u'Iran'), 
'IT': (u'Ufficio Italiano dei Cambi', u'Italy'), 
'ZA': (u'JSE Securities Exchange of South Africa', u'South Africa'), 
'CZ': (u'Czech National Bank', u'Czech Republic'), 
'CY': (u'Cyprus Stock Exchange', u'Cyprus'), 
'AR': (u'Caja de Valores S.A.', u'Argentina'), 
'AU': (u'Australian Stock Exchange Limited', u'Australia'), 
'AT': (u'Oesterreichische Kontrollbank AG', u'Austria'), 
'IN': (u'Securities and Exchange Board of India', u'India'), 
'CS': (u'Central Securities Depository A.D. Beograd', u'Serbia & Montenegro'), 
'CR': (u'Central de Valores - CEVAL', u'Costa Rica'), 
'IE': (u'The Irish Stock Exchange', u'Ireland'), 
'ID': (u'PT. Kustodian Sentral Efek Indonesia (Indonesian Central Securities Depository (ICSD))', u'Indonesia'), 
'ES': (u'Comision Nacional del Mercado de Valores (CNMV)', u'Spain'), 
'PE': (u'Bolsa de Valores de Lima', u'Peru'), 
'TN': (u'Sticodevam', u'Tunisia'), 
'PA': (u'Bolsa de Valores de Panama S.A.', u'Panama'), 
'SG': (u'Singapore Exchange Limited', u'Singapore'), 
'IL': (u'The Tel Aviv Stock Exchange', u'Israel'), 
'US': (u'Standard & Poor\xb4s - CUSIP Service Bureau', u'USA'), 
'MX': (u'S.D. Indeval SA de CV', u'Mexico'), 
'SK': (u'Central Securities Depository SR, Inc.', u'Slovakia'), 
'KR': (u'Korea Exchange - KRX', u'Korea'), 
'SI': (u'KDD Central Securities Clearing Corporation', u'Slovenia'), 
'KW': (u'Kuwait Clearing Company', u'Kuwait'), 
'MY': (u'Bursa Malaysia', u'Malaysia'), 
'MO': (u'MAROCLEAR S.A.', u'Morocco'), 
'SE': (u'VPC AB', u'Sweden'), 
'GB': (u'London Stock Exchange', u'United Kingdom')}


class ISIN(object):
    """Represents a valid ISIN number"""
    def __init__(self, isin):
        try:
            self.validate(isin)
            self.countrycode = isin[:2].upper()
            self.code = str(isin[2:-1])
            self.checkdigit = int(isin[-1])
            self.value = "%s%s%s" % (self.countrycode, self.code, self.checkdigit)
        except ISINException:
            raise
    
    def __str__(self):
    	return self.value
    
    def validate(self, isin):
        """Check the length, country code and checkdigit of the isin"""
        self.check_length(isin)
        self.check_country(isin)
        try:
            if self.calc_checkdigit(isin) != int(isin[-1]):
                raise CheckdigitError("Checkdigit '%s' is not valid" % isin[-1])
        except ValueError:
                raise CheckdigitError("Checkdigit '%s' is not valid" % isin[-1])
    
    def check_length(self, isin):
        """Raise ValueError is the isin is not 12 characters long"""
        if len(isin) != 12:
            raise LengthError('ISIN is not 12 characters')

    def check_country(self, isin):
        """Raise ValueError is the country code is not present or not 
        recognised"""
        if not isin[:2].isalpha():
            raise CountrycodeError('Country code is not present')
        if isin[:2] not in agencies.keys():
            raise CountrycodeError("Country Code '%s' is not valid" % isin[:2])

    def calc_checkdigit(self, isin):
        """Calculate and return the check digit"""
        #Convert alpha characters to digits
        isin2 = []
        for char in isin[:-1]:
            if char.isalpha():
                isin2.append((string.ascii_uppercase.index(char.upper()) + 9 + 1))
            else:
                isin2.append(char)
        #Convert each int into string and join
        isin2 = ''.join([str(i) for i in isin2])
        #Gather every second digit (even)
        even = isin2[::2]
        #Gather the other digits (odd)
        odd = isin2[1::2]
        #If len(isin2) is odd, multiply evens by 2, else multiply odds by 2
        if len(isin2) % 2 > 0:
            even = ''.join([str(int(i)*2) for i in list(even)])
        else:
            odd = ''.join([str(int(i)*2) for i in list(odd)])
        even_sum = sum([int(i) for i in even])
        #then add each single int in both odd and even
        odd_sum = sum([int(i) for i in odd])
        mod = (even_sum + odd_sum) % 10
        return 10 - mod
    	
    def agency(self):
        """Return the issuing agency name"""
        try:
            return agencies[self.value[0:2].upper()][0]
        except KeyError:
            return None
        
    def country(self):
        """Return the Country of issue"""
        try:
            return agencies[self.value[0:2].upper()][1]
        except KeyError:
            return None

class ISINException(Exception):
    pass

class CheckdigitError(ISINException):
    pass

class LengthError(ISINException):
    pass

class CountrycodeError(ISINException):
    pass

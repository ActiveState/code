import re

# Build up the regex patterns piece by piece
POSTAL_ZONES = ['AB', 'AL', 'B' , 'BA', 'BB', 'BD', 'BH', 'BL', 'BN', 'BR',
                'BS', 'BT', 'CA', 'CB', 'CF', 'CH', 'CM', 'CO', 'CR', 'CT',
                'CV', 'CW', 'DA', 'DD', 'DE', 'DG', 'DH', 'DL', 'DN', 'DT',
                'DY', 'E' , 'EC', 'EH', 'EN', 'EX', 'FK', 'FY', 'G' , 'GL',
                'GY', 'GU', 'HA', 'HD', 'HG', 'HP', 'HR', 'HS', 'HU', 'HX',
                'IG', 'IM', 'IP', 'IV', 'JE', 'KA', 'KT', 'KW', 'KY', 'L' ,
                'LA', 'LD', 'LE', 'LL', 'LN', 'LS', 'LU', 'M' , 'ME', 'MK',
                'ML', 'N' , 'NE', 'NG', 'NN', 'NP', 'NR', 'NW', 'OL', 'OX',
                'PA', 'PE', 'PH', 'PL', 'PO', 'PR', 'RG', 'RH', 'RM', 'S' ,
                'SA', 'SE', 'SG', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SR',
                'SS', 'ST', 'SW', 'SY', 'TA', 'TD', 'TF', 'TN', 'TQ', 'TR',
                'TS', 'TW', 'UB', 'W' , 'WA', 'WC', 'WD', 'WF', 'WN', 'WR',
                'WS', 'WV', 'YO', 'ZE']
POSTAL_ZONES_ONE_CHAR = [zone for zone in POSTAL_ZONES if len(zone) == 1]
POSTAL_ZONES_TWO_CHARS = [zone for zone in POSTAL_ZONES if len(zone) == 2]
THIRD_POS_CHARS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'S',
                   'T', 'U', 'W']
FOURTH_POS_CHARS = ['A', 'B', 'E', 'H', 'M', 'N', 'P', 'R', 'V', 'W', 'X',
                    'Y']
INCODE_CHARS = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'L', 'N', 'P', 'Q',
                'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
OUTCODE_PATTERN = (r'(' + 
                   r'(?:(?:' +
                   '|'.join(POSTAL_ZONES_ONE_CHAR) +
                   r')(?:\d[' +
                   ''.join(THIRD_POS_CHARS) +
                   r']|\d{1,2}))' +
                   r'|' +
                   r'(?:(?:' +
                   '|'.join(POSTAL_ZONES_TWO_CHARS) +
                   r')(?:\d[' +
                   ''.join(FOURTH_POS_CHARS) +
                   r']|\d{1,2}))' +
                   r')')
INCODE_PATTERN = (r'(\d[' +
                  ''.join(INCODE_CHARS) +
                  r'][' +
                  ''.join(INCODE_CHARS) +
                  r'])')
POSTCODE_PATTERN = OUTCODE_PATTERN + INCODE_PATTERN
STANDALONE_OUTCODE_PATTERN = OUTCODE_PATTERN + r'\s*$'

# Compile regexs
POSTCODE_REGEX = re.compile(POSTCODE_PATTERN)
STANDALONE_OUTCODE_REGEX = re.compile(STANDALONE_OUTCODE_PATTERN)

def parse_uk_postcode(postcode, strict=True, incode_mandatory=True):
    postcode = postcode.replace(' ', '').upper() # Normalize
    
    if len(postcode) > 7:
        raise ValueError('Postcode too long')
    
    # Validate postcode
    if strict:
        
        # Try for full postcode match
        postcode_match = POSTCODE_REGEX.match(postcode)
        if postcode_match:
            return postcode_match.group(1, 2)
            
        # Try for outcode only match
        outcode_match = STANDALONE_OUTCODE_REGEX.match(postcode)
        if outcode_match:
            if incode_mandatory:
                raise ValueError('Incode mandatory')
            else:
                return outcode_match.group(1), ''

        # Try Girobank special case
        if postcode == 'GIR0AA':
            return 'GIR', '0AA'
        elif postcode == 'GIR':
            if incode_mandatory:
                raise ValueError('Incode mandatory')
            else:
                return 'GIR', ''
        
        # None of the above
        raise ValueError('Invalid postcode')
        
    # Just chop up whatever we've been given.
    else:
        # Outcode only
        if len(postcode) <= 4:
            if incode_mandatory:
                raise ValueError('Incode mandatory')
            else:
                return postcode, ''
        # Full postcode
        else:
            return postcode[:-3], postcode[-3:]

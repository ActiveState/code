def cc_type(cc_number):
    """
    Function determines type of CC by the given number.
    
    WARNING:
    Creditcard numbers used in tests are NOT valid credit card numbers.
    You can't buy anything with these. They are random numbers that happen to
    conform to the MOD 10 algorithm!
    
    >>> # Unable to determine CC type
    >>> print cc_type(1234567812345670)
    None
    
    >>> # Test 16-Digit Visa
    >>> print cc_type(4716182333661786), cc_type(4916979026116921), cc_type(4532673384076298)
    Visa Visa Visa
    
    >>> # Test 13-Digit Visa
    >>> print cc_type(4024007141696), cc_type(4539490414748), cc_type(4024007163179)
    Visa Visa Visa
    
    >>> # Test Mastercard
    >>> print cc_type(5570735810881011), cc_type(5354591576660665), cc_type(5263178835431086)
    Mastercard Mastercard Mastercard
    
    >>> # Test American Express
    >>> print cc_type(371576372960229), cc_type(344986134771067), cc_type(379061348437448)
    American Express American Express American Express
    
    >>> # Test Discover
    >>> print cc_type(6011350169121566), cc_type(6011006449605014), cc_type(6011388903339458)
    Discover Discover Discover
    """
    AMEX_CC_RE = re.compile(r"^3[47][0-9]{13}$")
    VISA_CC_RE = re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$")
    MASTERCARD_CC_RE = re.compile(r"^5[1-5][0-9]{14}$")
    DISCOVER_CC_RE = re.compile(r"^6(?:011|5[0-9]{2})[0-9]{12}$")
    
    CC_MAP = {"American Express": AMEX_CC_RE, "Visa": VISA_CC_RE,
              "Mastercard": MASTERCARD_CC_RE, "Discover": DISCOVER_CC_RE}    
    
    for type, regexp in CC_MAP.items():
        if regexp.match(str(cc_number)):
            return type    
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

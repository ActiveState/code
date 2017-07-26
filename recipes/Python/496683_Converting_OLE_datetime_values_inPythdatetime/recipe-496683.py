#
# This is all you need to actually do the conversion

import datetime

OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)

def ole2datetime(oledt):
    return OLE_TIME_ZERO + datetime.timedelta(days=float(oledt))

#
#  The rest is just test code

import unittest
import pywintypes

class TestOleConversion(unittest.TestCase):

    def testEpochZero(self):
        """Tests time values compare for value of zero epoch seconds."""
        self.assertEqual(datetime.datetime(1970, 1, 1),
            ole2datetime(pywintypes.Time(0)))

    def testExamplesFromMFC(self):
        """Tests examples from the MFC DATE documentation."""
        for example in (
            #(year, month, day, hour, minute, second, OLE),
            (1899,    12,  30,    0,      0,      0, 0.0),   # 30 December 1899, midnight
            (1900,    01,  01,    0,      0,      0, 2.0),   # 1 January 1900, midnight
            (1900,    01,  04,    0,      0,      0, 5.0),   # 4 January 1900, midnight
            (1900,    01,  04,    6,      0,      0, 5.25),  # 4 January 1900, 6 A.M.
            (1900,    01,  04,   12,      0,      0, 5.5),   # 4 January 1900, noon
            (1900,    01,  04,   21,      0,      0, 5.875), # 4 January 1900, 9 P.M.
            ):
            expected = datetime.datetime(*example[:-1])
            self.assertEqual(expected, ole2datetime(example[-1]))        

if __name__ == '__main__':
    unittest.main()

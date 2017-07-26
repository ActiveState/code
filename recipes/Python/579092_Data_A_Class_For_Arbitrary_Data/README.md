## Data (A Class For Arbitrary Data)

Originally published: 2015-08-03 15:21:38
Last updated: 2015-08-03 15:22:40
Author: Alfe 

A class which is designed to be easy to use when one needs a piece of data with a minimum of source required.\n\nUsage:\n\n    shop = Data(owner="Homer", address="down the street", ice=Data(flavor="vanilla", amount=3))\n    print shop\n    Data:\n      owner = 'Homer'\n      ice = Data:\n              amount = 3\n              flavor = 'vanilla'\n      address = 'down the street'\n
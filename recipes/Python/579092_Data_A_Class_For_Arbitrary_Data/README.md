## Data (A Class For Arbitrary Data)  
Originally published: 2015-08-03 15:21:38  
Last updated: 2015-08-03 15:22:40  
Author: Alfe   
  
A class which is designed to be easy to use when one needs a piece of data with a minimum of source required.

Usage:

    shop = Data(owner="Homer", address="down the street", ice=Data(flavor="vanilla", amount=3))
    print shop
    Data:
      owner = 'Homer'
      ice = Data:
              amount = 3
              flavor = 'vanilla'
      address = 'down the street'

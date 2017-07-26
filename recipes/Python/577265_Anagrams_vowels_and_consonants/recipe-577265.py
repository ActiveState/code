#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 15/06/10
#version :2.6

from string import *
from itertools import *

"""
My program uses special functions to test, count, and extract vowels and consonants.
However,the string_check function uses isinstance() to check an objects type
and isinstance(obj, str) will be True only if obj is a str, and the 
vowel_or_Consonant is a boolean function that accept a text(string)as
an argument and which return either True or False and which you can call in
the program at any time to test every letter within a string to
determine whether it is a vowel or consonant.
Though, Vowel and Consonant functions return the count of each vowel and consonant.
and Anagrams_search function return a set of every possible combination,thus,
every possible Anagram.

"""

def my_try(arg =''):
    """ Raises an error exception if a letter is not in the alphabet or if the letter is not a space character ."""

    for item in arg:
        if item not in 'abcdefghijklmnopqrstuvwxyz ':
            raise TypeError,\
                "\n<Every letter within the text should be in the alphabet. \n"

def string_check(function):
    """
    A function which uses isinstance to determine whether an object is a string.
    """
    
    def wrapper(character):
        # string_check raises assertionError
        # if the character is not a string
        assert isinstance(character, str),\
        "Please enter a string and not %s" % (character)
        return function(character)
    return wrapper 
    
def Vowel_or_Consonant(char = ''):
    """
    A boolean function, which return either True or False
    """

    # Determine whether each letter in the text is a vowel or a
    # consonant. if it is a vowel, set test to True, otherwise, set test to false.
    for i in char:
        if str(i)in 'aeiouy':
            test = True
        else :
            test = False
        # Return the value of the test variable    
        return test
        
@string_check    
def Vowel(text = ''):
    """
    A function which return a set of vowels and the total
    number of each vowel in the text. 
    """
    
    #empty string
    string_A = ''
    for item in lower(text):
        if Vowel_or_Consonant(str(item)):
            string_A += item
            
    # sort a string_A
    char_A = sorted(string_A)
    
    # vowels' counts
    return "\n<The vowels are : %s \n" % \
           [(arg, len(list(karg))) for arg, karg  in groupby(char_A)]

@string_check           
def Consonant(text = ''):
    """
    A function which return a set of consonants and the total
    number of each consonant in the text. 
    """
    
    string_B = ''
    string_C = ''
    for arg in lower(text):
        if not Vowel_or_Consonant(str(arg)) and str(arg) in 'bcdfghjklmnpqrstvwxz':
            string_B += arg
        elif not Vowel_or_Consonant(str(arg)) and str(arg) not in 'bcdfghjklmnpqrstvwxz':
            string_C += arg
    # sort a string_B
    char_B = sorted(string_B)
    char_C = sorted(string_C)
    # consonants and others characters' Counts
    return "<The consonants are :%s \n\n<And the others characters are : %s\n" % \
           ([(arg, len(list(karg))) for arg, karg in groupby(char_B)],\
            [(arg, len(list(karg))) for arg, karg in groupby(char_C)])

def Anagrams_search(phrase = ''):
    """
    A function which return a set of every combination possible and for
    every word within a text.
    """
    #empty list
    mylist = []
    try:
        my_try(lower(phrase))
        
        for word in list(split(phrase)):
            #every possible combination for each word within the text 
            split_list = [arg for arg in permutations(lower(word),len(word))]
    
            for item in split_list:
                split_list = join(item,'')
                #append mylist 
                mylist.append(split_list)
        # a list of every possible combination including anagrams
        return "<The list of every possible combination and anagrams : %s" % \
               mylist
    #The program raise TypeError if input is not in the alphabet
    except TypeError,exception :
        print exception

if __name__ == "__main__":
  

    vowels = Vowel('Fouad Teniou')
    print vowels
    consonants = Consonant('Fouad Teniou')
    print consonants
    anagrams = Anagrams_search('Ten iou')
    print anagrams
    anagrams1 = Anagrams_search('Ten i7u')
    print anagrams1

#######################################################################

#python "C:\PythonPrograms\Anagrams-vowels-consonants.py"

#<The vowels are : [('a', 1), ('e', 1), ('i', 1), ('o', 2), ('u', 2)]

#<The consonants are :[('d', 1), ('f', 1), ('n', 1), ('t', 1)]

#<And the others characters are : [(' ', 1)].

#<The list of every possible combination and anagrams : 
#['ten', 'tne', 'etn', 'ent', 'nte', 'net', 'iou', 'iuo', 'oiu', 'oui', 'uio', 'uoi']

#<Every letter within the text should be in the alphabet.

#######################################################################
#VERSION PYTHON 3.2

#from itertools import *


#def my_try(arg =''):
#    """ Raises NegativeNumberError if number less than 0, and
#    raises ZeroNumberException if number is equal to 0."""
#    for item in arg:
#        if item not in 'abcdefghijklmnopqrstuvwxyz ':
#            raise TypeError("\n<Every letter within the text should be in the alphabet #\n")
#
#def string_check(function):
#    """
#   A function which uses isinstance to determine whether an object is a string.
#    """
#    
#    def wrapper(character):
#        # string_check raises assertionError
#        # if the character is not a string
#        assert isinstance(character, str),\
#        "Please enter a string and not %s" % (character)
#        return function(character)
#    return wrapper 
#    
#def Vowel_or_Consonant(char = ''):
#    """
#    A boolean function, which return either True or False
#    """
#
#    # Determine whether each letter in the text is a vowel or a
#    # consonant. if it is a vowel, set test to True, otherwise, set test to false.
#    for i in char:
#        if str(i)in 'aeiouy':
#            test = True
#        else :
#            test = False
#        # Return the value of the test variable    
#        return test
#        
#@string_check    
#def Vowel(text = ''):
#    """
#    A function which return a set of vowels and the total
#    number of each vowel in the text. 
#    """
#    
#   #empty string
#    string_A = ''
#    for item in str.lower(text):
#        if Vowel_or_Consonant(str(item)):
#            string_A += item
#            
#    # sort a string_A
#    char_A = sorted(string_A)
#    
#    # vowels' counts
#    return "\n<The vowels are : %s \n" % \
#           [(arg, len(list(karg))) for arg, karg  in groupby(char_A)]#
#
#@string_check           
#def Consonant(text = ''):
#    """
#    A function which return a set of consonants and the total
#    number of each consonant in the text. 
#    """
#    
#    string_B = ''
#    string_C = ''
#    for arg in str.lower(text):
#        if not Vowel_or_Consonant(str(arg)) and str(arg) in 'bcdfghjklmnpqrstvwxz':
#            string_B += arg
#        elif not Vowel_or_Consonant(str(arg)) and str(arg) not in 'bcdfghjklmnpqrstvwxz':
#            string_C += arg
#    # sort a string_B
#    char_B = sorted(string_B)
#    char_C = sorted(string_C)
#    # consonants and others characters' Counts
#    return "<The consonants are :%s \n\n<And the others characters are : %s\n" % \
#           ([(arg, len(list(karg))) for arg, karg in groupby(char_B)],\
#            [(arg, len(list(karg))) for arg, karg in groupby(char_C)])
#
#def Anagrams_search(phrase = ''):
#    """
#    A function which return set of every combination possible and for
#    every word within a text.
#    """
#    #empty list
#    mylist = []
#    try:
#        my_try(str.lower(phrase))
#        
#        for word in list(str.split(phrase)):
#            #every possible combination for each word within the text 
#            split_list = [arg for arg in permutations(str.lower(word),len(word))]
#           
#            for item in split_list:
#                
#                    
#                    split_list = ''.join(item)
#                    #append mylist
#                    
#                    mylist.append(split_list)
#        # a list of every possible combination including anagrams
#        return "<The list of every possible combination and anagrams : %s" % \
#               mylist
#    #The program raise TypeError if input is not in the alphabet
#    except TypeError as exception :
#        print(exception)
#

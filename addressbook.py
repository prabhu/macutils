#!/usr/bin/env python
# encoding: utf-8
"""
addressbook.py

Python wrapper around Mac OSX Address Book.
"""

from AddressBook import *
import sys
import os

# List of properties to be ignored.
IGNORED_PROPS = ["com.apple.ABPersonMeProperty", "ABPersonFlags", "com.apple.ABImageData",]

def getAddressBook():
    """
    Returns the addressbook instance.
    """
    return ABAddressBook.sharedAddressBook()

def all():
    """
    Returns all the people from the addressbook.
    """
    peopleList = []
    allPeople = getAddressBook().people()
    for people in allPeople:
        aperson = {}
        for prop in people.allProperties():
            if prop in IGNORED_PROPS:
                continue
            tmpval = people.valueForProperty_(prop)
            if type(tmpval) == ABMultiValueCoreDataWrapper:
                aval = [_getVal(tmpval.valueAtIndex_(i)) for i in range(0, tmpval.count())]
            else:
                aval = _getVal(tmpval)                
            if aval is not None:
                aperson[prop.lower()] = aval    
        peopleList.append(aperson)
    return peopleList

def _getVal(tmpval):
    """
    Extract value from unicode or Date object.
    """
    aval = None
    if type(tmpval) == objc.pyobjc_unicode:
        aval = tmpval
    elif issubclass(tmpval.__class__, NSDate):
        aval = tmpval.description()
    elif type(tmpval) == NSCFDictionary:
        aval = dict([(k.lower(), tmpval[k]) for k in tmpval.keys()])
    return aval
    
def main():
    all()

if __name__ == '__main__':
	main()


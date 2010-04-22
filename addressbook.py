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
IGNORED_PROPS = ["com.apple.ABPersonMeProperty", "ABPersonFlags",
                 "com.apple.ABImageData",
                 "com.apple.ABGroupMembersProperty",
                ]

def getAddressBook():
    """
    Returns the addressbook instance.
    """
    return ABAddressBook.sharedAddressBook()

def all():
    """
    Returns all the people from the addressbook.
    """
    return _clist(getAddressBook().people())

def groups():
    """
    Return groups
    """
    return _clist(getAddressBook().groups())

def me():
    """
    Returns the current logged in user.
    """
    return _clist([getAddressBook().me()])[0]

def getByUID(uid):
    """
    Returns a person or group by uid.
    """
    return _clist([getAddressBook().recordForUniqueId_(uid)])[0]

def _clist(slist):
    """
    Method to convert NSArray to python list
    """
    retList = []
    for p in slist:
        aobj = {}
        for prop in p.allProperties():
            if prop in IGNORED_PROPS:
                continue
            tmpval = p.valueForProperty_(prop)
            if type(tmpval) == ABMultiValueCoreDataWrapper:
                aval = [_getVal(tmpval.valueAtIndex_(i)) for i in range(0, tmpval.count())]
            else:
                aval = _getVal(tmpval)
            if aval is not None:
                aobj[prop.lower()] = aval
        retList.append(aobj)
    return retList

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

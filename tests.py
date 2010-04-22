#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Unit test cases for addressbook
"""
import unittest
import addressbook

class tests(unittest.TestCase):
    
    def testAll(self):
        """ Test retrieving all records """
        self.assert_(addressbook.all())
    
    def testGroups(self):
        """ Test retrieving groups """
        self.assert_(addressbook.groups())
    
    def testMe(self):
        """ Test retrieving current user """
        self.assert_(addressbook.me())
    
    def testGetByUID(self):
        """ Test getByUID """
        allr = addressbook.all()
        for a in allr:
            self.assert_(addressbook.getByUID(a['uid']))
            break

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
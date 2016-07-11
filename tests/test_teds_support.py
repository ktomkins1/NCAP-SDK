#!/usr/bin/env python
"""
test_teds
----------------------------------

Tests for `teds` module.
"""
# -*- coding: utf-8 -*-

import unittest
import ncaplite.teds_support as teds
from collections import OrderedDict

class TestTedsSupport(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_subitem(self):
        """ Test teds subitem helper function. """

        d = OrderedDict.fromkeys('ab')
        d['a'] = 1
        d['b'] = OrderedDict.fromkeys('cd')
        d['b']['c'] = 2
        d['b']['d'] = 3


        item1 = teds.subitem('a', d)
        item2 = teds.subitem('b', d)
        item3 = teds.subitem('c', d)
        item4 = teds.subitem('d', d)
        item5 = teds.subitem('e', d)

        self.assertEqual(item1, d['a'])
        self.assertEqual(item2, d['b'])
        self.assertEqual(item3, d['b']['c'])
        self.assertEqual(item4, d['b']['d'])
        self.assertEqual(item5, None)

    def test_dict_from_xml_file(self):
        """ Test reading a TEDs from an XML file into a python dict
        """
        xmlpath = 'tests/SmartTransducerTEDSMock.xml'
        my_teds = teds.teds_dict_from_file(xmlpath)
        tc_ted = teds.subitem('TransducerChannelTEDS', my_teds)
        ct = tc_ted['TransducerChannelTEDSDataBlock']['ChanType']['Value']
        channel_type = teds.ChanType(int(ct))
        expected = teds.ChanType.SENSOR
        self.assertEqual(channel_type.value, expected.value)



if __name__ == '__main__':
    unittest.main()

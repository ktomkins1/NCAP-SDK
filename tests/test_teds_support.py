#!/usr/bin/env python
"""
test_teds
----------------------------------

Tests for `teds` module.
"""
# -*- coding: utf-8 -*-

import unittest
import ncaplite.teds_support as teds

class TestTedsSupport(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_from_xml_file(self):
        """ Test reading a TEDs from an XML file into a python dict
        """
        xmlpath = 'tests/TransducerChannelMock.xml'
        my_ted = teds.teds_dict_from_file(xmlpath)
        ct = my_ted['TransducerChannelTEDS']['TransducerChannelTEDSDataBlock']['ChanType']['Value']
        channel_type = teds.ChanType(int(ct))
        expected = teds.ChanType.SENSOR
        self.assertEqual(channel_type.value, expected.value)

if __name__ == '__main__':
    unittest.main()

"""
.. module:: teds_support

   :platform: Unix, Windows
   :synopsis: Defines supporting functions the SDK uses for dealing with
   text-based TEDs

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# -*- coding: utf-8 -*-
import xmltodict
import xml.etree.ElementTree as ET
from enum import Enum
from collections import OrderedDict

class ChanType(Enum):
    """Defines TransducerChannel type."""

    SENSOR = 0
    ACTUATOR = 1
    EVENT_SENSOR = 2


class TEDSType(Enum):
    """Defines the TEDSType enumeration from Table 17 in 1451.0 ."""

    RESERVED = 0
    META_TEDS = 1
    META_ID_TEDS = 2
    CHAN_TEDS = 3
    CHAN_ID_TEDS = 4
    CAL_TEDS = 5
    CAL_ID_TEDS = 6
    EUAS_TEDS = 7
    FREQ_RESP_TEDS = 8
    TRANSFER_TEDS = 9
    COMMAND_TEDS = 10
    TITLE_TEDS = 11
    XDCR_NAME = 12
    PHY_TEDS = 13
    GEO_LOC_TEDS = 14
    UNITS_EXTENSION = 15


def teds_dict_from_file(xmlpath):
    """Get a dictionary object containing TEDS info given TEDS XML file path.

    :param xmlpath: The path to the XML ted representation
    :return: A dictionary containing the teds data
    """
    with open(xmlpath) as fd:
        teds = xmltodict.parse(fd.read(), encoding='UTF-8')
    return teds


def teds_dict_from_xml(xmltext):
    """Get a dictionary object containing TEDS info given TEDS XML string.

    :param xmltext: The TEDS XML as a string
    :return: a dictionary representation of the XML file
    """
    teds = xmltodict.parse(xmltext, encoding='UTF-8')
    return teds


def teds_text_from_file(xmlpath):
    """Get a string containing the TEDS XML text given the path to an XML file.

    :param xmlpath: path to the TEDS xml file
    :return: the raw string data from the TEDS xml file
    """
    with open(xmlpath) as fd:
        tedtext = fd.read()
    return tedtext

def teds_element_from_file(key, xmlns, xmlpath):
    """
    Get a list of specific TEDS xml elements from an xml file
    :param key: String in the format namespace:Element, eg. 'teds:TransducerChannelTEDS'
    :param xmlns: Dict which defines the namespace to use, eg. {'teds': 'http://localhost/1451HTTPAPI'}
    :param xmlpath: The path to the XML file, e.g 'tests/SmartTransducerTEDSMock.xml'
    :return: A list of the matching XML elements
    """
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    tedslist = []
    for teds in root.findall(key, xmlns):
        teds_xml_str = ET.tostring(teds, 'UTF-8', method='xml')
        tedslist.append(teds_xml_str)
    return tedslist

def subitem(key, d):
    """

    :param key:
    :param d:
    :return:
    """
    if key in d.keys(): return d[key]
    for k, v in iter(d.items()):
        if isinstance(v, OrderedDict):
            item = subitem(key,v)
            if item is not None:
                return item



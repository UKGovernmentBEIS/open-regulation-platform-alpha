#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import sys
sys.path.append('python/orp')

from orp.xmltools import recursive_walk
# import xml.etree.ElementTree as ET
from lxml import etree as ET

def test_recursive_walk_et():
    tree = ET.parse('python/orp/orp/xmltools/test/1.xml')

    elems = recursive_walk(tree.getroot())

    tlcroles = [e['attrib']['href'] for e in elems if 'TLCRole' in e['full_path'] and e['is_array_element']]

    assert tlcroles == [
        '/ontology/role/uk.A senior officer of the Department for Communities',
        '/ontology/role/uk.A senior officer of the Executive Office'
    ]

def test_recursive_walk_str():
    with open('python/orp/orp/xmltools/test/1.xml',"r") as f:
        elems = recursive_walk(f.read())
        tlcroles = [e['attrib']['href'] for e in elems if 'TLCRole' in e['full_path'] and e['is_array_element']]

        assert tlcroles == [
            '/ontology/role/uk.A senior officer of the Department for Communities',
            '/ontology/role/uk.A senior officer of the Executive Office'
        ]


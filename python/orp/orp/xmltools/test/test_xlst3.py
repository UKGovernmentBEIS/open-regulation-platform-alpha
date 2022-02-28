#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import sys
sys.path.append('python/orp')

from orp.xmltools import xslt3_transform


def test_xslt3_transform():
    with open('python/orp/orp/xmltools/test/akn2html.sef.json') as ss, open('python/orp/orp/xmltools/test/1.xml') as ak:
        success,data = xslt3_transform(ss.read(),ak.read(),prepand_path='node_modules/.bin/')
        assert success == True
        assert data != None
    with open('python/orp/orp/xmltools/test/akn2html.sef.json') as ss, open('python/orp/orp/xmltools/test/bad.xml') as ak:
        success,data = xslt3_transform(ss.read(),ak.read(),prepand_path='node_modules/.bin/')
        assert success == False



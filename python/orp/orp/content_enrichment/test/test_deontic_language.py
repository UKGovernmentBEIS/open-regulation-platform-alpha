
#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
#

from re import X
import sys
import pytest
import os
sys.path.append('python/orp')

from orp.content_enrichment.deontic_language import *

@pytest.fixture
def xml_doc():
    with open('python/orp/orp/content_enrichment/test/data/test_akomaNtoso.xml','r') as f:
        xml_doc = f.read()
    return xml_doc


def test_extract_obligations_from_string(xml_doc):
    sections = extract_obligations_from_string(xml_doc)
    #print('hello')

    sections_array = [
        (
            'You must do x, y and z:',
            {'type': 'xml',
            'sections': [{
                'extent_start': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[1]',
                'extent_end': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[1]',
                'extent_char_start': None,
                'extent_char_end': None}]}
        ),
        (
            'A protection order shall- mean x stop you from doing y',
            {'type': 'xml',
            'sections': [{
                'extent_start': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[2]',
                'extent_end': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[2]',
                'extent_char_start': None,
                'extent_char_end': None}]}
        ),
        (
            'The Secretary of State shall not make a protection order unless— you must have x or y you have one of the following- abc def ghi',
            {'type': 'xml',
            'sections': [{
                'extent_start': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[3]',
                'extent_end': '{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}act/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}body/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}section/{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subsection[3]',
                'extent_char_start': None,
                'extent_char_end': None}]}
        )

    ]

    assert sections == sections_array







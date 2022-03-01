#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import pytest
import sys

sys.path.append('python/orp')

from orp.authority_ner.new_extractAuthorities import *


@pytest.fixture
def html_doc():
    with open('python/orp/orp/authority_ner/test/test.html','r') as f:
        html_doc = f.read()
    return html_doc

@pytest.fixture
def reg_patterns():
    patterns = {"departments": r"the (Department|Ministry|Office) of(\sthe)? ([A-Z][a-z]+(?=(,)?(\s([A-Z]|and|[a-z]))))(?:(((,\s)|(\s)|(\sand\s))([A-Z][a-z]+)+)+)?(?![^<>]*>)",
            "authorities": r"the ([A-Z][a-z]+(?=\s[A-Z])((?:\s[A-Z][a-z]+)?)+) (Administration|Agency|Assembly|Authority|Board|Commission|Committee|Corporation|Council|Court|Executive|Institute|Office|Ombudsman|Parliament|Registry|Regulator|Service|Tribunal|Trust)(?=\sfor ([A-Z][a-z]+))?(?:\sfor(\s[A-Z][a-z]+)+)?(?![^<>]*>)"}
    return patterns




def test_extract_named_entities(html_doc, reg_patterns):
    sections = extract_entities_from_string(html_doc, reg_patterns)
    #print('hello')

    sections_array = [
        (
            'the Westminster City Council',
            {'type': 'html',
            'sections': [{
                'extent_start':'body/div[1]/p',
                'extent_end':'body/div[1]/p',
                'extent_char_start': 0,
                'extent_char_end': 28
                }]
            }
        ),
        (
            'the Common Council',
            {'type': 'html',
            'sections': [{
                'extent_start': 'body/div[1]/p',
                'extent_end': 'body/div[1]/p',
                'extent_char_start': 94,
                'extent_char_end': 112
                }]
            }
        ),
        (
            'the County Court',
            {'type': 'html',
            'sections': [{
                'extent_start': 'body/div[2]/span/p',
                'extent_end': 'body/div[2]/span/p',
                'extent_char_start': 0,
                'extent_char_end': 16
            }]
            }
        )
        ]

    assert sections == sections_array

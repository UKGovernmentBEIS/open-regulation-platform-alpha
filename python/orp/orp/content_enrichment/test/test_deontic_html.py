
#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
#

from re import X
import sys
import pytest
import os
sys.path.append('python/orp')

from orp.content_enrichment.deontic_language_html import *

@pytest.fixture
def xml_doc():
    with open('python/orp/orp/content_enrichment/test/data/test_html.html','r') as f:
        xml_doc = f.read()
    return xml_doc


def test_extract_obligations_from_string(xml_doc):
    sections = extract_obligations_from_string(xml_doc, by_section=True)
    #print('hello')

    sections_array = [
        (
            'You must do x, y and z:',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[1]/div/p',
                'extent_end': 'body/article/div[4]/section/section[1]/div/p',
                'extent_char_start': None,
                'extent_char_end': None}]}
        ),
        (
            'A protection order shall- mean x stop you from doing y',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[2]/div[1]/p',
                'extent_end': 'body/article/div[4]/section/section[2]/div[1]/p',
                'extent_char_start': None,
                'extent_char_end': None},
                {
                'extent_start': 'body/article/div[4]/section/section[2]/div[2]/div/p',
                'extent_end': 'body/article/div[4]/section/section[2]/div[2]/div/p',
                'extent_char_start': None,
                'extent_char_end': None
                },
                {
                'extent_start': 'body/article/div[4]/section/section[2]/div[3]/div/p',
                'extent_end': 'body/article/div[4]/section/section[2]/div[3]/div/p',
                'extent_char_start': None,
                'extent_char_end': None

                }]}
        ),
        (
            'The Secretary of State shall not make a protection order unless— you must have x or y you have one of the following- abc def ghi',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[3]/div[1]/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[1]/p',
                'extent_char_start': None,
                'extent_char_end': None
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[2]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[2]/div/p',
                'extent_char_start': None,
                'extent_char_end': None,
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[3]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[3]/div/p',
                'extent_char_start': None,
                'extent_char_end': None,
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[4]/div[1]/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[4]/div[1]/p',
                'extent_char_start': None,
                'extent_char_end': None
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[4]/div[2]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[4]/div[2]/div/p',
                'extent_char_start': None,
                'extent_char_end': None
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[4]/div[3]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[4]/div[3]/div/p',
                'extent_char_start': None,
                'extent_char_end': None
                },
                {
                'extent_start': 'body/article/div[4]/section/section[3]/div[5]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[5]/div/p',
                'extent_char_start': None,
                'extent_char_end': None
                }
                ]}
        )]

    assert sections == sections_array


def test_extract_obligations_from_string(xml_doc):
    sections = extract_obligations_from_string(xml_doc, by_section=False)
    #print('hello')

    sections_array = [
        (
            'You must do x, y and z:',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[1]/div/p',
                'extent_end': 'body/article/div[4]/section/section[1]/div/p',
                'extent_char_start': None,
                'extent_char_end': None}]}
        ),
        (
            'A protection order shall-',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[2]/div[1]/p',
                'extent_end': 'body/article/div[4]/section/section[2]/div[1]/p',
                'extent_char_start': None,
                'extent_char_end': None}]}
        ),
        (
            'The Secretary of State shall not make a protection order unless—',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[3]/div[1]/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[1]/p',
                'extent_char_start': None,
                'extent_char_end': None
                }]}
        ),
        (
            'you must have x',
            {'type': 'xml',
            'sections': [{
                'extent_start': 'body/article/div[4]/section/section[3]/div[2]/div/p',
                'extent_end': 'body/article/div[4]/section/section[3]/div[2]/div/p',
                'extent_char_start': None,
                'extent_char_end': None
                }]}
        )
        ]

    assert sections == sections_array
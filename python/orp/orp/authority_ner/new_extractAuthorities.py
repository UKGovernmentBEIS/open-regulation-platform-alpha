#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
# Alastair McKinley (a.mckinley@analyticsengines.com)
# Liam Brannigan (l.brannigan@analyticsengines.com)
#

from lxml import etree as ET
import re

def checkInnerHTML(element):
    children = element.getchildren()
    if len(children) > 0:
        resultStr = element.text or ''
        for e in children:
            if e.text:
                resultStr += ET.tostring(e, encoding='unicode')
        finalStr = " ".join(resultStr.split())
    else:
        finalStr = " ".join(element.text.split())

    return finalStr

def get_htmlTextExtentMap(html):
    tree = ET.HTML(html)
    etree = ET.ElementTree(tree)
    textExtents = []
    for element in etree.iter():
        textMap = {}
        if element.text:
            if element.tag == 'p':
                text = checkInnerHTML(element)
            else:
                text = " ".join(element.text.split())
            if text != "":
                textMap['raw_text'] = text
                path = etree.getelementpath(element)
                textMap['extent_path'] = path
                textExtents.append(textMap)
    return textExtents


def get_regexMatchLocation(regex, htmlTextExtentMap):
    named_entities = {}
    for extent in htmlTextExtentMap:
        iter = re.finditer(regex, extent['raw_text'])
        for m in iter:
            if m.group() not in named_entities.keys():
                named_entities[m.group()] = [{'extent_start': extent['extent_path'], 'extent_end': extent['extent_path'], 'extent_char_start': m.start(0), 'extent_char_end': m.end(0)}]
            else:
                named_entities[m.group()].append({'extent_start': extent['extent_path'], 'extent_end': extent['extent_path'], 'extent_char_start': m.start(0), 'extent_char_end': m.end(0)})

    postgres_namedEntities = []

    for entity, extents in named_entities.items():
        extent = {"type": "html"}
        data = entity
        extent['sections'] = extents
        postgres_namedEntities.append((data,extent))

    return postgres_namedEntities


def extract_entities_from_string(html, patterns: dict):

    entityDict = {}
    all_entities = []

    for entity in patterns:
        entityDict[entity] = {'pattern': re.compile(patterns[entity])}
        entityDict[entity]['htmlExtentMap'] = get_htmlTextExtentMap(html)
        entityDict[entity]['matches'] = get_regexMatchLocation(entityDict[entity]['pattern'], entityDict[entity]['htmlExtentMap'])

    for entity in entityDict:
        all_entities.append(entityDict[entity]['matches'])

    all_entities_flattened = [item for sublist in all_entities for item in sublist]

    return all_entities_flattened






# html_file = "data/debug.html"
# html_2 = "python/orp/orp/authority_ner/test/ukla_1994.html"
# html_3 = "python/orp/orp/authority_ner/test/test.html"



# patterns = {"departments": r"the (Department|Ministry|Office) of(\sthe)? ([A-Z][a-z]+(?=(,)?(\s([A-Z]|and|[a-z]))))(?:(((,\s)|(\s)|(\sand\s))([A-Z][a-z]+)+)+)?(?![^<>]*>)",
#             "authorities": r"the ([A-Z][a-z]+(?=\s[A-Z])((?:\s[A-Z][a-z]+)?)+) (Administration|Agency|Assembly|Authority|Board|Commission|Committee|Corporation|Council|Court|Executive|Institute|Office|Ombudsman|Parliament|Registry|Regulator|Service|Tribunal|Trust)(?=\sfor ([A-Z][a-z]+))?(?:\sfor(\s[A-Z][a-z]+)+)?(?![^<>]*>)"}

# with open(html_2, 'r') as file:
#     html = file.read()

# test = extract_entities_from_string(html, patterns)
# print('hello')



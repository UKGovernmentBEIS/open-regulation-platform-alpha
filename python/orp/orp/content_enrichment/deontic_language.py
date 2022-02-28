#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
#

""" How classification and assessment works for deontic language:
If a keyterm is found within a piece of text  ['shall', 'should', 'must', 'required', 'may'],
then the entire section (each section in akoma ntoso is defined by an 'eId' tag) is extracted
as a deontic extent.

Assessment works by an expert marking up sections of text they deem deontic,
the deontic_evaluation tool takes the same approach as the original classification method
and extracts the section xpath that the expert marked up text is found within. These sections 
are then regarded as 'positive' and all other sections in the document are deemed 'negative'.
Assessing the perfomance of the classification is carried out by scanning through the sections of the
original xml and checking for positive and negative cases as defined by the expert markup:

true positive = both the expert and alogorihtm have labelled the section as deontic
false positive = only the algorithm has labelled te section as deontic
true negative = neither the expert or the algorithm have labelled the section as deontic
false negative = only the expert have marked the section as deontic
"""


from lxml import etree as ET
import re
# import pandas as pd
# from pathlib import Path

# dataPath = Path("python/orp/orp/content_enrichment/data")
# processedPath = Path("python/orp/orp/assessments/deontic_language/data/algo_markups")

def get_namespace(element_tag):
    m = re.match(r'\{(.*)\}', element_tag)
    return m.group(1) if m else None

def tag_extract(full_tag):
    m = re.match('^{.*}(.*)$',full_tag)
    if m:
        return m.group(1)
    else:
        return None

def tag_extract_full_path(path):
    tag_list = []
    path_edited = path.replace("/{", "---{")
    location = path_edited.split('---')
    for item in location:
        tag = tag_extract(item)
        ns_tag = "ns:" + tag
        tag_list.append(ns_tag)
    new_path = '/'.join(tag_list)

    return new_path

def extract_obligations_from_string(doc_text):
    tree = ET.fromstring(doc_text)
    etree = ET.ElementTree(tree)
    if 'akomaNtoso' in tree.tag:
        namespace = get_namespace(tree.tag)
        nsmap = {'ns': namespace}
        return extract_obligations(tree=etree, nsmap=nsmap)
    else:
        raise ValueError(' Not akomaNtoso format')

def check_containment(traversed_elements, current_element):
    contained = False
    if current_element in traversed_elements:
        contained = True
    for element in traversed_elements:
        child_elements = element.getchildren()
        if current_element in child_elements:
            contained = True
            break
    return contained

#TODO: Need to ignore anything that falls under 'interpretation'

def extract_obligations(tree, nsmap, terms = ['shall','should', 'must', 'required', 'may not', 'may only',
    'commits an offence', 'liable', 'duty to', 'failure to comply', 'penalty imposed',
    'impose a penalty', 'enable the participant'], excluded_terms = ['shall be inserted','shall be cited','shall be substituted'],
    by_section = True): # TODO: may want to specify the terms when calling pipeline
    """ extacts text elements from akomaNtoso xml-formatted file given a list of key terms """
    traversed_elements = []
    obligations = []
    p_tag = "{" + nsmap['ns'] + "}" + "p"
    header_tag = "{" + nsmap['ns'] + "}" + "heading"

    body = tree.find(f'.//ns:body', namespaces = nsmap)
    for element in body.iter():
        # check this element isn't contained within one that we've already extracted from
        if check_containment(traversed_elements, element) == False:
            if element.tag == p_tag or element.tag == header_tag: # means that we're in a text element or heading
                text = ''.join(element.itertext()) # itertext overcomes issues when there's a tag mid element, because we are in a <p> element there should be no children
                if any(term.lower() in text.lower() for term in terms):
                    stripped_text = text.lower() # check to make sure it doesn't only contain key term as part of exclusion term (quicker to do this here as opposed to outside this if statement)
                    for phrase in excluded_terms:
                        stripped_text = stripped_text.replace(phrase, '')
                    if any(term.lower() in stripped_text.lower() for term in terms):
                        if by_section == True:
                            parent_elements = element.iterancestors() # get list of parent elements
                            element_text_list = []
                            obligation_dict = {}
                            for p_element in parent_elements: #
                                if 'eId' in p_element.attrib: # eId attribute signals a section tag
                                    if check_containment(traversed_elements, p_element) == False:
                                        traversed_elements.append(p_element)
                                        for text_element in p_element.findall('.//ns:p', namespaces= nsmap): # TODO: p tag is where text is found but could be made more dynamic?
                                            text = ' '.join(text_element.itertext()) # itertext overcomes the issue with subtags within text elements
                                            element_text_list.append(text)
                                        obligation_dict['text'] = ' '.join(element_text_list)
                                        full_path = tree.getelementpath(p_element) # getelementpath extracts xpath with the namespace
                                        obligation_dict['section_paths'] = [full_path]
                                        obligations.append(obligation_dict)
                                        break
                                    else:
                                        break
                        else:
                            full_path = tree.getelementpath(element) # getelementpath extracts xpath with the namespace
                            obligation_dict['section_paths'] = [full_path]
                            obligation_dict['text'] = text
        else:
            print('contained')

    obligations_for_postgres = []
    for oblig in obligations: # transform into structure accepted by postgres
        extent = {"type" : "xml"}
        data = oblig['text']
        extent['sections'] =  [{
            'extent_start' : s,
            'extent_end' : s,
            'extent_char_start' : None,
            'extent_char_end' : None,
        } for s in oblig['section_paths']]


        obligations_for_postgres.append((data,extent))

    return obligations_for_postgres

# if __name__ == "__main__":
#     docs = dataPath.glob("*.xml")
#     for docPath in docs:
#         name = docPath.name + '_new'
#         with open(docPath, "r") as f:
#             xml_doc = f.read()
#             obligations = extract_obligations_from_string(xml_doc)
#             obligation_df = pd.DataFrame(obligations)
#             obligation_df.to_csv(f"{processedPath}/{name}.csv")

# testfile = "/home/lstephens/git_projects/orp-alpha-gh-mirrored/data/legislation/ukla/1996/2.xml"
# with open(testfile,'r') as f:
#         xml_doc = f.read()

# extract_obligations_from_string(xml_doc)


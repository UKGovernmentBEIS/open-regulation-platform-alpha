#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
# Lauren Stephens (l.stephens@analyticsengines.com)
#

# import xml.etree.ElementTree as ET
from lxml import etree as ET
import re
from collections import Counter


def tag_extract(full_tag):
    m = re.match("^{.*}(.*)$", full_tag)
    if m:
        return m.group(1)
    else:
        return None


def recursive_walk(parent, parent_path=""):
    ret = []

    if isinstance(parent, str):
        parent = ET.fromstring(parent)

    multi = Counter([tag_extract(c.tag) for c in parent])

    multi_count = {k: 0 for k in multi}

    for child in parent:
        tag = tag_extract(child.tag)
        is_multi = True if multi[tag] > 1 else False
        multi_i = multi_count[tag]
        multi_count[tag] += 1
        # text = child.text if re.sub('\s*','',(child.text or '')) else None
        text = (
            (" ".join(child.itertext()))
            if re.sub("\s*", "", (child.text or ""))
            else None
        )
        full_path = parent_path + "/" + tag + (f"[{multi_i}]" if is_multi else "")
        if is_multi:
            multi_path = f"{parent_path}/{tag}[*]"
            ret.append(
                {
                    "full_path": multi_path,
                    "is_array_element": True,
                    "text": text if text else None,
                    "tag": tag,
                    "attrib": child.attrib,
                }
            )
        ret.append(
            {
                "full_path": full_path,
                "is_array_element": False,
                "text": text if text else None,
                "tag": tag,
                "attrib": child.attrib,
            }
        )
        ret.extend(recursive_walk(child, full_path))
    return ret

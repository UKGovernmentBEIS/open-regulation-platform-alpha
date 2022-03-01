
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import subprocess
import tempfile
import os

def xslt3_transform(stylesheet,xml,prepand_path=None):
    ss_f,ss_fn = tempfile.mkstemp(suffix='.sef.json')
    xml_f,xml_fn = tempfile.mkstemp(suffix='.xml')
    html_f,html_fn = tempfile.mkstemp(suffix='.html')

    os.write(ss_f,str(stylesheet).encode())
    os.write(xml_f,str(xml).encode())

    os.close(ss_f)
    os.close(xml_f)
    os.close(html_f)

    if prepand_path:
        exec_path = os.path.join(prepand_path,'xslt3')
    else:
        exec_path = 'xslt3'

    result = subprocess.run([exec_path,f'-xsl:{ss_fn}',f'-s:{xml_fn}',f'-o:{html_fn}','-t'],capture_output=True)

    if result.returncode == 0:
        with open(html_fn,"r") as f:
            return True,f.read()
    else:
        return False,f"""
            stderr:{result.stderr}
            stdout:{result.stdout}
        """

# def akomaNtoso_to_html()
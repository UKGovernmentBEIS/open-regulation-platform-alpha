
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests
import backoff
from typing import Any,List,Tuple
import csv
import os

types = [
    'nisi',
    #'nisro',
    'ukpga',
    'ukla',
    'asp',
    'asc',
    'anaw',
    'mwa',
    'ukcm',
    'nia',
    'uksi',
    'wsi',
    'ssi',
    'nisr',
    'ukmo',
    'uksro'
]

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
def try_get(url):
    import time
    import random
    time.sleep(random.random()*2)
    return requests.get(url)


def get_legislation(year: int = None,type: str = None, number: int = None) -> Tuple[int,str]:
    # for n in range(1,number+1):
    url = f"https://www.legislation.gov.uk/{type}/{year}/{n}/made/data.akn"
    resp = try_get(url)
    if resp:
        print(f"got doc for {y} type {t} number {n}")
        return resp.status_code,resp.text
    else:
        print(f"no doc for {y} type {t} number {n}")
        return resp.status_code,None

def doc_exists(year: int = None,type: str = None, number: int = None) -> bool:
    return os.path.exists(f"data/{t}/{y}/{n}.xml")

if __name__ == '__main__':
    number = 700
    # for y in range(1970,2022):
    for y in [2002,2012]:
        print(f'getting {y} examples')
        # for t in types:
        for t in ['uksi']:
            print(f'getting {y} examples for type {t}')
            dir_name = f"data/{t}/{y}"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)


            consecutive_errors_this_year_type = 0
            for n in range(1,number+1):
                base = f"data/{t}/{y}/{n}"
                fn = f"data/{t}/{y}/{n}.xml"
                error = f"data/{t}/{y}/{n}.error"

                if os.path.exists(error):
                    print(f"{error} exists")
                    consecutive_errors_this_year_type += 1
                    continue

                if not os.path.exists(fn):
                    code,l = get_legislation(year=y,type=t,number=n)
                    if code == 200:
                        consecutive_errors_this_year_type = 0
                        with open(f"{fn}","w") as f:
                            f.write(l)
                    else:
                        with open(f"{error}","w") as f:
                            f.write(str(code))
                            consecutive_errors_this_year_type += 1
                else:
                    consecutive_errors_this_year_type = 0
                    print(f"{fn} exists")

                if consecutive_errors_this_year_type > 50:
                    print(f"more than 50 consectutive errors for this {y} - {t} giving up")
                    break
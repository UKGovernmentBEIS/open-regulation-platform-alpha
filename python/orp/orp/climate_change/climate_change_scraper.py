# Initial version of climate change scraper
# Parked for now until further notice

#
# Copyright (C) Analytics Engines 2021
# Lauren Stephens (l.stephens@analyticsengines.com)
# Alastair McKinley (a.mckinley@analyticsengines.com)
# Matt Gourley (m.gourley@analyticsengines.com)
#

from bs4 import BeautifulSoup
from re import sub
import requests
import re
import json

CLIMATE_CHANGE_URL = 'https://www.gov.uk/guidance/climate-change'

def parseData():
    page = getUrl(CLIMATE_CHANGE_URL)
    soup = BeautifulSoup(page, parser)
    title = getTitle(soup)
    subject = getSubject(soup)
    category = getCategory(soup)
    author = getAuthor(soup)
    creationDate = getCreationDate(soup)
    modDate = getModDate(soup)
    contents = getContents(soup)
    content = getTextForContents(contents,soup)

    data = createJson(title,subject,category,author,creationDate,modDate,content)
    with open('data/climate_change.json', 'w') as f:
        json.dump(data,f)

def getUrl(url):
    req = requests.get(
        url,
        headers={'User-Agent': 'Mozilla/5.0'})
    return req.content

def createJson(title,subject,category,author,creationDate,modDate,content):
    data_list = [('title', title), ('subject', subject),
    ('category', category), ('author', author), ('creationDate', creationDate),
    ('modDate', modDate), ('content', content)]
    data = {k: v for k, v in data_list}
    return data

def getTitle(soup):
    title = soup.find('meta', property="og:title")
    title = title["content"] if title else "No meta title given"
    return title

def getSubject(soup):
    desc = soup.find('meta', property="og:description")
    desc = desc['content'] if desc else "No meta description given"
    return desc

def getCategory(soup):
    category = soup.find('meta', attrs={'name': 'govuk:themes'})
    category = category['content'] if category else "No meta category given"
    category = sub(r"(-)+", " ", category).title()
    return category

def getAuthor(soup):
    pub = soup.find('dt',class_='gem-c-metadata__term',text="From:").findNext('dd').findNext('a').string
    return pub

def getCreationDate(soup):
    pubDate = soup.find("dt",class_='gem-c-metadata__term',text="Published").findNext('dd').string
    return pubDate

def getModDate(soup):
    upd = soup.find("dt",class_='gem-c-metadata__term',text="Last updated").findNext('dd').find(text=True)
    upd = re.sub(r'[^a-zA-Z0-9 ]+', '',upd).strip()
    return upd

def getContents(soup):
    contentList = []
    contents = soup.find_all('li',class_='gem-c-contents-list__list-item gem-c-contents-list__list-item--dashed')
    for content in contents:
        content = content.find('a',class_="gem-c-contents-list__link govuk-link govuk-link--no-underline").text
        contentList.append(content)
    return contentList

def getTextForContents(contents,soup):
    dct = {}
    for content in contents:
        dct[content] = {'text': [], 'paragraphMetadata': '', 'revisionDate': ''}
        contentText = soup.find('h2',text=content)
        for sib in contentText.next_siblings:
            if 'Paragraph:' in sib.text:
                dct[content]['paragraphMetadata'] = sib.text
            elif 'Revision date' in sib.text:
                date = sub("Revision date: ", "", sib.text)
                fmtDate = sub(" ", "/", date)
                dct[content]['revisionDate'] = fmtDate
                break
            elif sib.text != '\n':
                dct[content]['text'].append(sib.text)
    return dct

if __name__ == '__main__':
    parser = 'html.parser'
    climate_change = parseData()
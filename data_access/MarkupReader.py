

import xml.etree.ElementTree as ET
root = ET.parse('Historical_Present.xml').getroot()

verses= {}

for type_tag in root.findall('references/'):
    verse = type_tag.get('verse')
    if verse.__contains__("JHN"):
        if verses.__contains__(verse):
            verses[verse]+=1
        else:
            verses[verse] = 1
print(verses)

def MarkUpContainsHistoricalPresent(string):
    if not verses.__contains__(string):
        return 0
    return verses[string]


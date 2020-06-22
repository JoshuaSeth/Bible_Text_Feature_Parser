import xml.etree.ElementTree as ET
root = ET.parse('Historical_Present.xml').getroot()

verses= []

for type_tag in root.findall('references/'):
    verse = type_tag.get('verse')
    if verse.__contains__("JHN"):
        verses.append(verse)
print(verses)

def MarkUpContainsHistoricalPresent(string):
    count = 0
    for verse in verses:
        if string == verse:
            count+=1
    return count
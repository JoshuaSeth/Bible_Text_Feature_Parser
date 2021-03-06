import xml.etree.ElementTree as ET
import json



compoundWords= []
foreignWordsCodes = {}
names = []

with open('female-names.json') as json_file:
    data = json.load(json_file)
    for p in data:
        names.append(p)
with open('male_names.json') as json_file:
    data = json.load(json_file)
    for p in data:
        names.append(p)


def AddToForeignList():
    if not(names.__contains__(type_tag.find('kjv_def').text.replace("-", "").replace(":", "").replace(" ", "").replace(".", ""))):
        strongsWord = type_tag.find('greek').get('unicode')
        strongsCode = type_tag.find('strongs').text
        foreignWordsCodes[strongsCode] = strongsWord
        print(strongsWord + " " + deriv.text + str(strongsCode))

root = ET.parse('strongsgreek.xml').getroot()
for type_tag in root.findall('entries/'):
    deriv = type_tag.find('strongs_derivation')
    if deriv is not None:
        if deriv.text.__contains__("compound"):
            strongsWord = type_tag.find('greek').get('unicode')
            compoundWords.append(strongsWord)


        if deriv.text.__contains__("foreign"):
            AddToForeignList()
        if deriv.text.__contains__("Hebrew"):
            AddToForeignList()
        if deriv.text.__contains__("Chaldee"):
            AddToForeignList()
        if deriv.text.__contains__("Latin"):
            AddToForeignList()
        # if deriv.text.__contains__("uncertain origin"):
        #     AddToForeignList()
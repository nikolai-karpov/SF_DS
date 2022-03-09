import xml.etree.ElementTree as ET

events=("start", "end", "start-ns", "end-ns")
for event, elem in ET.iterparse("homework/data/turbo_yandex.xml", events=events):
    #print('event: ', event)
    #print('elem: ', elem)
    pass
    
tree = ET.parse("homework/data/turbo_yandex.xml")
root = tree.getroot()

for child in root:
	print('child.tag: ', child.tag, 'child.attrib:', child.attrib)
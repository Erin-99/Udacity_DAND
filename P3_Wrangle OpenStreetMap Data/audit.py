import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "shanghai_china.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

chinese_words = re.compile(ur'[\u4e00-\u9fa5]')

num_words = re.compile(r'\d+')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",'Market','Zone', 'District','Mall',
            "Trail", "Parkway", "Commons","Block","Garden",'Highway','S308','Dong','Park','West']

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            'Ave':'Avenue',
            'Rd':'Road',
            'Rd.':'Road',
            'road':'Road',
            'rd':'Road',
            'lu':'Road',
            'Ave.':'Avenue',
            'Hwy.':'Highway',
            'lu':'Road',
            'Lu':'Road',
            'Rode':'Road',
           'Raod':'Road',
           'avenue':'Avenue',
           'Rd,':'Road',
           'garden':'Garden',
           'Ave.':'Avenue',
           'xiang':'Lane',
           'Xiang':'Lane',
           'Gonglu':'Parkway',
           'nanjing':'Nanjing Road',
           'hehuaxing':'Hehuaxing Road',
           'xingjianlu':'Xingjian Road',
           'JieQu':'Block',
           'Siping':'Siping Road',
           'Xiangyang':'Xiangyang Road',
           'Wukang':'Wukang Road'
            
            }

def is_chinese(uchar):

    #whether unicode is Chinese

    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':

            return True

    else:

            return False

def audit_street_type(street_types, street_name):
    # Find the last word of street_name
    m = street_type_re.search(street_name)
    #whether the street_name is Chinese or English, clean the English street_name
    if m and not is_chinese(street_name):
        #street_name=street_name.split('(')[0].strip()
        street_name=street_name.split(',')[0].strip()
        street_type = m.group()
        if street_type not in expected:
            #check whether there is a roomnumber
            if num_words.search(street_name) or "(" in street_name:
                street_name=street_name.split(' ')[:-1]
                street_name=" ".join(street_name)
                audit_street_type(street_types,street_name)
            else:
                street_types[street_type].add(street_name)

                
                
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, 'rb')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:  
        street_type = m.group()
        if street_type in mapping.keys():
            print 'Before: ', name
            name = re.sub(m.group(), mapping[m.group()], name)
            print 'After: ', name
    
    return name


st_types = audit(OSMFILE)
# print st_types
#print len(st_types)
#for st_type,ways in st_types.iteritems():
    #print st_type,
    #for e in ways:
        #print e
#print dict(st_types)
for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, '=>',better_name
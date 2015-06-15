
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import re
import json
from csv import reader


# In[2]:

mutual_fans_header = ['country_A','role_A','pageid_A','name_A','fan_count_A','country_B','role_B','pageid_B','name_B','fan_count_B','mutual_fans']


# In[3]:

network = {'nodes':[],'links':[]}
nodes = {}
threshold = 0.005
ifh = open('worldleaders_2015_v2_mutual_fans.csv','r')
first = True
filereader = reader(ifh, delimiter=',', quotechar='"')
for row in filereader:
    if first:
        first = False
        continue
    assert len(row) == len(mutual_fans_header)
    row_dict = dict(zip(mutual_fans_header, row))
    link_jaccard = float(row_dict['mutual_fans'])/(float(row_dict['fan_count_A']) + float(row_dict['fan_count_B']) - float(row_dict['mutual_fans']))
    if link_jaccard < threshold:
        continue
    if row_dict['pageid_A'] not in nodes:
        nodeA = {'country':row_dict['country_A'],
                 'role':row_dict['role_A'],
                 'pageid':row_dict['pageid_A'],
                 'name':row_dict['name_A'],
                 'fan_count':float(row_dict['fan_count_A']),
                 'position':len(network['nodes'])}
        nodes[row_dict['pageid_A']] = nodeA
        network['nodes'].append(nodeA)
    if row_dict['pageid_B'] not in nodes:
        nodeB = {'country':row_dict['country_B'],
                 'role':row_dict['role_B'],
                 'pageid':row_dict['pageid_B'],
                 'name':row_dict['name_B'],
                 'fan_count':float(row_dict['fan_count_B']),
                 'position':len(network['nodes'])}
        nodes[row_dict['pageid_B']] = nodeB
        network['nodes'].append(nodeB)
    link = {'source':nodes[row_dict['pageid_A']]['position'],
            'target':nodes[row_dict['pageid_B']]['position'],
            'value':float(row_dict['mutual_fans']),
            'jaccard':link_jaccard}
    network['links'].append(link)


# In[4]:

with open('all_govt_page_network.json','w') as ofh:
    json.dump(network, ofh)


# In[18]:

leader_network = {'nodes':[],'links':[]}
nodes = {}
threshold = 0.005
ifh = open('worldleaders_2015_v2_mutual_fans.csv','r')
first = True
filereader = reader(ifh, delimiter=',', quotechar='"')
for row in filereader:
    if first:
        first = False
        continue
    assert len(row) == len(mutual_fans_header)
    row_dict = dict(zip(mutual_fans_header, row))
    if row_dict['role_A'] in ['Leader','Other Leader'] and row_dict['role_B'] in ['Leader','Other Leader']:
        link_jaccard = float(row_dict['mutual_fans'])/(float(row_dict['fan_count_A']) + float(row_dict['fan_count_B']) - float(row_dict['mutual_fans']))
        if link_jaccard < threshold:
            continue
        if row_dict['pageid_A'] not in nodes:
            nodeA = {'country':row_dict['country_A'],
                     'role':row_dict['role_A'],
                     'pageid':row_dict['pageid_A'],
                     'name':row_dict['name_A'],
                     'fan_count':float(row_dict['fan_count_A']),
                     'position':len(leader_network['nodes'])}
            nodes[row_dict['pageid_A']] = nodeA
            leader_network['nodes'].append(nodeA)
        if row_dict['pageid_B'] not in nodes:
            nodeB = {'country':row_dict['country_B'],
                    'role':row_dict['role_B'],
                     'pageid':row_dict['pageid_B'],
                     'name':row_dict['name_B'],
                     'fan_count':float(row_dict['fan_count_B']),
                     'position':len(leader_network['nodes'])}
            nodes[row_dict['pageid_B']] = nodeB
            leader_network['nodes'].append(nodeB)
        
        link = {'source':nodes[row_dict['pageid_A']]['position'],
                'target':nodes[row_dict['pageid_B']]['position'],
                'value':float(row_dict['mutual_fans']),
                'jaccard':link_jaccard}
        leader_network['links'].append(link)


# In[16]:

leaders_links = pd.DataFrame(leader_network['links'])


# In[19]:

with open('worldleaders_network.json','w') as ofh3:
    json.dump(leader_network, ofh3)


# In[9]:

office_network = {'nodes':[],'links':[]}
nodes = {}
threshold = 0.005
ifh = open('worldleaders_2015_v2_mutual_fans.csv','r')
first = True
filereader = reader(ifh, delimiter=',', quotechar='"')
for row in filereader:
    if first:
        first = False
        continue
    assert len(row) == len(mutual_fans_header)
    row_dict = dict(zip(mutual_fans_header, row))
    link_jaccard = float(row_dict['mutual_fans'])/(float(row_dict['fan_count_A']) + float(row_dict['fan_count_B']) - float(row_dict['mutual_fans']))
    if link_jaccard < threshold:
        continue
    if row_dict['role_A'] == 'Government Office' and row_dict['role_B'] == 'Government Office':
        if row_dict['pageid_A'] not in nodes:
            nodeA = {'country':row_dict['country_A'],
                     'role':row_dict['role_A'],
                     'pageid':row_dict['pageid_A'],
                     'name':row_dict['name_A'],
                     'fan_count':float(row_dict['fan_count_A']),
                     'position':len(office_network['nodes'])}
            nodes[row_dict['pageid_A']] = nodeA
            office_network['nodes'].append(nodeA)
        if row_dict['pageid_B'] not in nodes:
            nodeB = {'country':row_dict['country_B'],
                    'role':row_dict['role_B'],
                     'pageid':row_dict['pageid_B'],
                     'name':row_dict['name_B'],
                     'fan_count':float(row_dict['fan_count_B']),
                     'position':len(office_network['nodes'])}
            nodes[row_dict['pageid_B']] = nodeB
            office_network['nodes'].append(nodeB)
        link = {'source':nodes[row_dict['pageid_A']]['position'],
                'target':nodes[row_dict['pageid_B']]['position'],
                'value':float(row_dict['mutual_fans']),
                'jaccard':link_jaccard}
        office_network['links'].append(link)


# In[10]:

with open('government_office_network.json','w') as ofh1:
    json.dump(office_network, ofh1)


# In[11]:

foreign_ministry_network = {'nodes':[],'links':[]}
nodes = {}
threshold = 0.005
ifh = open('worldleaders_2015_v2_mutual_fans.csv','r')
first = True
filereader = reader(ifh, delimiter=',', quotechar='"')
for row in filereader:
    if first:
        first = False
        continue
    assert len(row) == len(mutual_fans_header)
    row_dict = dict(zip(mutual_fans_header, row))
    link_jaccard = float(row_dict['mutual_fans'])/(float(row_dict['fan_count_A']) + float(row_dict['fan_count_B']) - float(row_dict['mutual_fans']))
    if link_jaccard < threshold:
        continue
    if row_dict['role_A'] == 'Foreign Ministry' and row_dict['role_B'] == 'Foreign Ministry':
        if row_dict['pageid_A'] not in nodes:
            nodeA = {'country':row_dict['country_A'],
                     'role':row_dict['role_A'],
                     'pageid':row_dict['pageid_A'],
                     'name':row_dict['name_A'],
                     'fan_count':float(row_dict['fan_count_A']),
                     'position':len(foreign_ministry_network['nodes'])}
            nodes[row_dict['pageid_A']] = nodeA
            foreign_ministry_network['nodes'].append(nodeA)
        if row_dict['pageid_B'] not in nodes:
            nodeB = {'country':row_dict['country_B'],
                    'role':row_dict['role_B'],
                     'pageid':row_dict['pageid_B'],
                     'name':row_dict['name_B'],
                     'fan_count':float(row_dict['fan_count_B']),
                     'position':len(foreign_ministry_network['nodes'])}
            nodes[row_dict['pageid_B']] = nodeB
            foreign_ministry_network['nodes'].append(nodeB)
        link = {'source':nodes[row_dict['pageid_A']]['position'],
                'target':nodes[row_dict['pageid_B']]['position'],
                'value':float(row_dict['mutual_fans']),
                'jaccard':link_jaccard}
        foreign_ministry_network['links'].append(link)


# In[12]:

with open('foreign_ministry_network.json','w') as ofh2:
    json.dump(foreign_ministry_network, ofh2)


# In[ ]:




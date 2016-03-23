import os
import json
author_map = {}
author_list = []
baseurl='http://dl.acm.org/'

with open('aff.json1','r') as outfile:
    data_dict = json.load(outfile)
datas = data_dict['authors']
for data in datas:
	record = {'link' : baseurl+data[0], 'FName' : data[4], 'MName':data[5], 'LName': data[3], 'FULL Name':data[6]}
	author_list.append(record)
output_dict = {'authors' : [author for author in author_list] }
with open('Author1.json','w') as outfile:
    json.dump(output_dict,outfile)
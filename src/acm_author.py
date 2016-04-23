import json
import os
import glob

author_dict = {}
files = glob.glob("../output/*.json")

for file in files:
	with open(file, 'r') as outfile:
		data_dict = json.load(outfile)
	jname = file.split('/')[-1].split('.')
	jdata_dict = data_dict[jname[0]]['Volumes']
	volumes = jdata_dict.keys()
	for volume in volumes:
		issues = jdata_dict[volume].keys()
		for issue in issues:
			issue_data = jdata_dict[volume][issue]['articles']
			article_names = issue_data.keys()
			for article in article_names:
				authors = issue_data[article]['authors']
				for author in authors:
					if author['name'] == '':
						continue;
					parts = author['name'].split(' ')
					if len(parts) > 2:
						record = {'link' : author['link'], 'FName' : parts[0], 'MName': parts[1], 'LName': parts[2], 'FULL Name':author['name']}
					elif len(parts) > 1:
						record = {'link' : author['link'], 'FName' : parts[0], 'MName': '', 'LName': parts[1], 'FULL Name':author['name']}
					else:
						record = {'link' :author['link'], 'FName' : parts[0], 'MName': '', 'LName': '', 'FULL Name':author['name']}
					author_dict[author['name']] = record
					print(record)
output_dict = {'authors' : [author for IDs,author in author_dict.items()] }
with open('../data/acm_authordata','w') as outfile:
	json.dump(output_dict,outfile)
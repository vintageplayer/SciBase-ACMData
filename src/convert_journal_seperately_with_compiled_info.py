import re
import json
import unicodedata


journal_list = []

with open('../data/ACM_Journal_list.csv','r') as infile:
	lines = infile.read().split('\n')
for line in lines:
	jname = line.split(',')[2]
	journal_list.append(jname)


for journal_name in journal_list:
	journal_dict = {}
	print('Scanning : '+str(journal_name))
	try:
		with open('../output/Journal Data/'+journal_name+'.json','r') as infile:
			journal_dict = json.load(infile)
	except IOError:
		print('File Not Found : '+journal_name)
		continue
	with open('../output/Author and citation details/'+journal_name+'.json','r') as infile:
		j2_dict = json.load(infile)

	for volume in journal_dict[journal_name]['Volumes']:
		for issue in journal_dict[journal_name]['Volumes'][volume]:
			for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
				journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['citations'] = j2_dict['Volumes'][volume][issue][article]['citation_data']
				journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data'] = j2_dict['Volumes'][volume][issue][article]['authors']

	with open('../output/Finalized_structure/'+journal_name+'.json','w') as outfile:
		json.dump(journal_dict,outfile)
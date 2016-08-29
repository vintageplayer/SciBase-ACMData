import re
import json
import unicodedata


journal_list = []

with open('../../data/ACM_Journal_list.csv','r') as infile:
	lines = infile.read().split('\n')
for line in lines:
	jname = line.split(',')[2]
	journal_list.append(jname)

for journal_name in journal_list:
	journal_dict = {}
	try:
		with open('../../output/Article_Author_data/'+journal_name+'.json','r') as infile:
			journal_dict = json.load(infile)
	except FileNotFoundError:
		print('File Not Found : '+journal_name)
		continue
	with open('../../output/Author Details from references/'+journal_name+'.json','r') as infile:
		j2_dict = json.load(infile)
	volume_dict = {}
	for volume in journal_dict['Volumes']:
		issue_dict = {}
		for issue in journal_dict['Volumes'][volume]:
			article_dict = {}
			for article in journal_dict['Volumes'][volume][issue]:
				article_dict[article] = {}
				article_dict[article]['authors'] = journal_dict['Volumes'][volume][issue][article]
				article_dict[article]['citation_data'] = j2_dict['Volumes'][volume][issue][article]
			issue_dict[issue] = article_dict
		volume_dict[volume] = issue_dict


	final_dict = {'Volumes':volume_dict}

	with open('../../output/Author and citation details/'+journal_name+'.json','w') as outfile:
		json.dump(final_dict,outfile)
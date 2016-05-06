import json 
import os

complete_dict = {}
complete_dict['ACM'] = {}
Jlist = os.listdir('../output')
for journal in Jlist:
	if journal[0]!='.':
		with open('../output/'+journal,'r') as infile:
			journal_data = json.load(infile)
		complete_dict['ACM'][journal.split('.')[0]] = journal_data[journal.split('.')[0]]
with open('../data/complete_data.json','w') as outfile:
	json.dump(complete_dict,outfile)
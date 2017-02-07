import json
import glob

journals = glob.glob("../output/Journal Data/*.json")
prev_journals = "../output/Previous Versions/Journal Data-Initial author data/"

# for journal in journals:
# 	fname = journal.split('/').pop()

# 	jdic = json.loads(journal)

# 	prev_dic = json.loads(prev_journals+fname)

for journal in journals:
	fname = journal.split('/').pop()
	journal_name = fname.split('.')[0]
	print('Scanning : '+str(fname))
	try:
		with open(journal,'r') as infile:
			journal_dict = json.load(infile)
	except IOError:
		print('File Not Found : '+journal_name)
		continue

	try:
		with open(prev_journals+fname,'r') as infile:
			prev_dict = json.load(infile)
	except IOError:
		print('Prev file Not Found : '+journal_name)
		continue

	# volume_dict = {}
	for volume in journal_dict[journal_name]['Volumes']:
		for issue in journal_dict[journal_name]['Volumes'][volume]:
			for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
				journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['citation_strings'] = prev_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['citations']


	with open('../output/New Version/'+fname,'w') as outfile:
		json.dump(journal_dict,outfile)

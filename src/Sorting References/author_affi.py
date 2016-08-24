import re
import json
import unicodedata

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('_',' ',text)
    return text

def get_words():
	words = [ text_to_id(i) for i in open('wordlist.txt','r').read().split('\n')]
	return words

def get_country_list():
	temp_list = open("all_countries.txt","r").read().split('\n')
	countries = [ text_to_id(i.split('|')[1]) for i in temp_list]
	return countries

def get_institute_list():
	institute_list = open('../../data/InstituteCountryContinent.csv','r').read().split('\n')
	institute_dict = {}
	for element in institute_list:
		temp_list = element.split('","')
		temp_list[0] = temp_list[0].strip('"')
		temp_list[2] = temp_list[2].strip('"')
		institute_dict[text_to_id(temp_list[0])] = temp_list
	return institute_dict

def get_authors_list(areference):
	temp = areference[:]
	if len(temp.split(',')) == 1:
		return None

	auth_list = []

	string_len = len(areference)
	pattern = re.compile('[,]([ ][A-Z][ ]?[.])+[,0-9]')
	# if re.search('[,]([ ][A-Z][ ]?[.])+[,0-9]',areference,0,string_len-10) != None:
	if pattern.search(areference,0,string_len-10) != None:
		chars_removed = 0
		initials = re.finditer('[,]([ ][A-Z][ ]?[.])+[,0-9]',areference)
		for initial in initials:
			check_last = areference[chars_removed:initial.start()]
			if ' and' in check_last:
				if len(check_last.split(',')) == 1:
					auth_name = areference[initial.start()+2:initial.end()-1]+check_last.split('and')[-1]
					auth_list.append(auth_name)
				else:
					auth_name = areference[initial.start()+2:initial.end()-1]+check_last.split('and')[-1]
					auth_parts = check_last.split('and')[0].split(',')
					second_auth_name = auth_parts[1] + auth_parts[0]
					second_auth_name = second_auth_name[1:]
					auth_list.append(auth_name)
					auth_list.append(second_auth_name)
				continue
			fname =  areference[initial.start()+2:initial.end()-1]+' ' + areference[chars_removed:initial.start()]
			chars_removed += initial.end() - chars_removed
			fname = re.sub('[ ]+', ' ', fname)
			auth_list.append(fname)
	else:
		temp = temp.split(',')
		parts = [temp[0]]
		for i in temp[1:]:
			part = i[1:]
			parts.append(part)

		count = len(parts)
		for part in reversed(parts):
			if re.search('[A-Z][.]',part) == None:
				count -= 1
				if re.search('[:]|["]',part) != None:
					break
			else:
				break
		if count!=0 :
			[auth_list.append(i) for i in parts[:count]]
		else:
			return None

	return auth_list


def get_country(areference):
	global Countries

	areference = text_to_id(areference)
	for country in Countries:
		if country in areference:
			return country

	return None

def get_institution(areference):
	global institute_dict
	global institute_list

	areference = text_to_id(areference)

	for institute in institute_list:
		if institute in areference:
			return institute

	return None

	"""
		OLD LOGIC
	
	# parts = re.split('[,.]',areference)
	# possible_list = ['university','institution','school','institute','college','laboratory','laboratories','technology','enginnering']
	# for word in possible_list:
	# 	for part in reversed(parts):
	# 		temp = text_to_id(part)
	# 		if re.search('[^A-Za-z]'+word,temp) != None:
	# 			part = re.sub('^[^A-Za-z]','',part)
	# 			return part
	# return None

	"""

def get_values(areference):
	global citation_data_list
	global institute_dict

	auth_list =  get_authors_list(areference)

	if auth_list == None:
		return None

	affiliation = get_institution(areference)
	if affiliation == None:
		country = get_country(areference)
	else:
		country = institute_dict[affiliation][1]
		affiliation = institute_dict[affiliation][0]

	for author in auth_list:
		temp = {"Name":author,"Country":country,"Affiliation":affiliation}
		citation_data_list.append(temp)


English_words = get_words()
Countries = get_country_list()

institute_dict = get_institute_list()
institute_list = institute_dict.keys()

journal_list = []

with open('../../data/ACM_Journal_list.csv','r') as infile:
	lines = infile.read().split('\n')
for line in lines:
	jname = line.split(',')[2]
	journal_list.append(jname)

for journal_name in journal_list:
	journal_dict = {}
	try:
		with open('../../output/Journal Data/'+journal_name+'.json','r') as infile:
			journal_dict = json.load(infile)
	except FileNotFoundError:
		print('File Not Found : '+journal_name)
		continue
	volume_dict = {}
	for volume in journal_dict[journal_name]['Volumes']:
		issue_dict = {}
		for issue in journal_dict[journal_name]['Volumes'][volume]:
			article_dict = {}
			for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
				citation_data_list = []
				for citation in journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['citations']:
					get_values(citation)
				article_dict[article] = citation_data_list
			issue_dict[issue] =article_dict
		volume_dict[volume] = issue_dict


	final_dict = {'Volumes':volume_dict}

	with open('../../output/Author Details from references/'+journal_name+'.json','w') as outfile:
		json.dump(final_dict,outfile)

# author_dict = {"Authors":final_list}
# with open('../../output/Author Details from references/sample.json','w') as outfile:
# 	json.dump(author_dict,outfile)
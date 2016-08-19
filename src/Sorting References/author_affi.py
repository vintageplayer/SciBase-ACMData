import re
import json
import unicodedata
import sys

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

def get_instituion(areference):
	parts = re.split('[,.]',areference)
	possible_list = ['university','institution','school','institute','college','laboratory','laboratories','technology','enginnering']
	for word in possible_list:
		for part in reversed(parts):
			temp = text_to_id(part)
			if re.search('[^A-Za-z]'+word,temp) != None:
				part = re.sub('^[^A-Za-z]','',part)
				return part
	return None

def get_values(areference):
	global final_list
	auth_list =  get_authors_list(areference)

	if auth_list == None:
		return None

	country = get_country(areference)
	affiliation = get_instituion(areference)

	for author in auth_list:
		temp = {"Name":author,"Country":country,"Affiliation":affiliation}
		final_list.append(temp)


final_list = []
English_words = get_words()
Countries = get_country_list()

journal_dict = {}

with open('../../output/Journal Data/TEAC.json','r') as infile:
	journal_dict = json.load(infile)

for volume in journal_dict['TEAC']['Volumes']:
	for issue in journal_dict['TEAC']['Volumes'][volume]:
		for article in journal_dict['TEAC']['Volumes'][volume][issue]['articles']:
			for citation in journal_dict['TEAC']['Volumes'][volume][issue]['articles'][article]['citations'][::]:
				get_values(citation)


author_dict = {"Authors":final_list}
with open('../../output/Author Details from references/sample.json','w') as outfile:
	json.dump(author_dict,outfile)
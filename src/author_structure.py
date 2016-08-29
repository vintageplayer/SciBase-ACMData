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

def initialize():
    global country_list
    global city_list
    global city_country_dict

    temp_list = open("./Sorting References/all_countries.txt","r").read().split('\n')
    country_list = [ text_to_id(i.split('|')[1]) for i in temp_list]

    with open('Continents_Countries.json','r') as infile:
        temp_dict = json.load(infile)

    for continent in temp_dict.keys():
        for country in temp_dict[continent]:
            for city in temp_dict[continent][country]['cities']:
                city = text_to_id(city)
                city_list.append(city)
                city_country_dict[city] = country

def get_country(astring):
    global country_list
    for country in country_list:
        if country in astring:
            return country

    return None

def get_city_country(astring):
    global city_list
    global city_country_dict

    temp = []
    for city in city_list:
        city_word  = ' '+city+' '
        if city_word in astring:
            temp.append(city)
            temp.append(city_country_dict[city])
            return temp

    return None

def get_values(arecord):
    author_dict = {}
    author_dict['Name'] = arecord['name']
    if arecord['affiliation']!=None:
        author_dict['university'] = arecord['affiliation']
        temp = get_city_country(arecord['affiliation'])
        if temp != None:
            author_dict['city'] = temp[0]
            author_dict['country'] = temp[1]
        else:
            author_dict['country'] = get_country(arecord['affiliation'])
            author_dict['city'] = None
    else:
        author_dict['university'] = None
        author_dict['country'] = None

    return author_dict

city_list = []
city_country_dict = {}
country_list = []
initialize()

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
    # try:
    #     with open('../output/Journal Data/'+journal_name+'.json','r') as infile:
    #         journal_dict = json.load(infile)
    # except FileNotFoundError:
    #     print('File Not Found : '+journal_name)
    #     continue
    volume_dict = {}
    for volume in journal_dict[journal_name]['Volumes']:
        issue_dict = {}
        for issue in journal_dict[journal_name]['Volumes'][volume]:
            article_dict = {}
            for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
                authors_data_list = []
                for author in journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data']:
                    authors_data_list.append(get_values(author))
                article_dict[article] = authors_data_list
            issue_dict[issue] =article_dict
        volume_dict[volume] = issue_dict


    final_dict = {'Volumes':volume_dict}

    with open('../output/Article_Author_data/'+journal_name+'.json','w') as outfile:
        json.dump(final_dict,outfile)
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

    temp = {}

    with open('../data/Univ_data.json') as infile:
        temp = json.load(infile)

    return temp


def get_university(astring):
    global university_details

    result = None
    for university in  university_details['list']:
        if university['institution'] in astring:
            result = {}
            result['university']    = university['institution']
            result['city']          = university['city']
            result['country']       = university['country']

    return result


# def get_values(arecord):
#     author_dict = {}
#     author_dict['Name'] = arecord['name']
#     if arecord['affiliation']!=None:
#         author_dict['university'] = arecord['affiliation']
#         temp = get_city_country(arecord['affiliation'])
#         if temp != None:
#             author_dict['city'] = temp[0]
#             author_dict['country'] = temp[1]
#         else:
#             author_dict['country'] = get_country(arecord['affiliation'])
#             author_dict['city'] = None
#     else:
#         author_dict['university'] = None
#         author_dict['country'] = None
#         author_dict['city'] = None

#     return author_dict

def get_values(arecord):
    arecord['affiliation_string'] = arecord['university']
    if arecord['affiliation_string']!=None:
        temp = get_university(arecord['affiliation_string'])
        if temp != None:
            arecord['university'] = temp['university']
            arecord['city'] = temp['city']
            arecord['country'] = temp['country']
        else:
            arecord['university'] = None
            """
                Keeping the city and country as predicted by the previous logic
            """

    return arecord



university_details  = initialize()
journal_list        = []

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
    # volume_dict = {}
    for volume in journal_dict[journal_name]['Volumes']:
        for issue in journal_dict[journal_name]['Volumes'][volume]:
            for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
                authors_data_list = []
                for author in journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data']:
                    authors_data_list.append(get_values(author))
                journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data'] = authors_data_list


    with open('../output/'+journal_name+'.json','w') as outfile:
        json.dump(journal_dict,outfile)


"""
    Previous Script Code
"""
# for journal_name in journal_list:
#     journal_dict = {}
#     print('Scanning : '+str(journal_name))
#     try:
#         with open('../output/Journal Data/'+journal_name+'.json','r') as infile:
#             journal_dict = json.load(infile)
#     except IOError:
#         print('File Not Found : '+journal_name)
#         continue
#     volume_dict = {}
#     for volume in journal_dict[journal_name]['Volumes']:
#         issue_dict = {}
#         for issue in journal_dict[journal_name]['Volumes'][volume]:
#             article_dict = {}
#             for article in journal_dict[journal_name]['Volumes'][volume][issue]['articles']:
#                 authors_data_list = []
#                 for author in journal_dict[journal_name]['Volumes'][volume][issue]['articles'][article]['affiliation_data']:
#                     authors_data_list.append(get_values(author))
#                 article_dict[article] = authors_data_list
#             issue_dict[issue] =article_dict
#         volume_dict[volume] = issue_dict


#     final_dict = {'Volumes':volume_dict}

#     with open('../output/Article_Author_data/'+journal_name+'.json','w') as outfile:
#         json.dump(final_dict,outfile)
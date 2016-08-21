import os
import json
#mdir="./Output5/JDIQ"
#dir=os.listdir(mdir)
#volume_dict={}
#issue_dict={}
#for sub in dir:
def get_volume_dict(sub,volume_dict,mdir):
	issue_dict={}
	Volume=sub.split(" ")
	if not volume_dict.has_key(str(Volume[0]+Volume[1])):
		volume_dict[str(Volume[0]+Volume[1])]={}
	aritcles=os.listdir(mdir+"/"+sub)
	output={}
	for article in aritcles:
		if article[0]!= '.':
			fs=open((mdir+'/'+sub+'/'+article+'/citations.txt'),"r")
			citations=fs.readlines()
			fs.close()
			fs=open((mdir+'/'+sub+'/'+article+'/references.txt'),"r")
			references=fs.readlines()
			fs.close()
			fs=open((mdir+'/'+sub+'/'+article+'/title.txt'),"r")
			title=fs.read()
			fs.close()
			fs=open((mdir+'/'+sub+'/'+article+'/doi.txt'),"r")
			doi=fs.read()
			fs.close()
			fs=open((mdir+'/'+sub+'/'+article+"/authors.txt"),"r")
			authors=fs.readlines()#strip("\n")
			author_names = [author.split(" ")[0] for author in authors]
			links = [author.split(" ")[1] for author in authors]
			links = [('http://dl.acm.org/'+link.split("&")[0]) for link in links]
			author_names = [name.replace('_',' ') for name in author_names]
			fs.close()
			fs = open((mdir+'/'+sub+'/'+article+"/stats.txt"),"r")
			stats = fs.readlines()
			if len(stats) == 0:
				stats = [0,0,0,0]
			stat = {}
			stat['Downloads (6 weeks) '] = stats[0]
			stat['Downloads (12 months)'] = stats[1]
			stat['Downloads (cumulative)'] = stats[2]
			stat['Citation Count'] = stats[3]
			fs.close()
			fs=open((mdir+'/'+sub+'/'+article+"/abstract.txt"),"r")
			abstract=(fs.read()).strip("\n")
			fs.close() 
			output[str(article)] = {"title" : title, "authors" : [{'link':link,'name':name} for link,name in zip(links,author_names)] , "Metrics": stat, "abstract" : abstract , "doi":doi , "references":references , "citations" : citations}
	if len(Volume)<4:
		Volume.append(Volume[2])
		Volume.append(Volume[2])
		Volume[2] = "Issue"
		Volume[3] = "1"
	if len(Volume)<6:
		Volume.append(Volume[4])
		Volume[4] = 0
	issue_dict[str(Volume[2]+Volume[3].strip(','))] = {"date":{"month":Volume[4], "year":Volume[5]}, "articles":output}
	volume_dict[str(Volume[0]+Volume[1])].update(issue_dict)
	return volume_dict

ISSN_file = "../data/Journal_data/ISSN_MAP.csv"

file = open(ISSN_file,'r').read()
ISSN_List = file.split('\n')
ISSN_dict = {}
for element in ISSN_List:
	parts = element.split(',')
	ISSN_dict[parts[0]] = parts[1]

Jdir = "../data/Journal_data/Journals"
jlist = os.listdir(Jdir)
for Journal in jlist:
	if Journal[0] != '.':
		jdic = {}
		vdir  = Jdir + '/' + Journal + '/' + 'Volumes'
		idir = os.listdir(vdir)
		volume_dict = {}
		for sub in idir:
			if sub[0]!= '.':
				volume_dict = get_volume_dict(sub,volume_dict,vdir)
		jdic[Journal] = {"Volumes":volume_dict, "ISSN":ISSN_dict[Journal]}
		with open("../output/"+Journal+".json","w") as jfile:
			json.dump(jdic,jfile)
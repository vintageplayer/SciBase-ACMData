from bs4 import BeautifulSoup
import urllib2, sys
import json
import os
data = {}
"""
url = 'http://dl.acm.org/griddata.cfc?method=getAffils&returnFormat=json&argumentCollection={%22page%22%3A1%2C%22pageSize%22%3A1%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J204%22%2C%22myfilter%22%3A%22%22}&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=DE229159ACBF5F1D2A0583226441B4BA&_cf_rc=2'
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib2.Request(url,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
with open('aff.json','w') as outfile:
	outfile.write(str(soup))
with open('aff.json','r') as infile:
	raw = infile.read()
data = json.loads(raw)
count = data['TOTALROWCOUNT']
new_url = 'http://dl.acm.org/griddata.cfc?method=getAffils&returnFormat=json&argumentCollection={%22page%22%3A1%2C%22pageSize%22%3A'+str(count)+'%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J204%22%2C%22myfilter%22%3A%22%22}&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=DE229159ACBF5F1D2A0583226441B4BA&_cf_rc=2'
req = urllib2.Request(new_url,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
with open('aff.json','w') as outfile:
	outfile.write(str(soup))
burl = 'http://dl.acm.org/'
with open('aff.json','r') as infile:
	raw = infile.read()
data = json.loads(raw)
dir = 'Output3/Affiliations'
if not os.path.exists(dir):
		os.makedirs(dir)
cfl = open(dir+'/'+'college_list.txt','w')
for i in range(0,(count-1)):
	cfl.write(data['QUERY']['DATA'][i][0].encode('utf8') + '\n')
clf.close()
"""
with open('aff.json','r') as outfile:
	datas = json.load(outfile)
datas = datas['QUERY']['DATA']
#url = 'http://dl.acm.org/griddata.cfc?method=getNames&returnFormat=json&argumentCollection=%7B%22page%22%3A1%2C%22pageSize%22%3A1%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J204%22%2C%22myfilter%22%3A%22%22%7D&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=DE229159ACBF5F1D2A0583226441B4BA&_cf_rc=2'
url = 'http://dl.acm.org/griddata.cfc?method=getNames&returnFormat=json&argumentCollection=%7B%22page%22%3A1%2C%22pageSize%22%3A1%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J1191%22%2C%22myfilter%22%3A%22%22%7D&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=F251BBBD32EB66141FEEE88A90D1C5C9&_cf_rc=4'
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib2.Request(url,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
with open('aff.json1','w') as outfile:
	outfile.write(str(soup))
with open('aff.json1','r') as infile:
	raw = infile.read()
data = json.loads(raw)
count = data['TOTALROWCOUNT']
#new_url = 'http://dl.acm.org/griddata.cfc?method=getNames&returnFormat=json&argumentCollection=%7B%22page%22%3A1%2C%22pageSize%22%3A'+str(count)+'%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J204%22%2C%22myfilter%22%3A%22%22%7D&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=DE229159ACBF5F1D2A0583226441B4BA&_cf_rc=2'
new_url = 'http://dl.acm.org/griddata.cfc?method=getNames&returnFormat=json&argumentCollection=%7B%22page%22%3A1%2C%22pageSize%22%3A'+str(count)+'%2C%22gridsortcolumn%22%3A%22%22%2C%22gridsortdir%22%3A%22%22%2C%22useid%22%3A%22J1191%22%2C%22myfilter%22%3A%22%22%7D&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=F251BBBD32EB66141FEEE88A90D1C5C9&_cf_rc=4'
req = urllib2.Request(new_url,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
with open('aff.json1','w') as outfile:
	outfile.write(str(soup))
burl = 'http://dl.acm.org/'
with open('aff.json1','r') as infile:
	raw = infile.read()
new_data = json.loads(raw)
new_data = new_data['QUERY']['DATA']
for data in new_data:
	if data not in datas:
		datas.append(data)
output_dict = {'authors':datas}
with open('aff.json1','w') as outfile:
	json.dump(output_dict,outfile)
"""
dir = 'Output3/Affiliations'
afl = open(dir+'/'+'author_list.txt','w')
for i in range(0,(count-1)):
	lname = data['QUERY']['DATA'][i][3].encode('utf8')
	fname = data['QUERY']['DATA'][i][4].encode('utf8')
	if data['QUERY']['DATA'][i][5]!=None:
		midname = data['QUERY']['DATA'][i][5].encode('utf8')
	else : 
		midname = '-'
	afl.write(lname + ' ' + fname  + ' ' + midname + '\n')
afl.close()
"""
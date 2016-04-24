from bs4 import BeautifulSoup
import urllib2


f = open('journal_links.txt','r')
o = open('../data/ACM_Journal_list.csv','w')

journals = f.readlines()


for journal in journals:
	url = journal.split("'")[1]
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	page = urllib2.urlopen(req)	
	soup = BeautifulSoup(page, 'html.parser')
	full_name = soup.find('h5').get_text()
	abbreviation = journal.split("'")[0].split(' ')[1]
	temp = full_name
 	temp = temp.replace(' (','(')
	record = full_name + ',' + temp.split('(')[0] + ',' + abbreviation
	o.write(record + '\n')
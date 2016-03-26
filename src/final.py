from bs4 import BeautifulSoup
import urllib2, sys
import json
import os
import re
import unicodedata
import ast

def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

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
    return text

def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(aurl,headers=hdr)
	page = urllib2.urlopen(req)	
	asoup = BeautifulSoup(page, 'html.parser')
	return asoup

baseurl='http://dl.acm.org/'
author_map = {}
y = 0
 # ENTER THE URL FROM JOURNAL LIST
url = 'http://dl.acm.org/pub_series.cfm?id=J778&_cf_containerId=pubs&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=A4CD5C7467A0092AB36D2384B391AB15&_cf_rc=1'
soup = get_soup(url)

# CHANGE THE PATH TO '../data/Journal_data/<SELECETED JOURNAL NAME>/Volumes'
Dir = '../data/Journal_data/TACCESS/Volumes'
adir = '../data/Author_Details'
addir = adir + '/Details'
ckdir(Dir)
ckdir(adir)
ckdir(addir)
fl = open(adir+'/AuthorURLMap.txt','r')
temp = fl.read()
if temp != '':
    author_map = ast.literal_eval(temp)
fl.close()
anfl = open(adir+'/AuthorNames.txt','a')
posts = soup.find_all("a")

for post in posts[0::]:
    if post.get_text() != 'Issue-in-Progress' :
        print('post index : ' + str(posts.index(post)))
        ndir = Dir+'/'+str(post.get_text())
        ckdir(ndir)
        link = post["href"]
        newurl = baseurl + link
        newsoup = get_soup(newurl)
        values = re.findall(r'prox.*?=\s*(.*?);', str(newsoup), re.DOTALL )
        newvalue =values[0].split('{', 1)[1].rsplit('}', 1)[0]
        link2 =(newvalue.split('{', 1)[1]).split('[',1)[1].rsplit("'",1)[0].split("'",1)[1]
        url3 =baseurl+link2
        soup3 = get_soup(url3)
        articles=(soup3.find("table",{"class":"text12"})).find_all("tr")
        index = len(articles) 
        z = y
        i = 0
        while i < ((index - z)/6):
            while articles[i*6+z].find("a") == None or 'citation.cfm?id' not in str(articles[i*6+z].find("a")["href"]):
                z = z + 1
            article=articles[i*6+z].find("a")["href"]
            furl = baseurl + article +"&preflayout=flat"
            fsoup = get_soup(furl)
            test_author = articles[i*6+z+1].get_text()
            if 'Article' in test_author or 'Page' in test_author:
                i = i + 1
                continue
            shrunk = fsoup.find("div",{"class":"flatbody"})
            smaller = shrunk.find_all('div',{'class':'flatbody'})
            if smaller == []:
                smaller = fsoup.find_all("div",{"class":"flatbody"})
                x=1 
            else :
                x=0 
            athrs = smaller[0+x].find('dl')
            while not athrs: 
                x = x + 1
                athrs = smaller[0+x].find('dl')
            references = smaller[1+x].find_all('div')
            citations = smaller[2+x].find_all('div')
            athrs = smaller[0+x].find_all('span')
            fdir=ndir+'/'+(articles[(i*6)+2+z].find("span").get_text(strip=True))
            ckdir(fdir)
            fn=open(fdir+"/abstract.txt","w")
            try :
                if x==0:
                    abstract=(shrunk.find('div',{'style':'display:inline'})).get_text(strip=True)
                else :
                    abstract = smaller[0].get_text(strip=True)
                fn.write(abstract.encode('utf8'))
            except Exception:
                pass
            try:
                fn.close()
                fn = open(fdir + '/stats.txt', 'w')
                bib = fsoup.find('td',{'class':'small-text'},{'colspan':'2'})
                datas = bib.get_text().split(':')
                for data in datas[1::]:
                    value = int(data.split('\r')[0].replace(',',''))
                    fn.write(str(value)+'\n')
            except Exception:
                pass
            try :
                fn.close()
                fn=open(fdir+"/authors.txt","w")
                authors=(articles[(i*6)+1+z].find("span").get_text(strip=True)).split(',')
                athr_urls = articles[(i*6)+1+z].find("span").find_all('a')
                for author,athr,athr_url in zip(authors,athrs,athr_urls):
                    author = text_to_id(author)
                    if author_map.has_key(athr_url['href']) == False:
                        author_map[athr_url['href']] = []
                    author_map[athr_url['href']].append(author)
                    fn.write(author + ' ' + str(athr_url['href']) + '\n')
                    anfl.write(author + '\n')
                    ff=open(addir + '/' + author, 'w')
                    stats = athr.find_all('td', {'class': 'small-text'})
                    for stat in stats:
                        ff.write(stat.get_text() + '\n')
                    ff.close()
                aumfl = open(adir+'/AuthorURLMap.txt','w')
                aumfl.write(str(author_map))
                aumfl.close()
            except Exception:
                pass
            try:
                fn.close()
                fn = open(fdir + '/institution.txt', 'w')
                info = fsoup.find('table',{'style':'margin-top: 10px; border-collapse:collapse; padding:2px;'},{'class':'medium-text'})
                records = info.find_all('a')
                for record in records[::2]:
                    fn.write(text_to_id(record.get_text())+' '+text_to_id(records[records.index(record)+1].get_text()))
            except  Exception:
                pass
            try :
                fn.close()
                fn=open(fdir+"/references.txt","w")
                for reference in references[1::2]:
                    fn.write(reference.get_text(strip=True).encode('utf8')+'\n')
            except Exception:
                pass
            try :
                fn.close()
                fn=open(fdir+"/citations.txt","w")
                for citation in citations:
                    fn.write(citation.get_text(strip=True).encode('utf8')+'\n')
            except Exception:
                pass
            try :
                fn.close()
                fn=open(fdir+"/doi.txt","w")
                abstract=articles[(i*6)+3+z].find("span").get_text(strip=True)
                fn.write(abstract.encode('utf8'))
            except Exception:
                pass
            try :
                fn.close()
                fn=open(fdir+"/title.txt","w")
                title=articles[(i*6)+z].find("span").get_text(strip=True)
                fn.write(title.encode('utf8'))
                fn.close()
            except Exception:
                pass
            i = i+ 1

anfl.close()

from bs4 import BeautifulSoup
import urllib2, sys
import json
import os
import re
import unicodedata
import ast

baseurl='http://dl.acm.org/'
author_map = {}
y = 0
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:#NameError: # unicode is a default on python 3 
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

url = 'http://dl.acm.org/pub_series.cfm?id=J967&_cf_containerId=pubs&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=C37F87628DE0E7610F1187FC299D1CA1&_cf_rc=1'
soup = get_soup(url)
Dir = "Output5/JACM"
adir = 'Output5/Author_Details'
addir = adir + '/Details'
ckdir(Dir)
ckdir(adir)
ckdir(addir)
fl = open('Output5/Author_Details/AuthorURLMap1.txt','r')
author_map = ast.literal_eval(fl.read())
fl.close()
anfl = open(adir+'/AuthorNames.txt','a')
posts = soup.find_all("a")
for post in posts:#[::]:
    if posts.index(post)!=1 and posts.index(post)!=0:
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
        index=len(articles)/6
        z = y
        for i in range(0,(index)):
            while articles[i*6+z].find("a") == None :
            	z = z + 1
            article=articles[i*6+z].find("a")["href"]
            furl = baseurl + article +"&preflayout=flat"
            fsoup = get_soup(furl)
            print(furl)
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
                aumfl = open(adir+'/AuthorURLMap2.txt','w')
                aumfl.write(str(author_map))
                aumfl.close()
            except Exception:
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

anfl.close()
#!/usr/bin/env python2

from lxml import etree
import urllib

print "ok"
url='http://service.canal-plus.com/video/rest/getMEAs/cplus/39'
regexpNS = "http://exslt.org/regular-expressions"

data=urllib.urlopen(url).read()

xml=etree.XML(data)
tb={}
for a in xml.xpath("//MEA[RUBRIQUAGE/RUBRIQUE='LE_JT_DE_CANALPLUS']"):
	index= a.xpath('./ID/text()')[0]
	url='http://service.canal-plus.com/video/rest/getVideosLiees/cplus/'+index
	print "get %s"%(index)
	data=urllib.urlopen(url).read()
	video=etree.XML(data)
#	etree.dump(video)
	for b in video.xpath("//VIDEO"):
		tb[b.xpath('./ID/text()')[0]]=b.xpath('./INFOS/DESCRIPTION')[0].text

for idv in sorted(tb,reverse=True,key=int):
	print idv

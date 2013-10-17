# -*- coding: Latin-1 -*-
import re

"""
"""

PLUGIN_PREFIX           = "/video/Cplus"
PLUGIN_ID               = "com.plexapp.plugins.Cplus"
PLUGIN_REVISION         = 0.1
PLUGIN_UPDATES_ENABLED  = True
CACHE_INTERVAL = 3600 * 2
ICON="icon-default.png"
ART= "bg-default.jpg"
NAME="CPlus"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu,NAME,R(ICON),R(ART))
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("ShowList", viewMode="List", mediaType="items")
  MediaContainer.title1 = 'Cplus'
  MediaContainer.content = 'Items'
  MediaContainer.art = R(ART)
  HTTP.SetCacheTime(CACHE_INTERVAL)

####################################################################################################
def MainMenu():
  dir = MediaContainer(title1="Canal Plus", content = 'Items', art = R(ART))
  dir.viewGroup = 'ShowList'
  dir.Append(Function(DirectoryItem(sub_category, title="Le Zapping" , thumb=R("LeZapping.jpg")), Emission_cat='1830', stitle='zapping'))
  dir.Append(Function(DirectoryItem(sub_category, title="Les Guignols" , thumb=R("LesGuignols.jpg")), Emission_cat='1784', stitle='guignols'))
  dir.Append(Function(DirectoryItem(sub_category, title="Le Petit Journal" , thumb=R("LePetitJournal.jpg")), Emission_cat='3351', stitle='le-petit-journal'))
  dir.Append(Function(DirectoryItem(sub_category, title="GroLand" , thumb=R("GroLand.jpg")), Emission_cat='1787', stitle='groland.con'))
  dir.Append(Function(DirectoryItem(sub_category, title="Salut Les Terriens" , thumb=R("icon-default.png")), Emission_cat='3350', stitle='terriens'))
  dir.Append(Function(DirectoryItem(sub_category, title="Effet Papillon" , thumb=R("icon-default.png")), Emission_cat='3356', stitle='papillon'))
  return dir


####################################################################################################
def sub_category (sender, Emission_cat, title = None, replaceParent=False, values=None,stitle=False):
	dir = MediaContainer(title1="", title2=title, replaceParent=replaceParent)
	dir.viewGroup = 'Details'

	mod=stitle
	idd=Emission_cat
	
	site_url='http://www.canalplus.fr/c/pid'+idd
	fhtml=HTML.ElementFromURL(site_url)
	string= XML.StringFromElement(fhtml)
	lst= re.findall('like.*vid=([0-9]*)',string)
	Evnt= max(lst)

	base_address = 'http://service.canal-plus.com/video/rest/getVideosLiees/cplus/'+Evnt
	data=XML.ElementFromURL(base_address)
	hack="?secret=pqzerjlsmdkjfoiuerhsdlfknaes"
	for video in data.xpath('//VIDEO'):
		id= video.xpath('ID')[0].text
		rub= video.xpath('RUBRIQUAGE/RUBRIQUE')[0].text
		cat= video.xpath('RUBRIQUAGE/CATEGORIE')[0].text
		dat= video.xpath('INFOS/PUBLICATION/DATE')[0].text
		url= video.xpath('MEDIA/VIDEOS/HD')[0].text
		img= video.xpath('MEDIA/IMAGES/GRAND')[0].text
		com= video.xpath('INFOS/TITRAGE/TITRE')[0].text
		com= com+ " "+video.xpath('INFOS/TITRAGE/SOUS_TITRE')[0].text
		url=url.replace('rtmp://vod-fms.canalplus.fr/ondemand/videos','http://vod-flash.canalplus.fr/WWWPLUS/STREAMING')+hack
		dir.Append(VideoItem(url,rub+" "+cat,'',com,'',img))
 	return dir
		
#  xml_sections = ETXML.parse(urllib.urlopen(base_address))
#  sections = xml_sections.getroot()
#  for s in range(0,len(sections)):
#  	rub= sections[s].find('RUBRIQUAGE').find('RUBRIQUE').text
#  	cat= sections[s].find('RUBRIQUAGE').find('CATEGORIE').text
#  	inf= sections[s].find('INFOS').find('PUBLICATION').find('DATE').text
#  	url= sections[s].find('MEDIA').find('VIDEOS').find('HD').text
#  	img= sections[s].find('MEDIA').find('IMAGES').find('PETIT').text
#	com= sections[s].find('INFOS').find('TITRAGE').find('SOUS_TITRE').text
##Replace 
# rtmp://vod-fms.canalplus.fr/ondemand/videos
#by http://vod-flash.canalplus.fr/WWWPLUS/STREAMING
#	dir.Append(VideoItem(url,rub+" "+cat,'',rub+"\n"+inf+"\n"+com,'',img))
####################################################################################################

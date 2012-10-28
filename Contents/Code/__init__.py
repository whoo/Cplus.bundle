# -*- coding: Latin-1 -*-

"""

this program grab information from Cplus and provide content for plex application
Based on reading of
	Pierre Della Nave 
	SesameStreet Plugin
	France2 Plugin by Erwan Loisant

Copyright (C) 2012	Dominique DERRIER

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
import PMS
from PMS import Plugin, Log, XML, HTTP
from PMS.Objects import *
from PMS.Shortcuts import *
import re
import unicodedata
## NOT SURE beCAUSE it porduce some error
import xml.etree.ElementTree as ETXML


PLUGIN_PREFIX           = "/video/Cplus"
PLUGIN_ID               = "com.plexapp.plugins.Cplus"
PLUGIN_REVISION         = 0.1
PLUGIN_UPDATES_ENABLED  = True

CACHE_INTERVAL = 3600 * 2

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, 'Cplus', 'cplus-default.jpg', 'bg-default.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("ShowList", viewMode="List", mediaType="items")
  MediaContainer.title1 = 'Cplus'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('bg-default.jpg')
  HTTP.SetCacheTime(CACHE_INTERVAL)

####################################################################################################
def MainMenu():
  dir = MediaContainer(title1="Canal Plus", content = 'Items', art = R('art-default.jpg'))
  dir.viewGroup = 'ShowList'

  dir.Append(Function(DirectoryItem(sub_category, title="Le Zapping" , thumb=R("LeZapping.jpg")), Emission_cat='756696', title='Zapping'))
  dir.Append(Function(DirectoryItem(sub_category, title="Les Guignols" , thumb=R("LesGuignols.jpg")), Emission_cat='756876', title='Guignols'))
  dir.Append(Function(DirectoryItem(sub_category, title="Le Petit Journal" , thumb=R("LePetitJournal.jpg")), Emission_cat='756887', title='PetitJournal'))
  dir.Append(Function(DirectoryItem(sub_category, title="GroLand" , thumb=R("GroLand.jpg")), Emission_cat='757232', title='PetitJournal'))
  return dir


####################################################################################################
def sub_category (sender, Emission_cat, title = None, replaceParent=False, values=None):

  dir = MediaContainer(title1="", title2=title, replaceParent=replaceParent)
  dir.viewGroup = 'Details'
  base_address = 'http://service.canal-plus.com/video/rest/getVideosLiees/cplus/'+Emission_cat

  xml_sections = ETXML.parse(urllib.urlopen(base_address))
  sections = xml_sections.getroot()
  for s in sections:
  	rub= s.find('RUBRIQUAGE').find('RUBRIQUE').text
  	cat= s.find('RUBRIQUAGE').find('CATEGORIE').text
  	inf= s.find('INFOS').find('PUBLICATION').find('DATE').text
  	url= s.find('MEDIA').find('VIDEOS').find('HD').text
  	img= s.find('MEDIA').find('IMAGES').find('PETIT').text
	com= s.find('INFOS').find('TITRAGE').find('SOUS_TITRE').text
#Replace 
# rtmp://vod-fms.canalplus.fr/ondemand/videos
#by http://vod-flash.canalplus.fr/WWWPLUS/STREAMING
	hack="?secret=pqzerjlsmdkjfoiuerhsdlfknaes"
	url=url.replace('rtmp://vod-fms.canalplus.fr/ondemand/videos','http://vod-flash.canalplus.fr/WWWPLUS/STREAMING')+hack
	
	if not (com):
		com="none"
	dir.Append(VideoItem(url,rub+" "+cat,'',rub+"\n"+inf+"\n"+com,'',img))
  return dir
####################################################################################################

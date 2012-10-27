# -*- coding: Latin-1 -*-

"""
Based on 
Pierre Della Nave 
SesameStreet Plugin
France2 Plugin by Erwan Loisant


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

  dir.Append(Function(DirectoryItem(sub_category, title="Zapping" , thumb=R("Zapping.jpg")), Emission_cat='756696', title='Zapping'))
  dir.Append(Function(DirectoryItem(sub_category, title="Guignlos" , thumb=R("Guignols.jpg")), Emission_cat='756876', title='Guignols'))
  dir.Append(Function(DirectoryItem(sub_category, title="PetitJournal" , thumb=R("petitjournal.jpg")), Emission_cat='756887', title='PetitJournal'))
  return dir


####################################################################################################
def sub_category (sender, Emission_cat, title = None, replaceParent=False, values=None):

  dir = MediaContainer(title1="", title2=title, replaceParent=replaceParent)
  dir.viewGroup = 'Details'
  base_address = 'http://service.canal-plus.com/video/rest/getVideosLiees/cplus/'+Emission_cat
  logo_string = 'logo_h.jpg'

  xml_sections = ETXML.parse(urllib.urlopen(base_address))
  sections = xml_sections.getroot()
  for s in sections:
  	rub= s.find('RUBRIQUAGE').find('RUBRIQUE').text
  	cat= s.find('RUBRIQUAGE').find('CATEGORIE').text
  	inf= s.find('INFOS').find('PUBLICATION').find('DATE').text
  	url= s.find('MEDIA').find('VIDEOS').find('HD').text
  	img= s.find('MEDIA').find('IMAGES').find('PETIT').text
	com= s.find('INFOS').find('TITRAGE').find('SOUS_TITRE').text
	dir.Append(VideoItem(url,rub+" "+cat,'',rub+" "+cat+" du "+inf+" "+com,'',img))
  return dir
####################################################################################################

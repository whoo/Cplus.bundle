# -*- coding: Latin-1 -*-

"""
Author: Pierre Della Nave 
Date: May 2009
Revision: 0.1

Acknowledgements and Credits:
SesameStreet Plugin
France2 Plugin by Erwan Loisant

 Copyright (c) 2008 Erwan Loisant <eloisant@gmail.com>

 This file may be used under the terms of the
 GNU General Public License Version 2 (the "GPL"),
 http://www.gnu.org/licenses/gpl.html

 Software distributed under the License is distributed on an "AS IS" basis,
 WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 for the specific language governing rights and limitations under the
 License.
"""
import PMS
from PMS import Plugin, Log, XML, HTTP
from PMS.Objects import *
from PMS.Shortcuts import *
import re
import unicodedata

PLUGIN_PREFIX           = "/video/Cplus"
PLUGIN_ID               = "com.plexapp.plugins.Cplus"
PLUGIN_REVISION         = 0.3
PLUGIN_UPDATES_ENABLED  = True

WEB_ROOT = 'http://jt.france2.fr'

CACHE_INTERVAL = 3600 * 2

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, 'Cplus', 'icon-default.jpg', 'art-default.jpg')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("ShowList", viewMode="List", mediaType="items")
  MediaContainer.title1 = 'Cplus'
  MediaContainer.content = 'Items'
  MediaContainer.art = R('art-default.jpg')
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

def get_jt_stream(html):
    stream_pattern = re.compile('"(http://[^"]+)"')
    match = stream_pattern.search(html)
    if match != None:
      stream_url = match.group(1)
    return stream_url

####################################################################################################

def get_jt_name(html):
    html = html.encode("Latin-1")
    name_pattern = re.compile('<h3 class="itemTitle">([^<>]+)</h3>')
    match_name = name_pattern.search(html)
    if match_name != None:
      name = unicode(match_name.group(1),"utf-8")
    return name

####################################################################################################

from htmlentitydefs import name2codepoint 
def replace_entities(match):
    try:
        ent = match.group(1)
        if ent[0] == "#":
            if ent[1] == 'x' or ent[1] == 'X':
                return unichr(int(ent[2:], 16))
            else:
                return unichr(int(ent[1:], 10))
        return unichr(name2codepoint[ent])
    except:
        return match.group()

entity_re = re.compile(r'&(#?[A-Za-z0-9]+?);')
def html_unescape(data):
    return entity_re.sub(replace_entities, data)

####################################################################################################

def get_jt_summary(html):
    html = html.encode("utf-8")
    html = html_unescape(html)
    summary_pattern = re.compile('class="subjecttimer.*>(.*)</a>')
    try:
    	match_summary = summary_pattern.findall(html.replace('</li>','\n'))
        summary = ''
    	if match_summary != None:
    		for str in match_summary:
			Log(str)
			summary = summary + str +'\n'
    except:
    	summary = "Sommaire non disponible"
    if summary == '':
	summary = "Sommaire non disponible"
    return summary

####################################################################################################

def sub_category (sender, Emission_cat, title = None, replaceParent=False, values=None):

  dir = MediaContainer(title1="", title2=title, replaceParent=replaceParent)
  dir.viewGroup = 'Details'
  base_address = 'http://service.canal-plus.com/video/rest/getVideosLiees/cplus/'+Emission_cat
  logo_string = 'logo_h.jpg'

  html = HTTP.Request(base_address,encoding="Latin-1")
  archives_pattern = re.compile('<HD>(.*)</HD>')
  videolist = archives_pattern.findall(html) 
#  for video in videolist:
# 	dir.
  for video in videolist:
   dir.Append(VideoItem(video,title,'','08/10/12','Guignols.jpg'))
    
  return dir

####################################################################################################


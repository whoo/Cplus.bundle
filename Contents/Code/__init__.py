import re
BASE_URL = "http://service.canal-plus.com/video/rest/"

PLUGIN_PREFIX           = "/video/NCplus"
PLUGIN_ID               = "com.plexapp.plugins.CNplus"
PLUGIN_REVISION         = 0.1
PLUGIN_UPDATES_ENABLED  = True
CACHE_INTERVAL = 3600 * 2
ICON="icon-default.png"
ART= "bg-default.jpg"
NAME="Canal +"


def Start():
	Plugin.AddPrefixHandler("/video/canalplus", ListeCategories, "Canal Plus", "icon-default.png", "art-default.jpg")
	ObjectContainer.title1    = 'Canal Plus'
	ObjectContainer.art       = R(ART)
	


#Root categories
def ListeCategories():
	oc = ObjectContainer()

	icon=None
	idCategorie="39"
	nom="X"
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = idCategorie,nomSousCategorie="ZAPPING"),title="Zapping",thumb=R("LeZapping.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = idCategorie,nomSousCategorie="LES GUIGNOLS"),title="Les guignols",thumb=R("LesGuignols.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = idCategorie,nomSousCategorie="LE_PETIT_JOURNAL"),title="Le petit Journal",thumb=R("LePetitJournal.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "1080",nomSousCategorie="GROLAND_EMISSIONS"),title="GroLand",thumb=R("GroLand.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "1080",nomSousCategorie="SALUT_LES_TERRIENS"),title="Slt",thumb=R("cplus-default.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "1080",nomSousCategorie="LES_NOUVEAUX_EXPLORATEURS"),title="Explorateur",thumb=R("cplus-default.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "1080",nomSousCategorie="LE_SUPPLEMENT"),title="Le supplement",thumb=R("cplus-default.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "1080",nomSousCategorie="L_EFFET_PAPILLON"),title="L'effet papillon",thumb=R("cplus-default.jpg")))
	oc.add(DirectoryObject(key=Callback(ListeVideos,idSousCategorie = "105",nomSousCategorie="L_OEIL_DE_LINKS"),title="Oeil de links",thumb=R("cplus-default.jpg")))
	return oc


def ListeVideos(idSousCategorie, nomSousCategorie):
	oc =ObjectContainer(title1="", title2=nomSousCategorie)
	dirvideos = XML.ElementFromURL(BASE_URL + "getMEAs/cplus/" + idSousCategorie).xpath("//MEA[RUBRIQUAGE/RUBRIQUE='%s']"%(nomSousCategorie))

	tb={}
	for listv in dirvideos:
		idVideo = listv.xpath('./ID')[0].text
	        videosXml = XML.ElementFromURL(BASE_URL + "getVideosLiees/cplus/" + idVideo)
		videos = videosXml.xpath("//VIDEO")
		hack="?secret=pqzerjlsmdkjfoiuerhsdlfknaes"
		for video in videos:
			idv=video.xpath('./ID')[0].text
			titre = video.xpath('./INFOS/TITRAGE/TITRE')[0].text
			soustitre = video.xpath('./INFOS/TITRAGE/SOUS_TITRE')[0].text
			if soustitre.strip() != "":
				titre =  titre + " - " + soustitre
			description = video.xpath('./INFOS/DESCRIPTION')[0].text
			thumb = video.xpath('.//MEDIA/IMAGES/GRAND')[0].text
			video_url = video.xpath('.//MEDIA/VIDEOS/HD')[0].text
			if (video_url != None ):
				video_url=video_url.replace('rtmp://vod-fms.canalplus.fr/ondemand/videos','http://vod-flash.canalplus.fr/WWWPLUS/STREAMING')
				video_url=video_url+hack
				dd={'thumb':thumb,'summary':description,'titre':titre}
				tb[idv]={'video_url':video_url+"&"+JSON.StringFromObject(dd),'thumb':thumb,'description':description,'titre':titre}

	for idv in sorted(tb,reverse=True):
		dd=MovieObject(url=tb[idv]['video_url'],title=tb[idv]['titre'],summary=tb[idv]['description'],thumb=tb[idv]['thumb'])
		oc.add(dd)
	
	return oc


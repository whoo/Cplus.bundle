import re
BASE_URL = "http://service.canal-plus.com/video/rest/"

PLUGIN_PREFIX = "/video/NCplus"
PLUGIN_ID = "com.plexapp.plugins.CNplus"
PLUGIN_REVISION = 0.4
PLUGIN_UPDATES_ENABLED = True
CACHE_INTERVAL = 3600 * 2
ICON = "icon-default.png"
ART = "bg-default.jpg"
NAME = "Canal +"


def Start():
    Plugin.AddPrefixHandler(
        "/video/canalplus",
        ListeCategories,
        "Canal Plus",
        "icon-default.png",
     "bg-default.jpg")
    ObjectContainer.title1 = 'Canal Plus'
    ObjectContainer.art = R(ART)


# Root categories
def ListeCategories():
    oc = ObjectContainer()

    ListVids = [
        {'duree': 3, 'cat': 39, 'nom': 'ZAPPING', 'title': 'Zapping', 'icon': 'LeZapping.jpg'},
        {'duree': 5, 'cat': 39, 'nom': 'LES_GUIGNOLS', 'title': 'Les Guignols de l\'info', 'icon': 'LesGuignols.jpg'},
        {'duree': 10, 'cat': 39, 'nom': 'LE_PETIT_JOURNAL', 'title': 'Le Petit Journal', 'icon': 'LePetitJournal.jpg'},
        {'duree': 10, 'cat': 39, 'nom': 'LE_GRAND_JOURNAL', 'title': 'Le Grand Journal', 'icon': 'LeGrandJournal.jpg'},
        {'duree': 10, 'cat': 39, 'nom': 'LE.JT.DE.CANAL', 'title': 'Le Journal de canal', 'icon': 'jtcanal.jpg'},
        {'duree': 10, 'cat': 1080, 'nom': 'SALUT.LES.TERRIENS', 'title': 'Salut les Terriens', 'icon': 'Slt.jpg'},
        {'duree': 10, 'cat': 1080, 'nom': 'LES_NOUVEAUX_EXPLORATEURS', 'title': 'Les Explorateurs', 'icon': 'Explorateurs.jpg'},
        {'duree': 10, 'cat': 130, 'nom': 'GROLAND', 'title': 'GroLand', 'icon': 'GroLand.jpg'},
        {'duree': 10, 'cat': 1080, 'nom': 'LE_SUPPLEMENT', 'title': 'Le supplement politique', 'icon': 'supplementpolitique.jpg'},
        {'duree': 10, 'cat': 105, 'nom': 'L_OEIL_DE_LINKS', 'title': 'Oeil de links', 'icon': 'oeildelinks.jpg'}
    ]

    icon = None
    for a in ListVids:
        oc.add(
            DirectoryObject(
                key=Callback(
                    ListeVideos,
                    Video=a),
                title=a['title'],
                thumb=R(
                    a['icon'])))

    return oc


# Chosen sub-category's videos
def ListeVideos(Video):
    """List Video from main categorie"""
    idSousCategorie = str(Video['cat'])
    nomSousCategorie = Video['nom']

    oc = ObjectContainer(title1="", title2=Video['title'])
    regexpNS = "http://exslt.org/regular-expressions"
    dirvideos = XML.ElementFromURL(
        BASE_URL +
        "getMEAs/cplus/" +
        idSousCategorie).xpath(
        "//MEA[RUBRIQUAGE/*[re:test(., '%s', 'i')]]" %
        (nomSousCategorie),
        namespaces={
            're': regexpNS})

    tb = {}
    for listv in dirvideos:
        idVideo = listv.xpath('./ID')[0].text
        videosXml = XML.ElementFromURL(
            BASE_URL + "getVideosLiees/cplus/" + idVideo)
        videos = videosXml.xpath("//VIDEO")
        hack = "?secret=pqzerjlsmdkjfoiuerhsdlfknaes"
        for video in videos:
            idv = video.xpath('./ID')[0].text
            titre = video.xpath('./INFOS/TITRAGE/TITRE')[0].text
            soustitre = video.xpath('./INFOS/TITRAGE/SOUS_TITRE')[0].text
            duration = video.xpath('./DURATION')[0].text
            if (duration is None):
                duration = 60*6
            if soustitre.strip() != "":
                titre = titre + " - " + soustitre
            description = soustitre + " ("+str(int(duration)/60)+"min.)" + "\n" + video.xpath(
                './INFOS/DESCRIPTION')[0].text.replace('"', '\'')
            thumb = video.xpath('.//MEDIA/IMAGES/GRAND')[0].text
            if (video.xpath('.//MEDIA/VIDEOS/HD')):
                video_url = video.xpath('.//MEDIA/VIDEOS/HD')[0].text
            else:
                video_url = None
            if (int(duration)/60 > Video['duree']):
                if (video_url is not None):
                    video_url = video_url.replace(
                        'rtmp://vod-fms.canalplus.fr/ondemand/videos',
                        'http://vod-flash.canalplus.fr/WWWPLUS/STREAMING')
                    video_url = video_url.replace(
                        'rtmp://ugc-vod-fms.canalplus.fr/ondemand/videos',
                        'http://vod-flash.canalplus.fr/WWWPLUS/STREAMING')
                    # video_url=video_url.replace('http://vod-flash.canalplus.fr/WWWPLUS/GEO5','http://album.voyez.ca/WWWPLUS/GEO5')
                    video_url = video_url+hack
                    titre=titre.replace("&"," et ")
                    description=description.replace("&"," et ")
                    dd = {
                        'thumb': thumb,
                        'summary': description,
                        'titre': titre}
                    tb[idv] = {
                        'video_url': video_url+"&"+JSON.StringFromObject(dd),
                        'thumb': thumb,
                        'description': description,
                        'titre': titre}

    for idv in sorted(tb, reverse=True, key=int):
        dd = MovieObject(
            url=tb[idv]['video_url'],
            title=tb[idv]['titre'],
            summary=tb[idv]['description'],
            thumb=tb[idv]['thumb'])
        oc.add(dd)
    return oc

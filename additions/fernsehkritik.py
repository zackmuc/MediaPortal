#!/usr/bin/python
# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer, SimplePlaylist
import random

def fernsehkritikGenreListEntry(entry):
    return [entry,
        (eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
        ]
    
def fernsehkritikFilmListEntry(entry):
    return [entry,
        (eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
        ]

class fernsehkritikGenreScreen(Screen):
    
    def __init__(self, session):
        self.session = session
        self.plugin_path = mp_globals.pluginPath
        self.skin_path =  mp_globals.pluginPath + "/skins"
        
        path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
        if not fileExists(path):
            path = self.skin_path + "/original/defaultGenreScreen.xml"

        with open(path, "r") as f:
            self.skin = f.read()
            f.close()
            
        Screen.__init__(self, session)
        
        self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
            "ok"    : self.keyOK,
            "cancel": self.keyCancel
        }, -1)
        
        self.keyLocked = True
        self['title'] = Label("fernsehkritik.com")
        self['ContentTitle'] = Label("Genre:")
        self['name'] = Label("")
        self['F1'] = Label("Exit")
        self['F2'] = Label("")
        self['F3'] = Label("")
        self['F4'] = Label("")
        
        self.genreliste = []
        self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
        self.chooseMenuList.l.setItemHeight(25)
        self['genreList'] = self.chooseMenuList
        
        self.onLayoutFinish.append(self.loadPage)
        
    def loadPage(self):    
        self.genreliste = [('TV Magazin',"http://fernsehkritik.tv/tv-magazin/komplett/")]
        #more genres need to be added, (like youtube channel...)
        
        self.chooseMenuList.setList(map(fernsehkritikGenreListEntry, self.genreliste))
        self.keyLocked = False

    def keyOK(self):
        streamGenreName = self['genreList'].getCurrent()[0][0]
        streamGenreLink = self['genreList'].getCurrent()[0][1]
        print streamGenreName, streamGenreLink
        
        self.session.open(fernsehkritikFilmeListeScreen, streamGenreLink, streamGenreName)

    def keyCancel(self):
        self.close()

class fernsehkritikFilmeListeScreen(Screen):
    
    def __init__(self, session, streamGenreLink, streamGenreName):
        self.session = session
        self.streamGenreLink = streamGenreLink   #http://fernsehkritik.tv/tv-magazin/komplett/'
        self.streamGenreName = streamGenreName
        self.plugin_path = mp_globals.pluginPath
        self.skin_path =  mp_globals.pluginPath + "/skins"
        
        path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
        if not fileExists(path):
            path = self.skin_path + "/original/defaultListScreen.xml"

        with open(path, "r") as f:
            self.skin = f.read()
            f.close()
            
        Screen.__init__(self, session)
        
        self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
            "ok"    : self.keyOK,
            "cancel": self.keyCancel,
            "up" : self.keyUp,
            "down" : self.keyDown,
            "right" : self.keyRight,
            "left" : self.keyLeft,
            "nextBouquet" : self.keyPageUp,
            "prevBouquet" : self.keyPageDown
        }, -1)

        self['title'] = Label("fernsehkritik.tv")
        self['ContentTitle'] = Label("%s:" % self.streamGenreName)
        self['name'] = Label("")
        self['F1'] = Label("Exit")
        self['F2'] = Label("")
        self['F3'] = Label("")
        self['F4'] = Label("")
        self['handlung'] = Label("")
        self['page'] = Label("")
        self['Page'] = Label("")
        self['coverArt'] = Pixmap()
        
        self.keyLocked = True
        self.streamFolge = ''
        self.streamLink = ''
        self.page = 1
        self.filmliste = []
        self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
        self.chooseMenuList.l.setItemHeight(25)
        self['liste'] = self.chooseMenuList
        
        self.onLayoutFinish.append(self.loadPage)
        
    def loadPage(self): 
        url = str(self.streamGenreLink)
        getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
        
    def dataError(self, error):
        print 'Fehler lesen fernsehkritik.tv', error
        
    def loadPageData(self, data):
        folgen = re.findall('<h2>\s*<a[^>]+href="(?:\.\.|)?/folge-(\d+)/?"[^>]*>\s*Folge (?:\d+) vom (\d{1,2}\. [\wä]+ \d{4})\s*</a>', data, re.S)
        self.filmliste = []
        for folge, datum in folgen:
            fTitle = "Folge " + folge + " vom " + datum
            fLink = "http://fernsehkritik.tv/folge-" + folge + "/Start/"
            self.filmliste.append((fTitle,fLink))
        self.chooseMenuList.setList(map(fernsehkritikFilmListEntry, self.filmliste))
        self.keyLocked = False 

    def keyOK(self):
        if self.keyLocked:
            return
        self.streamFolge = self['liste'].getCurrent()[0][0]
        self.streamLink = self['liste'].getCurrent()[0][1]
        print self.streamLink
        getPage(self.streamLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.buildStreamLinks).addErrback(self.dataError)

    def buildStreamLinks(self, data):
        #Streams Links ermitteln und an SimplePlayer Class übergeben
        streamLinks = []
        rand = str(random.randint(1, 3))
        folgenNr = re.findall(r"\{ url: base \+ '(\d+(?:-\d+)?\.flv)' \}", data, re.S)
        for folgeNr in folgenNr:
            url = "dl" + rand + ".fernsehkritik.tv/fernsehkritik" + folgeNr
            streamLinks.append(url)
        print streamLinks
        self.session.open(fernsehkritiktvPlayer,streamLinks,playIdx=0,playAll = True,
            listTitle = "fernsehkritiv.tv"
            )   

    def keyLeft(self):
        if self.keyLocked:
            return
        self['liste'].pageUp()
        
    def keyRight(self):
        if self.keyLocked:
            return
        self['liste'].pageDown()
        
    def keyUp(self):
        if self.keyLocked:
            return
        self['liste'].up()

    def keyDown(self):
        if self.keyLocked:
            return
        self['liste'].down()
        
    def keyPageDown(self):
        print "PageDown"
        if self.keyLocked:
            return
        if not self.page < 2:
            self.page -= 1
            self.loadPage()

    def keyPageUp(self):
        print "PageUP"
        if self.keyLocked:
            return
        self.page += 1
        self.loadPage()
            
    def keyCancel(self):
        self.close()


class fernsehkritiktvPlayer(SimplePlayer):

    def __init__(self, session, playList, playIdx=0, playAll=False, listTitle=None):
        print "Fernsehkritik Plaxer:"

        SimplePlayer.__init__(self, session, playList, playIdx, playAll, listTitle)
        
    def getVideo(self):
        stvLink = self.playList[self.playIdx][2]
        stvTitle = "%s%s" % (self.playList[self.playIdx][0], self.playList[self.playIdx][1])
        self.playStream(stvTitle, stvLink)

    def openPlaylist(self):
        self.session.openWithCallback(self.cb_Playlist, fernsehkritiktvPlaylist, self.playList, self.playIdx, listTitle=self.listTitle)
        
class fernsehkritiktvPlaylist(SimplePlaylist):

    def __init__(self, session, playList, playIdx, listTitle=None):

        SimplePlaylist.__init__(self, session, playList, playIdx, listTitle)
        
    def playListEntry(self, entry):
        return [entry,
            (eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+entry[1])
            ]     
 
                
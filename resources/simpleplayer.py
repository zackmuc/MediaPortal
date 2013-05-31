#	-*-	coding:	utf-8	-*-

import random
from Screens.InfoBarGenerics import *
from Plugins.Extensions.MediaPortal.resources.imports import *
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/mediainfo/plugin.pyo'):
	from Plugins.Extensions.mediainfo.plugin import mediaInfo
	MediainfoPresent = True
else:
	MediainfoPresent = False

class SimplePlayer(Screen, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):
	ENABLE_RESUME_SUPPORT = True
	ALLOW_SUSPEND = True
	
	#prepared for MP infobar
	skin = '\n\t\t<screen position="center,center" size="300,200" title="MP Player">\n\t\t</screen>'
	
	def __init__(self, session, playList, playIdx=0, playAll=False, listTitle=None):
		Screen.__init__(self, session)
		print "SimplePlayer:"
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		
		self["actions"] = ActionMap(["WizardActions",'MediaPlayerSeekActions',"EPGSelectActions",'MoviePlayerActions','ColorActions','InfobarActions'],
		{
			"leavePlayer": self.leavePlayer,
			"info":		self.openMediainfo,
			"input_date_time": self.openMenu,
			"up": 		self.openPlaylist,
			"down":		self.playRandom,
			"back":		self.leavePlayer,
			"left":		self.playPrevStream,
			"right":	self.playNextStream

		}, -1)
		
		InfoBarNotifications.__init__(self)
		InfoBarBase.__init__(self)
		InfoBarShowHide.__init__(self)

		self.allowPiP = False
		InfoBarSeek.__init__(self)

		#self.skinName = 'MediaPortal SimplePlayer'
		self.skinName = 'MoviePlayer'
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()

		self.randomPlay = False
		self.playMode = ""
		self.listTitle = listTitle
		self.playAll = playAll
		self.playList = playList
		self.playIdx = playIdx
		self.playLen = len(playList)
		self.returning = False
		
		self.setPlaymode()
		self.onClose.append(self.playExit)

		self.onLayoutFinish.append(self.getVideo)
			
	def playVideo(self):
		print "playVideo:"
		if not self.playAll:
			self.close()
		else:
			self.getVideo()
	
	def dataError(self, error):
		print "dataError:"
		print error
		self.playNextStream()
		
	def playStream(self, title, url):
		print "playStream: ",title,url
		sref = eServiceReference(0x1001, 0, url)
		sref.setName(title)
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def playPrevStream(self):
		print "_prevStream:"
		if self.playIdx > 0:
			self.playIdx -= 1
		else:
			self.playIdx = self.playLen - 1
		self.playVideo()
		
	def playNextStream(self):
		print "playNextStream:"
		if self.playIdx in range(0, self.playLen-1):
			self.playIdx += 1
		else:
			self.playIdx = 0
		self.playVideo()

	def playRandom(self):
		print 'playRandom:'
		if self.playLen > 1:
			self.playIdx = random.randint(0, self.playLen-1)
			self.playVideo()
	
	def seekFwd(self):
		self.playNextStream()
		
	def seekBack(self):
		self.playPrevStream()
	
	def leavePlayer(self):
		print "exitPlayer:"
		self.close()

	def doEofInternal(self, playing):
		print "doEofInt:"
		if playing == True:
			if self.randomPlay:
				self.playRandom()
			else:
				self.playNextStream()
				
	def playExit(self):
		print "playExit:"
		self.session.nav.playService(self.lastservice)

	def getVideo(self):
		print "getVideo:"
		self.close()

	def openPlaylist(self):
		self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList, self.playIdx, listTitle=self.listTitle)
		
	def cb_Playlist(self, data):
		if data != -1:
			self.playIdx = data
			self.getVideo()
			
	def openMediainfo(self):
		if MediainfoPresent:
			url = self.session.nav.getCurrentlyPlayingServiceReference().getPath()
			if re.match('.*?http://', url, re.S):
				self.session.open(mediaInfo, True)

	def openMenu(self):
		self.session.openWithCallback(self.cb_Menu, SimplePlayerMenu)
		
	def cb_Menu(self, data):
		print "cb_Menu:"
		if data != []:
			if data[0][0] == 1:
				self.setPlaymode()
		
	def lockShow(self):
		pass
		
	def unlockShow(self):
		pass
		
	def setPlaymode(self):
		print "setPlaymode:"
		self.randomPlay = config.mediaportal.sp_randomplay.value
		if self.randomPlay:
			self.playMode = "Random"
		else:
			self.playMode = "Next"
	
class SimplePlaylist(Screen):

	def __init__(self, session, playList, playIdx, listTitle=None):
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
		
		self['OkCancelActions'] = HelpableActionMap(self, 'OkCancelActions',
		{
			'cancel':	self.exit,
			'ok': 		self.ok
		}, -1)
			
		self.playList = playList
		self.playIdx = playIdx
		self.listTitle = listTitle

		self['title'] = Label("Playlist")
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.showPlaylist)

	def playListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			] 
		
	def showPlaylist(self):
		print 'showPlaylist:'
		if self.listTitle != None:
			self['ContentTitle'].setText(self.listTitle)
		else:
			self['ContentTitle'].setText("Auswahl")

		self.chooseMenuList.setList(map(self.playListEntry, self.playList))
		self['genreList'].moveToIndex(self.playIdx)

	def exit(self):
		self.close(-1)

	def ok(self):
		idx = self['genreList'].getSelectedIndex()
		self.close(idx)

class SimpleConfig(ConfigListScreen, Screen):
	skin = '\n\t\t<screen position="center,center" size="300,200" title="MP Player Konfiguration">\n\t\t\t<widget name="config" position="10,10" size="290,190" scrollbarMode="showOnDemand" />\n\t\t</screen>'
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self.list.append(getConfigListEntry('Random Play', config.mediaportal.sp_randomplay))
		ConfigListScreen.__init__(self, self.list)
		self['setupActions'] = ActionMap(['SetupActions'],
		{
			'ok': 		self.save,
			'cancel': 	self.keyCancel
		},-2)
		
	def save(self):
		for x in self['config'].list:
			x[1].save()
	
		self.close()
	
	def keyCancel(self):
		for x in self['config'].list:
			x[1].cancel()
	
		self.close()

class SimplePlayerMenu(Screen):
	skin = '\n\t\t<screen position="center,center" size="300,200" title="MP Player Menü">\n\t\t\t<widget name="menu" position="10,10" size="290,190" scrollbarMode="showOnDemand" />\n\t\t</screen>'
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self['setupActions'] = ActionMap(['SetupActions'],
		{
			'ok': 		self.keyOk,
			'cancel':	self.keyCancel
		}, -2)

		self.liste = []
		self.liste.append(('Konfiguration', 1))
		self['menu'] = MenuList(self.liste)
		
	def openConfig(self):
		self.session.open(SimpleConfig)
		self.close([(1, None)])
		
	def keyOk(self):
		choice = self['menu'].l.getCurrentSelection()[1]
		if choice == 1:
			self.openConfig()
		
	def keyCancel(self):
		self.close([])

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
	
	def __init__(self, session, playList, playIdx=0, playAll=False, listTitle=None, plType='local', title_inr=0, cover=False):
	
		Screen.__init__(self, session)
		print "SimplePlayer:"
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/tec/SimplePlayer.xml" % self.skin_path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()	
		
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

		self.skinName = 'MediaPortal SimplePlayer'
		#self.skinName = 'MoviePlayer'
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()
		
		self.randomPlay = False
		self.playMode = ""
		self.listTitle = listTitle
		self.playAll = playAll
		self.playList = playList
		self.playIdx = playIdx
		self.playLen = len(playList)
		self.returning = False
		self.pl_entry = ['', '', '']
		self.plType = plType
		self.playList2 = []
		self.pl_name = ''
		self.title_inr = title_inr
		self.cover = cover
		
		# load default cover
		self['Cover'] = Pixmap()
		self.ShowCover()
		
		self.setPlaymode()
		self.onClose.append(self.playExit)

		self.onLayoutFinish.append(self.getVideo)
			
	def playVideo(self):
		print "playVideo:"
		if not self.playAll:
			self.close()
		else:
			if self.plType == 'global':
				self.getVideo2()
			else:
				self.getVideo()
	
	def dataError(self, error):
		print "dataError:"
		print error
		self.playNextStream()
		
	def playStream(self, title, url, album='', artist=''):
		print "playStream: ",title,url
		sref = eServiceReference(0x1001, 0, url)
		sref.setName(title)
		pos = title.find('. ', 0, 5)
		if pos > 0:
			pos += 2
			title = title[pos:]
		self.pl_entry = [title, None, artist, album]
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

	def getVideo2(self):
		print "getVideo2:"
		if self.playLen > 0:
			titel = self.playList2[self.playIdx][0]
			url = self.playList2[self.playIdx][1]
			album = self.playList2[self.playIdx][2]
			artist = self.playList2[self.playIdx][3]
			self.playStream(titel, url, album, artist)
		else:
			self.close()
				
	def openPlaylist(self):
		if self.playLen > 0:
			if self.plType == 'local':
				self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList, self.playIdx, listTitle=self.listTitle, plType=self.plType, title_inr=self.title_inr)
			else:
				self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList2, self.playIdx, listTitle=None, plType=self.plType, title_inr=0)
		
	def cb_Playlist(self, data):
		if data[0] != -1:
			self.playIdx = data[0]
			if self.plType == 'global':
				if data[1] == 'del':
					self.session.nav.stopService()
					SimplePlaylistIO.delEntry(self.pl_name, self.playList2, self.playIdx)
					self.playLen = len(self.playList2)
					if self.playIdx >= self.playLen:
						self.playIdx -= 1
					if self.playIdx < 0:
						self.close()
				else:
					self.getVideo2()
			else:
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
			if data[0] == 1:
				self.setPlaymode()
			elif data[0] == 2:
				url = self.session.nav.getCurrentlyPlayingServiceReference().getPath()
				if re.match('.*?(putpat.tv|myvideo)', url, re.I):
					self.session.open(MessageBox, _("Fehler: URL ist nicht persistent !"), MessageBox.TYPE_INFO, timeout=5)
					return
					
				self.pl_entry[1] = url
				self.pl_name = data[1]
				res = SimplePlaylistIO.addEntry(data[1], self.pl_entry)
				if res == 1:
					self.session.open(MessageBox, _("Eintrag hinzugefügt"), MessageBox.TYPE_INFO, timeout=5)
				elif res == 0:
					self.session.open(MessageBox, _("Eintrag schon vorhanden"), MessageBox.TYPE_INFO, timeout=5)
				else:
					self.session.open(MessageBox, _("Fehler!"), MessageBox.TYPE_INFO, timeout=5)

			elif data[0] == 3:
				self.pl_name = data[1]
				pl_list = SimplePlaylistIO.getPL(data[1])
				if pl_list != []:
					self.session.nav.stopService()
					self.playList2 = pl_list
					self.playIdx = 0
					self.playLen = len(self.playList2)
					self.plType = 'global'
					self.openPlaylist()
					
			elif data[0] == 4:
				if self.plType != 'local':
					self.plType = 'local'
					self.pl_name = ''
					self.playIdx = 0
					self.playLen = len(self.playList)
					self.playList2 = []
				if self.playLen > 0:
					self.openPlaylist()

	def ShowCover(self):
		print "Simpler Player Load Cover:", self.cover
		if self.cover:
			if fileExists("/tmp/Icon.jpg"):
				print "YEEEESSSSSS"
				self['Cover'].instance.setPixmap(gPixmapPtr())
				self.scale = AVSwitch().getFramebufferScale()
				self.picload = ePicLoad()
				size = self['Cover'].instance.size()
				self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
				if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
					ptr = self.picload.getData()
					if ptr != None:
						self['Cover'].instance.setPixmap(ptr)
						self['Cover'].show()
						del self.picload
			else:
				print "Simpler Player Load Cover:", self.cover, "kein cover vorhanden."
					
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

	def __init__(self, session, playList, playIdx, listTitle=None, plType='local', title_inr=0):
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
		
		self["actions"] = ActionMap(["OkCancelActions",'MediaPlayerSeekActions',"EPGSelectActions",'ColorActions','InfobarActions'],
		{
			'cancel':	self.exit,
			'red':		self.red,
			'ok': 		self.ok
		}, -2)
		
		self.playList = playList
		self.playIdx = playIdx
		self.listTitle = listTitle
		self.plType = plType
		self.title_inr = title_inr

		self['title'] = Label("Playlist")
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		if self.plType == 'global':
			self['F1'] = Label("Löschen")
		else:
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
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[self.title_inr])
			] 
		
	def showPlaylist(self):
		print 'showPlaylist:'
		if self.listTitle != None:
			self['ContentTitle'].setText(self.listTitle)
		else:
			self['ContentTitle'].setText("Auswahl")

		self.chooseMenuList.setList(map(self.playListEntry, self.playList))
		self['genreList'].moveToIndex(self.playIdx)
	
	def red(self):
		if self.plType == 'global':
			idx = self['genreList'].getSelectedIndex()
			"""
			del playList[idx:idx+1]
			if len(self.playList) == 0:
				self.close([0,'del',self.playList])
			else:
				self.chooseMenuList.setList(map(self.playListEntry, self.playList))
				self['genreList'].moveToIndex(self.playIdx)
			"""
			self.close([idx,'del',self.playList])

	def exit(self):
		self.close([-1,'',self.playList])

	def ok(self):
		idx = self['genreList'].getSelectedIndex()
		self.close([idx,'',self.playList])

class SimpleConfig(ConfigListScreen, Screen):
	skin = '\n\t\t<screen position="center,center" size="300,200" title="MP Player Konfiguration">\n\t\t\t<widget name="config" position="10,10" size="290,190" scrollbarMode="showOnDemand" />\n\t\t</screen>'
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self.list.append(getConfigListEntry('Random Play', config.mediaportal.sp_randomplay))
		self.list.append(getConfigListEntry('Youtube VideoPrio', config.mediaportal.youtubeprio))
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
		self.liste.append(('Configuration', 1))
		self.liste.append(('Add service to global playlist', 2))
		self.liste.append(('Open global playlist', 3))
		self.liste.append(('Open local playlist', 4))
		self['menu'] = MenuList(self.liste)
		
	def openConfig(self):
		self.session.open(SimpleConfig)
		self.close([1, ''])
		
	def addToPlaylist(self, id, name):
		self.close([id, name])
		
	def openPlaylist(self, id, name):
		self.close([id, name])
		
	def keyOk(self):
		choice = self['menu'].l.getCurrentSelection()[1]
		if choice == 1:
			self.openConfig()
		elif choice == 2:
			self.addToPlaylist(2, 'mp_global_pl_01')
		elif choice == 3:
			self.openPlaylist(3, 'mp_global_pl_01')
		elif choice == 4:
			self.openPlaylist(4, '')
		
	def keyCancel(self):
		self.close([])

class SimplePlaylistIO:
		
	@staticmethod
	def delEntry(pl_name, list, idx):
		print "delEntry:"
		
		assert pl_name != None
		assert list != [] and idx in range(0, len(list))
		
		pl_path = config.mediaportal.watchlistpath.value + pl_name
		del list[idx:idx+1]
		l = len(list)
		j = 0
		try:
			f1 = open(pl_path, 'w')
			while j < l:
				wdat = '<title>%s</<url>%s</<album>%s</<artist>%s</\n' % (list[j][0], list[j][1], list[j][2], list[j][3])
				f1.write(wdat)
				j += 1
					
			f1.close()
			
		except IOError, e:
			print "Fehler:\n",e
			print "eCode: ",e
			f1.close()
	
	@staticmethod
	def addEntry(pl_name, entry):
		print "addEntry:"
		
		album = entry[3]
		artist = entry[2]
		url = entry[1]
		title = entry[0].replace('\n\t', ' - ')
		title = title.replace('\n', ' - ')

		assert pl_name != None
		
		pl_path = config.mediaportal.watchlistpath.value + pl_name
		try:
			if fileExists(pl_path):
				f1 = open(pl_path, 'a+')
				
				data = f1.read()
				m = re.findall('<url>(.*?)</', data)
				if m:
					found = False
					for x in m:
						if x == url:
							found = True
							break
				
					if found:
						f1.close()
						return 0
			else:
				f1 = open(pl_path, 'w')
		
			wdat = '<title>%s</<url>%s</<album>%s</<artist>%s</\n' % (title, url, album, artist)
			f1.write(wdat)
			f1.close()
			return 1
		
		except IOError, e:
			print "Fehler:\n",e
			print "eCode: ",e
			f1.close()
			return -1
	
	@staticmethod
	def getPL(pl_name):
		print "getPL:"
		
		list = []
		
		assert pl_name != None
			
		pl_path = config.mediaportal.watchlistpath.value + pl_name
		try:
			if not fileExists(pl_path):
				f_new = True
			else:
				f_new = False
				f1 = open(pl_path, 'r')
					
			if not f_new:
				while True:
					entry = f1.readline().strip()
					print "entry: ",entry
					if entry == "":
						break
					m = re.search('<title>(.*?)</<url>(.*?)</<album>(.*?)</<artist>(.*?)</', entry) 
					if m:
						print "m:"
						titel = m.group(1)
						url = m.group(2)
						album = m.group(3)
						artist = m.group(4)
						list.append((titel, url, album, artist))
				
				f1.close()
			
			return list
				
		except IOError, e:
			print "Fehler:\n",e
			print "eCode: ",e
			f1.close()

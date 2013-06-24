#	-*-	coding:	utf-8	-*-

import Queue
import random
from Screens.InfoBarGenerics import *
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.youtubelink import YoutubeLink
from Plugins.Extensions.MediaPortal.resources.putpattvlink import PutpattvLink
from Plugins.Extensions.MediaPortal.resources.myvideolink import MyvideoLink
from Plugins.Extensions.MediaPortal.resources.songstolink import SongstoLink
from Plugins.Extensions.MediaPortal.resources.cannalink import CannaLink
from Plugins.Extensions.MediaPortal.resources.eightieslink import EightiesLink
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/mediainfo/plugin.pyo'):
	from Plugins.Extensions.mediainfo.plugin import mediaInfo
	MediainfoPresent = True
else:
	MediainfoPresent = False

class SimplePlayer(Screen, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide, InfoBarAudioSelection, InfoBarSubtitleSupport):
	ENABLE_RESUME_SUPPORT = True
	ALLOW_SUSPEND = True
	
	def __init__(self, session, playList, playIdx=0, playAll=False, listTitle=None, plType='local', title_inr=0, cover=False, ltype='', autoScrSaver=False):
	
		Screen.__init__(self, session)
		print "SimplePlayer:"
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		self.wallicon_path = mp_globals.pluginPath + "/icons_wall/"

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
		#InfoBarServiceNotifications.__init__(self)
		InfoBarBase.__init__(self)
		InfoBarShowHide.__init__(self)
		InfoBarAudioSelection.__init__(self)
		InfoBarSubtitleSupport.__init__(self)
		
		self.allowPiP = False
		InfoBarSeek.__init__(self)

		self.skinName = 'MediaPortal SimplePlayer'
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()
		
		self.scrSaver = ''
		self.saverActive = False
		self.autoScrSaver = autoScrSaver
		self.pl_open = False
		self.randomPlay = False
		self.playMode = ""
		self.listTitle = listTitle
		self.playAll = playAll
		self.playList = playList
		self.playIdx = playIdx
		self.playLen = len(playList)
		self.returning = False
		self.pl_entry = ['', '', '', '', '', '', '', '']
		self.plType = plType
		self.playList2 = []
		self.pl_name = ''
		self.title_inr = title_inr
		self.cover = cover
		self.ltype = ltype
		self.playlistQ = Queue.Queue(0)
		self.pl_status = (0, '', '', '', '')
		self.pl_event = SimpleEvent()
		self['Icon'] = Pixmap()
		
		# load default cover
		self['Cover'] = Pixmap()

		self.SaverTimer = eTimer()
		self.SaverTimer.callback.append(self.openSaver)
		
		self.setPlaymode()
		self.configSaver()
		self.onClose.append(self.playExit)
		#self.onFirstExecBegin.append(self.showCover)
		self.onFirstExecBegin.append(self.showIcon)
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
		
	def playStream(self, title, url=None, album='', artist='', imgurl=''):
		print "playStream: ",title,url
		if url == None:
			return
			
		if self.cover:
			self.showCover(imgurl)
		
		sref = eServiceReference(0x1001, 0, url)
		
		pos = title.find('. ', 0, 5)
		if pos > 0:
			pos += 2
			title = title[pos:]
			
		if artist != '':
			sref.setName(artist + ' - ' + title)
		else:
			sref.setName(title)
			
		self.pl_entry = [title, None, artist, album, self.ltype, '', imgurl]
		self.session.nav.stopService()
		self.session.nav.playService(sref)
		
		self.pl_status = (self.playIdx, title, artist, album, imgurl, self.plType)
		if self.pl_open:
			self.playlistQ.put(self.pl_status)
			self.pl_event.genEvent()

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
			titel = self.playList2[self.playIdx][1]
			url = self.playList2[self.playIdx][2]
			album = self.playList2[self.playIdx][3]
			artist = self.playList2[self.playIdx][4]
			imgurl = self.playList2[self.playIdx][7]
			if len(self.playList2[self.playIdx]) < 6:
				ltype = ''
			else:
				ltype = self.playList2[self.playIdx][5]
				
			if ltype == 'youtube':
				YoutubeLink(self.session).getLink(self.playStream, self.dataError, titel, url, imgurl)
			elif ltype == 'putpattv':
				token = self.playList2[self.playIdx][6]
				PutpattvLink(self.session).getLink(self.playStream, self.dataError, titel, url, token, imgurl)
			elif ltype == 'myvideo':
				token = self.playList2[self.playIdx][6]
				MyvideoLink(self.session).getLink(self.playStream, self.dataError, titel, url, token, imgurl)
			elif ltype == 'songsto':
				token = self.playList2[self.playIdx][6]
				SongstoLink(self.session).getLink(self.playStream, self.dataError, titel, artist, album, token, imgurl)
			elif ltype == 'canna':
				CannaLink(self.session).getLink(self.playStream, self.dataError, titel, artist, album, url, imgurl)
			elif ltype == 'eighties':
				token = self.playList2[self.playIdx][6]
				EightiesLink(self.session).getLink(self.playStream, self.dataError, titel, artist, album, url, token, imgurl)
			elif url:
				self.playStream(titel, url, album, artist, imgurl=imgurl)
		else:
			self.close()
				
	def openPlaylist(self):
		if self.playLen > 0:
			if self.playlistQ.empty():
				self.playlistQ.put(self.pl_status)
			self.pl_open = True
			self.pl_event.genEvent()
			
			if self.plType == 'local':
				self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList, self.playIdx, listTitle=self.listTitle, plType=self.plType, title_inr=self.title_inr, queue=self.playlistQ, mp_event=self.pl_event)
			else:
				self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList2, self.playIdx, listTitle=None, plType=self.plType, title_inr=0, queue=self.playlistQ, mp_event=self.pl_event)
		
	def cb_Playlist(self, data):
		self.pl_open = False
		
		while not self.playlistQ.empty():
			t = self.playlistQ.get_nowait()
			
		if data[0] != -1:
			self.playIdx = data[0]
			if self.plType == 'global':
				if data[1] == 'del':
					self.session.nav.stopService()
					self.playList2 = SimplePlaylistIO.delEntry(self.pl_name, self.playList2, self.playIdx)
					self.playLen = len(self.playList2)
					if self.playIdx >= self.playLen:
						self.playIdx -= 1
					if self.playIdx < 0:
						self.close()
					else:
						self.openPlaylist()
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
		self.session.openWithCallback(self.cb_Menu, SimplePlayerMenu, self.plType)
		
	def cb_Menu(self, data):
		print "cb_Menu:"
		if data != []:
			if data[0] == 1:
				self.setPlaymode()
				self.configSaver()
			elif data[0] == 2:
				if self.plType != 'local':
					self.session.open(MessageBox, _("Fehler: Service darf nur von der lok. PL hinzugefügt werden"), MessageBox.TYPE_INFO, timeout=5)
					return
					
				url = self.session.nav.getCurrentlyPlayingServiceReference().getPath()
				
				if re.match('.*?(putpattv)', url, re.I):
					self.session.open(MessageBox, _("Fehler: URL ist nicht persistent !"), MessageBox.TYPE_INFO, timeout=5)
					return
				
				if self.pl_entry[4] == 'youtube':
					url = self.playList[self.playIdx][2]
				elif self.pl_entry[4] == 'putpattv':
					url = self.playList[self.playIdx][1]
					self.pl_entry[5] = self.playList[self.playIdx][2]
				elif self.pl_entry[4] == 'myvideo':
					url = self.playList[self.playIdx][1]
					self.pl_entry[5] = self.playList[self.playIdx][2]
					
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

	def showCover(self, cover):
		print "showCover:", cover
		pm_file = "/tmp/Icon.jpg"
		if cover:
			downloadPage(cover, pm_file).addCallback(self.showPixmap, pm_file, 'Cover')
	
	def showIcon(self):
		print "showIcon:"
		pm_file = self.wallicon_path + mp_globals.activeIcon + ".png"
		self.showPixmap(None, pm_file, 'Icon')
		
	def showPixmap(self, dummy, pm_file, pm_name):
		print "showPixmap: ", pm_file
		if fileExists(pm_file):
			self[pm_name].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self[pm_name].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(pm_file, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self[pm_name].instance.setPixmap(ptr)
					self[pm_name].show()
					del self.picload
		else:
			print "No pixmap to load: ", pm_file
					
	#def lockShow(self):
	#	pass
		
	#def unlockShow(self):
	#	pass
	
	def configSaver(self):
		print "configSaver:"
		self.scrSaver = config.mediaportal.sp_scrsaver.value
		print "Savermode: ",self.scrSaver
		if self.scrSaver == 'automatic' and self.autoScrSaver or self.scrSaver == 'on':
			if not self.saverActive:
				self.SaverTimer.start(1000*60, True)
				self.saverActive = True
				print "scrsaver timer startet"
		else:
			self.SaverTimer.stop()
			self.saverActive = False

	def openSaver(self):
		print "openSaver:"
		self.session.openWithCallback(self.cb_Saver, SimpleScreenSaver) 
		
	def cb_Saver(self):
		print "cb_Saver:"
		self.saverActive = False
		self.configSaver()
		
	def setPlaymode(self):
		print "setPlaymode:"
		self.randomPlay = config.mediaportal.sp_randomplay.value
		if self.randomPlay:
			self.playMode = "Random"
		else:
			self.playMode = "Next"

class SimplePlaylist(Screen):

	def __init__(self, session, playList, playIdx, listTitle=None, plType='local', title_inr=0, queue=None, mp_event=None):
		self.session = session
	
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/showSongstoAll.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/showSongstoAll.xml"

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
		self.playlistQ = queue
		self.event = mp_event

		self["title"] = Label("")
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("")
		if self.plType == 'global':
			self['F1'] = Label("Löschen")
		else:
			self['F1'] = Label("")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		
		#self.updateTimer = eTimer()
		#self.updateTimer.callback.append(self.updateStatus)

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['streamlist'] = self.chooseMenuList
		
		self.onClose.append(self.resetEvent)
		
		self.onLayoutFinish.append(self.showPlaylist)

	def updateStatus(self):
		print "updateStatus:"
		if self.playlistQ and not self.playlistQ.empty():
			t = self.playlistQ.get_nowait()
			self["songtitle"].setText(t[1])
			self["artist"].setText(t[2])
			self["album"].setText(t[3])
			self.getCover(t[4])
			if t[5] == self.plType:
				self.playIdx = t[0]
				if self.playIdx >= len(self.playList):
					self.playIdx = 0
				self['streamlist'].moveToIndex(self.playIdx)
			
		#self.updateTimer.start(1000, True)
	
	def playListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[self.title_inr])
			] 
		
	def showPlaylist(self):
		print 'showPlaylist:'
		
		if self.listTitle:
			self['title'].setText("MP Playlist - %s" % self.listTitle)
		else:
			self['title'].setText("MP %s Playlist" % self.plType)

		self.chooseMenuList.setList(map(self.playListEntry, self.playList))
		
		if self.event:
			self.event.addCallback(self.updateStatus)
		else:
			self['streamlist'].moveToIndex(self.playIdx)
		#self.updateTimer.start(100, True)
		
	
	def getCover(self, url):
		print "getCover:", url
		if url:
			downloadPage(url, "/tmp/Icon.jpg").addCallback(self.showCover)
		else:
			self.showCoverNone()
	
	def showCover(self, picData):
		print "showCover:"
		picPath = "/tmp/Icon.jpg"
		self.showCoverFile(picPath)
		
	def showCoverNone(self):
		print "showCoverNone:"
		picPath = self.skin_path+"/original/images/m_no_coverArt.png"
		self.showCoverFile(picPath)
	
	def showCoverFile(self, picPath):
		print "showCoverFile:"
		if fileExists(picPath):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload
		else:
			print "coverfile not found: ", picPath
					
	def red(self):
		if self.plType == 'global':
			idx = self['streamlist'].getSelectedIndex()
			"""
			del playList[idx]
			l = len(self.playList)
			if l == 0:
				self.close([-1,'',self.playList])
			else:
				self.chooseMenuList.setList(map(self.playListEntry, self.playList))
				if self.playIdx not in range(0, l):
					self.playIdx -= 1
				self['genreList'].moveToIndex(self.playIdx)
			"""
			self.close([idx,'del',self.playList])

	def exit(self):
		self.close([-1,'',self.playList])

	def ok(self):
		if len(self.playList) == 0:
			self.exit()
		idx = self['streamlist'].getSelectedIndex()
		self.close([idx,'',self.playList])
		
	def resetEvent(self):
		print "resetEvent:"
		if self.event:
			self.event.reset()

class SimpleConfig(ConfigListScreen, Screen):
	skin = '\n\t\t<screen position="center,center" size="300,200" title="MP Player Konfiguration">\n\t\t\t<widget name="config" position="10,10" size="290,190" scrollbarMode="showOnDemand" />\n\t\t</screen>'
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self.list.append(getConfigListEntry('Random Play', config.mediaportal.sp_randomplay))
		self.list.append(getConfigListEntry('Screensaver', config.mediaportal.sp_scrsaver))
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
	
	def __init__(self, session, pltype):
		Screen.__init__(self, session)
		self.session = session
		self.pltype = pltype
		self['setupActions'] = ActionMap(['SetupActions'],
		{
			'ok': 		self.keyOk,
			'cancel':	self.keyCancel
		}, -2)

		self.liste = []
		self.liste.append(('Configuration', 1))
		if pltype in ('local', 'extern') :
			self.liste.append(('Add service to global playlist', 2))
			if pltype == 'local':
				self.liste.append(('Open global playlist', 3))
		else:
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
		assert list != []
		
		pl_path = config.mediaportal.watchlistpath.value + pl_name
		
		l = len(list)
		if idx in range(0, l):
			del list[idx]
			l = len(list)
			
		j = 0
		try:
			f1 = open(pl_path, 'w')
			while j < l:
				wdat = '<title>%s</<url>%s</<album>%s</<artist>%s</<ltype %s/><token %s/><img %s/>\n' % (list[j][1], list[j][2], list[j][3], list[j][4], list[j][5], list[j][6], list[j][7])
				f1.write(wdat)
				j += 1
					
			f1.close()
			return list
			
		except IOError, e:
			print "Fehler:\n",e
			print "eCode: ",e
			f1.close()
			return list
	
	@staticmethod
	def addEntry(pl_name, entry):
		print "addEntry:"
		
		imgurl = entry[6]
		token = entry[5]
		ltype = entry[4]
		album = entry[3]
		artist = entry[2]
		url = entry[1]
		title = entry[0].replace('\n\t', ' - ')
		title = title.replace('\n', ' - ')
		
		if token == None:
			token = ''
			
		if url == None:
			url = ''
			
		if imgurl == None:
			imgurl = ''
			
		cmptup = (url, artist, title)

		assert pl_name != None
		
		pl_path = config.mediaportal.watchlistpath.value + pl_name
		try:
			if fileExists(pl_path):
				f1 = open(pl_path, 'a+')
				
				data = f1.read()
				m = re.findall('<title>(.*?)</<url>(.*?)</.*?<artist>(.*?)</', data)
				if m:
					found = False
					for (t,u,a) in m:
						if (u,a,t)  == cmptup:
							found = True
							break
				
					if found:
						f1.close()
						return 0
			else:
				f1 = open(pl_path, 'w')
		
			wdat = '<title>%s</<url>%s</<album>%s</<artist>%s</<ltype %s/><token %s/><img %s/>\n' % (title, url, album, artist, ltype, token, imgurl)
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
					m2 = re.search('<ltype (.*?)/>', entry)
					m3 = re.search('<token (.*?)/>', entry)
					m4 = re.search('<img (.*?)/>', entry)
					if m:
						print "m:"
						titel = m.group(1)
						url = m.group(2)
						album = m.group(3)
						artist = m.group(4)
						if m2:
							ltype = m2.group(1)
						else:
							ltype = ''
						if m3:
							token = m3.group(1)
						else:
							token = ''
						if m4:
							imgurl = m4.group(1)
						else:
							imgurl = ''
							
						if artist != '':
							name = "%s - %s" % (artist, titel)
						else:
							name = titel
							
						list.append((name, titel, url, album, artist, ltype, token, imgurl))
				
				f1.close()
			
			return list
				
		except IOError, e:
			print "Fehler:\n",e
			print "eCode: ",e
			f1.close()
			return list

class SimpleEvent:
	def __init__(self):
		self._ev_callback = None
		self._ev_on = False
		
	def genEvent(self):
		#print "genEvent:"
		if self._ev_callback:
			self._ev_on = False
			self._ev_callback()
		else:
			self._ev_on = True
			
	def addCallback(self, cb):
		#print "addCallback:"
		self._ev_callback=cb
		if self._ev_on:
			self._ev_on = False
			cb()
	
	def reset(self):
		#print "reset"
		self._ev_callback = None
		self._ev_on = False

class SimpleScreenSaver(Screen):
	skin = """
		<screen position="0,0" size="1280,720" flags="wfNoBorder" zPosition="9" transparent="0">
		</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = SimpleScreenSaver.skin
			
		self["setupActions"] = ActionMap([ "SetupActions" ],
		{
			"cancel": self.cancel,
			"ok": self.cancel
		})

	def cancel(self):
		self.close()
		

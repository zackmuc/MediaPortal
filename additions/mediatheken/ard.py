#
# ARD-Mediathek von chroma_key
#

from Plugins.Extensions.MediaPortal.resources.imports import *

def ARDGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def ARDFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 

class ARDGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("ARD Mediathek")
		self['name'] = Label("Auswahl der Sendung")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.genreliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.genreliste = []
		for c in xrange(26):
			self.genreliste.append((chr(ord('A') + c), None))
		self.genreliste.insert(0, ('0-9', None))
		self.chooseMenuList.setList(map(ARDGenreListEntry, self.genreliste))
		self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['List'].getCurrent()[0][0]
		self.session.open(ARDSubGenreScreen, streamGenreLink)
		
	def keyLeft(self):
		self['List'].pageUp()
		
	def keyRight(self):
		self['List'].pageDown()
		
	def keyUp(self):
		self['List'].up()

	def keyDown(self):
		self['List'].down()

	def keyCancel(self):
		self.close()
		
class ARDSubGenreScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("ARD Mediathek")
		self['name'] = Label("Auswahl der Sendung")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		
		self.genreliste = []
		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		# chroma_key: Beispiel-URL fuer Smartphones... http://m.ardmediathek.de/Sendungen-A-Z?pageId=13932746 .... Auf der koennte man zwar wesentlich leichter aufbauen, da man hier auch die hoechste Qualitaet leichter
		# er-parsen kann, aber leider werden auch deutlich weniger Clips hierfuer gehostet ..... Beispiel... http://m.ardmediathek.de/coldmirror?docId=10017896&pageId=13932914
		# chroma_key: Der RSS-Feed ist super, hat scheinbar gleichviele Treffer wie die hier verwendeten Links, und hat dafuer sogar ausfuehrliche Inhaltsangaben (Metadaten, die bei dem, hier Verwendeten
		# fehlen) doch leider fehlt den RSS-Feeds ein Vorschau-Bildchen, sowie die Duration.....Beispiel...  url = "http://www.ardmediathek.de/export/rss/id=10017896" (id ist die docId)
		# chroma_key: URL fuer eine spaetere, einzubauende Suchfunktion (wenn man zb nach "coca cola" suchen wuerde)... http://www.ardmediathek.de/suche?s=coca+cola
		self.keyLocked = True
		url = "http://www.ardmediathek.de/ard/servlet/ajax-cache/3474820/view=list/initial=%s/index.html" % (self.streamGenreLink)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		sendungen = re.findall('<img src="(.*?)".*?<a href=".*?documentId=(.*?)".*?data-xtclib=".*?">\n\s+(.*?)\n\s+</a>.*?<span class="mt-count">(.*?)</span>.*?<span class="mt-channel">(.*?)</span>', data, re.S)
		if sendungen:
			for (image,id,title,ausgaben,sender) in sendungen:
				image = "http://www.ardmediathek.de%s" % image
				url = "http://www.ardmediathek.de/ard/servlet/ajax-cache/3516962/view=list/documentId=%s" %id
				zusatzinfo = "%s - %s" % (sender,ausgaben)
				# chroma_key: Ohne folgende 3 Zeilen, bekomme ich (zumindest auf meiner DMM8000) trotz zuvorigem "decodehtml" weiterhin zB. ein '&#034;' statt ein Gaensefuesschen gelistet.
				# Daher habe ich das "decodehtml" rausgeworfen, und die hartcodierte Umwandlung eingebaut, die nicht schadet. Kommt weiter unten nochmal... 
				# Abgefangen werden hier " und ' und & (letzteres kommt zB. bei 'Quarks & Co' vor... )
				title = title.replace("&#034;","'")
				title = title.replace("&#039;","'")
				title = title.replace("&amp;","&")
				self.genreliste.append((title,url,image,zusatzinfo))
		else:
			self.genreliste.append(('Keine Sendungen mit diesem Buchstaben vorhanden.', None, None, None))
		self.chooseMenuList.setList(map(ARDGenreListEntry, self.genreliste))
		self.keyLocked = False
		self.loadPic()

	def dataError(self, error):
		print error

	def loadPic(self):
		streamPic = self['List'].getCurrent()[0][2]
		if streamPic == None:
			return
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['List'].getCurrent()[0][3]
		self['handlung'].setText(streamHandlung)
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['List'].getCurrent()[0][1]
		if streamGenreLink == None:
			return
		self.session.open(ARDFilmeListeScreen, streamGenreLink)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.loadPic()

	def keyCancel(self):
		self.close()

class ARDFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/RTLnowGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/RTLnowGenreScreen.xml"
		print path
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

		self['title'] = Label("ARD Mediathek")
		self['name'] = Label("Folgen Auswahl")
		self['handlung'] = Label("")
		self['Pic'] = Pixmap()
		self.page = 1		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['List'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		url = "%s/goto=%s" % (self.streamGenreLink,self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		self.filmliste = []
		# chroma_key: Aufgehobener Code fuer Versuch mit RSS... folgen = re.findall('<item>.*?<title>(.*?)</title>.*?<description>(.*?)</description>.*?<link>(.*?)</link>', data, re.S)
		seiten = re.findall('<option selected="selected".*?goto=(.*?)/.*?<span>(.*?)</span>', data, re.S)
		# chroma_key: Wenn man auch bereits der ersten Seite ein optional angehaengtes "goto=1" unterschiebt, kann man auch bereits auf der ersten Seite er-parsen, wieviele Seiten es gibt.
		if seiten:
			for (a,b) in seiten:
				seite = "Seite:\t%s%s" % (a,b)
		else:
			seite = "Seite:\t1 von 1"
		folgen = re.findall('img src="(.*?)".*?<a href="(.*?)".*?xtclib=".*?">(.*?)</a>.*?aus: (.*?)</p>.*?"mt-airtime">(.*?)</span>.*?>(.*?)</span>', data, re.S)
		if folgen:
			for (image,url,title,sendung,airtime,sender) in folgen:
				image = "http://www.ardmediathek.de%s" % image
				title = title.replace("&#034;","'")
				title = title.replace("&#039;","'")
				title = title.replace("&amp;","&")
				sendung = sendung.replace("&#034;","'")
				sendung = sendung.replace("&#039;","'")
				sendung = sendung.replace("&amp;","&")				

				if airtime:
					if len(airtime) == 0:
						date = "Keine Angabe"
						dur = "Keine Angabe"
				if len(airtime) == 8:
					date = "%s" % (airtime)
					dur = "Keine Angabe"
				else:
					date = airtime[:8]
					dur = airtime[9:]
				handlung = "Sendung:\t%s\nClip vom:\t%s\nBroadcaster:\t%s\nDauer:\t>> %s <<\n\n%s" % (sendung,date,sender,dur,seite)
				self.filmliste.append((title,url,handlung,image))
		else:
			self.filmliste.append(('Keine Folgen gefunden.', None, None, None))
		self.chooseMenuList.setList(map(ARDFilmListEntry, self.filmliste))
		self.keyLocked = False
		self.loadPic()

	def loadPic(self):
		streamPic = self['List'].getCurrent()[0][3]
		if streamPic == None:
			return
		streamName = self['List'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['List'].getCurrent()[0][2]
		self['handlung'].setText(streamHandlung)
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['Pic'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['Pic'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['Pic'].instance.setPixmap(ptr.__deref__())
					self['Pic'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		self.streamName = self['List'].getCurrent()[0][0]
		id = self['List'].getCurrent()[0][1]
		if id == None:
			return
		url = "http://www.ardmediathek.de%s" % id
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_Link).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def get_Link(self, data):
		qualitycheck = re.findall('mediaCollection.addMediaStream\((.*?),\s+(.*?),\s+"(.*?)",\s+"(.*?)",.*?\)', data, re.S)
		if qualitycheck:
			qualinull = "n"
			qualieins = "e"
			qualizwei = "z"
			qualidrei = "d"
			for (a,b,c,d) in qualitycheck:
				if "30" in (a+b):
					# Nur '.mp4" ... vermeide '.m3u8' oder '.asx'
					if d[-4:] == ".mp4":
						if c:
							# Bei manchen rtmp-URLs fehlt ein '/' am Ende von c
							if c[-1:] != "/":
								c = c + "/"
						qualidrei = (c + d)
				elif "31" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualidrei = (c + d)
				elif "32" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualidrei = (c + d)
				elif "20" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualizwei = (c + d)
				elif "21" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualizwei = (c + d)
				elif "22" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualizwei = (c + d)
				elif "10" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualieins = (c + d)
				elif "11" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualieins = (c + d)
				elif "12" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualieins = (c + d)
				elif "00" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualinull = (c + d)
				elif "01" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualinull = (c + d)
				elif "02" in (a+b):
					if d[-4:] == ".mp4":
						if c:
							if c[-1:] != "/":
								c = c + "/"
						qualinull = (c + d)
			# Lade das schlechteste und steigere aufs beste, das gefunden wurde
			if len(qualinull) != 1:
				stream = qualinull
			if len(qualieins) != 1:
				stream = qualieins
			if len(qualizwei) != 1:
				stream = qualizwei
			if len(qualidrei) != 1:
				stream = qualidrei
			#
			# Broadcaster erkennen. Derzeit nur fuer SWR und SR.
			#
			ard = "mvideos.daserste.de"
			br = "cdn-storage.br.de"
			hr = "www.hr.gl-systemhaus.de"
			mdr = "x4100mp4"
			ndr = "media.ndr.de"
			rb = "httpmedia.radiobremen.de"
			rbb = "http-stream.rbb-online.de"
			sr = "sr.fcod"
			swr = "ios-ondemand.swr.de"
			ts = "media.tagesschau.de"
			wdr = "http-ras.wdr.de"
			#
			if swr in stream:
				stream = stream.replace("ios-ondemand","pd-ondemand")
				stream = stream.replace("swr.de/i","swr.de")
				stream = stream.replace("mp4/master.m3u8","mp4")
			if sr in stream:
				stream = stream.replace("MP4:","mp4:")
			# Playpath fuer neueren Dreamboxen reparieren
			noplaypath = "mp4:"
			if noplaypath in stream:
				stream = stream.replace("mp4:"," playpath=mp4:")
			# Gebe gefundenen Streamlink als kleine Textdatei aus, zum monitoren und fuer Fehlersuche
			fobj_out = open("/tmp/ard-stream.txt","w")
			fobj_out.write(stream)
			fobj_out.close()
			sref = eServiceReference(0x1001, 0, stream)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['List'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['List'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['List'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['List'].down()
		self.loadPic()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadPage()
			
	def keyPageUp(self):
		print "PageUp"
		if self.keyLocked:
			return
		self.page += 1 
		self.loadPage()
		
	def keyCancel(self):
		if os.path.isfile("/tmp/ard-stream.txt"):
			os.remove("/tmp/ard-stream.txt")
		self.close()

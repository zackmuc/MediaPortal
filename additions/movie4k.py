from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.decrypt import *

if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TMDb/plugin.pyo'):
    from Plugins.Extensions.TMDb.plugin import *
    TMDbPresent = True
else:
    TMDbPresent = False

def m4kGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def m4kLetterEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_CENTER, entry)
		]

def m4kFilmListEntry2(entry):
	png = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/%s.png" % entry[2]
	if fileExists(png):
		flag = LoadPixmap(png)	
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 5, 3, 20, 20, flag),
			(eListboxPythonMultiContent.TYPE_TEXT, 30, 0, 880, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 30, 0, 880, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]
		
def m4kSerienABCEntry(entry):
	flag_name = False

	if entry[2] == "http://img.movie4k.to/img/us_flag_small.png":
		flag_name = "2.png"
	elif entry[2] == "http://img.movie4k.to/img/us_ger_small.png":
		flag_name = "1.png"

	if flag_name:
		png = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/%s" % flag_name
		flag = LoadPixmap(png)
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 20, 5, 16, 11, flag),
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]

def m4kSerienABCStaffelnEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def m4kFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
def m4kWatchSeriesListEntry(entry):
	if int(entry[4]) != 0:
		new_eps = str(entry[4])
	else:
		new_eps = ""
		
	png = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/%s.png" % entry[2]
	if fileExists(png):
		flag = LoadPixmap(png)	
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 15, 3, 20, 20, flag),
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 750, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
			(eListboxPythonMultiContent.TYPE_TEXT, 800, 0, 50, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, new_eps)
			]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 750, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
			(eListboxPythonMultiContent.TYPE_TEXT, 800, 0, 50, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, new_eps)
			]

class m4kGenreScreen(Screen):
	
	def __init__(self, session, mode):
		self.session = session
		self.showM4kPorn = mode
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("movie4k.to")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.searchStr = ''
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		if self.showM4kPorn == "porn":
			self.genreliste.append(("Letzte Updates (XXX)", "http://www.movie4k.to/xxx-updates.html"))
			self.genreliste.append(('Pornos', 'http://www.movie4k.to/genres-xxx.html'))
		else:
			self.genreliste.append(("Watchlist", "Watchlist"))
			self.genreliste.append(("Kinofilme", "http://www.movie4k.to/index.php?lang=de"))
			self.genreliste.append(("Videofilme", "http://www.movie4k.to/index.php?lang=de"))
			self.genreliste.append(("Neue Updates (Filme)", "http://www.movie4k.to/movies-updates-"))
			self.genreliste.append(("Empfohlene Serien", "http://www.movie4k.to/tvshows_featured.php"))
			self.genreliste.append(("Letzte Updates (Serien)", "http://www.movie4k.to/tvshows_featured.php"))
			self.genreliste.append(("Alle Filme A-Z", "FilmeAZ"))
			self.genreliste.append(("Alle Serien A-Z", "SerienAZ"))
			self.genreliste.append(("Suche", "http://www.movie4k.to/movies.php?list=search"))
			self.genreliste.append(("Abenteuer", "http://movie4k.to/movies-genre-4-"))
			self.genreliste.append(("Action", "http://movie4k.to/movies-genre-1-"))
			self.genreliste.append(('Biografie', 'http://movie4k.to/movies-genre-6-'))
			self.genreliste.append(('Bollywood', 'http://movie4k.to/movies-genre-27-'))
			self.genreliste.append(('Dokumentation', 'http://movie4k.to/movies-genre-8-'))
			self.genreliste.append(('Drama', 'http://movie4k.to/movies-genre-2-'))
			self.genreliste.append(('Erwachsene', 'http://movie4k.to/movies-genre-58-'))
			self.genreliste.append(('Familie', 'http://movie4k.to/movies-genre-9-'))
			self.genreliste.append(('Fantasy', 'http://movie4k.to/movies-genre-10-'))
			self.genreliste.append(('Film Noir', 'http://movie4k.to/movies-genre-60-'))
			self.genreliste.append(('Game Show', 'http://movie4k.to/movies-genre-61-'))
			self.genreliste.append(('History', 'http://movie4k.to/movies-genre-13-'))
			self.genreliste.append(('Horror', 'http://movie4k.to/movies-genre-14-'))
			self.genreliste.append(('Comedy', 'http://movie4k.to/movies-genre-3-'))
			self.genreliste.append(('Kriegsfilme', 'http://movie4k.to/movies-genre-24-'))
			self.genreliste.append(('Krimi', 'http://movie4k.to/movies-genre-7-'))
			self.genreliste.append(('Kurzfilme', 'http://movie4k.to/movies-genre-55-'))
			self.genreliste.append(('Musicals', 'http://movie4k.to/movies-genre-56-'))
			self.genreliste.append(('Musik', 'http://movie4k.to/movies-genre-15-'))
			self.genreliste.append(('Mystery', 'http://movie4k.to/movies-genre-17-'))
			self.genreliste.append(('News', 'http://movie4k.to/movies-genre-62-'))
			self.genreliste.append(('Reality TV', 'http://movie4k.to/movies-genre-59-'))
			self.genreliste.append(('Romanzen', 'http://movie4k.to/movies-genre-20-'))
			self.genreliste.append(('Sci-Fy', 'http://movie4k.to/movies-genre-21-'))
			self.genreliste.append(('Andere', 'http://movie4k.to/movies-'))
			self.genreliste.append(('Sport', 'http://movie4k.to/movies-'))
			self.genreliste.append(('Talk Shows', 'http://movie4k.to/movies-genre-63-'))
			self.genreliste.append(('Thriller', 'http://movie4k.to/movies-genre-23-'))
			self.genreliste.append(('Animation', 'http://movie4k.to/movies-genre-5-'))
			self.genreliste.append(('Western', 'http://movie4k.to/movies-genre-25-'))
		self.chooseMenuList.setList(map(m4kGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		
		if streamGenreName == "Watchlist":
			self.session.open(m4kWatchlist)
		elif streamGenreName == "Kinofilme":
			self.session.open(m4kKinoFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Videofilme":
			self.session.open(m4kVideoFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Letzte Updates (Filme)":
			self.session.open(m4kupdateFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Empfohlene Serien":
			self.session.open(m4kTopSerienFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Letzte Updates (Serien)":
			self.session.open(m4kSerienUpdateFilmeListeScreen, streamGenreLink)
		elif streamGenreName == "Alle Serien A-Z":
			self.session.open(m4kSerienABCAuswahl, streamGenreLink)
		elif streamGenreName == "Alle Filme A-Z":
			self.session.open(m4kSerienABCAuswahl, streamGenreLink)
		elif streamGenreLink == 'http://www.movie4k.to/movies.php?list=search':
			self.streamGenreLink = streamGenreLink
			self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Suchbegriff eingeben")), text = " ")
		elif streamGenreName == "Letzte Updates (XXX)":
			self.session.open(m4kXXXUpdateFilmeListeScreen, streamGenreLink, '')
		elif streamGenreName == "Pornos":
			self.session.open(m4kKinoAlleFilmeListeScreen, streamGenreLink)
		else:
			self.session.open(m4kKinoAlleFilmeListeScreen, streamGenreLink)
			
	def searchCallback(self, callbackStr):
		if callbackStr is not None:
			self.searchStr = callbackStr
			url = self.streamGenreLink
			self.searchData = self.searchStr
			self.session.open(m4kSucheAlleFilmeListeScreen, url, self.searchData)
			
	def keyCancel(self):
		self.close()
		
class m4kWatchlist(Screen):
	
	def __init__(self, session):
		self.session = session
		self.plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal"
		
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/kxWatchlist.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/kxWatchlist.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red" : self.keyDel,
			"info": self.update
		}, -1)
		
		self['title'] = Label("Watchlist")
		self['leftContentTitle'] = Label("Movie4k Watchlist")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		self['name'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPlaylist)

	def loadPlaylist(self):
		self.streamList = []
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			readStations = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist","r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink, stationLang, stationTotaleps) = data[0]
					self.streamList.append((stationName, stationLink, stationLang, stationTotaleps, "0"))
			print "Load Watchlist.."
			self.streamList.sort()
			self.streamMenuList.setList(map(m4kWatchSeriesListEntry, self.streamList))
			readStations.close()
			self.keyLocked = False
			
	def update(self):
		self.count = len(self.streamList)
		self.counting = 0
		
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp"):
			self.write_tmp = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp" , "a")
			self.write_tmp.truncate(0)
		else:
			self.write_tmp = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp" , "a")
					
		if len(self.streamList) != 0:
			self.keyLocked = True
			self.streamList2 = []
			#print sname, surl, slang, stotaleps
			ds = defer.DeferredSemaphore(tokens=1)
			downloads = [ds.run(self.download,item[1]).addCallback(self.check_data, item[0], item[1], item[2], item[3]).addErrback(self.dataError) for item in self.streamList]
			finished = defer.DeferredList(downloads).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def download(self, item):
		return getPage(item)
		
	def check_data(self, data, sname, surl, slang, stotaleps):
		#print sname, surl, slang, stotaleps
		count_all_eps = 0
		self.counting += 1
		self['title'].setText("Update %s/%s" % (self.counting,self.count))

		staffeln = re.findall('<FORM name="episodeform(.*?)">(.*?)</FORM>', data, re.S)
		for (staffel, ep_data) in staffeln:
			#(staffel, ep_data) = each
			episodes = re.findall('<OPTION value=".*?".*?>Episode.(.*?)</OPTION>', ep_data, re.S)
			count_all_eps += int(len(episodes))
			last_new_ep = staffel, episodes[-1]
			
			
		new_eps =  int(count_all_eps) - int(stotaleps)	
			
		self.write_tmp.write('"%s" "%s" "%s" "%s"\n' % (sname, surl, slang, count_all_eps))
		
		self.streamList2.append((sname, surl, slang, str(stotaleps), str(new_eps)))
		self.streamList2.sort()
		self.streamMenuList.setList(map(m4kWatchSeriesListEntry, self.streamList2))

		print self.counting, self.count
		if self.counting == self.count:
			print "update done."
			self['title'].setText("Update done.")
			self.write_tmp.close()
			shutil.move(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp", config.mediaportal.watchlistpath.value+"mp_m4k_watchlist")
			self.keyLocked = False
			
		if last_new_ep:
			(staffel, episode) = last_new_ep
			if int(staffel) < 10:
				staffel3 = "S0"+str(staffel)
			else:
				staffel3 = "S"+str(staffel)

			if int(episode) < 10:
				episode3 = "E0"+str(episode)
			else:
				episode3 = "E"+str(episode)
								
			SeEp = "%s%s" % (staffel3, episode3)
	
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		url = self['streamlist'].getCurrent()[0][1]
		print stream_name, url
		self.session.open(m4kEpisodenListeScreen, url, stream_name)
			
	def keyDel(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		
		selectedName = self['streamlist'].getCurrent()[0][0]

		writeTmp = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp","w")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			readStations = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist","r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink, stationLang, stationTotaleps) = data[0]
					if stationName != selectedName:
						writeTmp.write('"%s" "%s" "%s" "%s"\n' % (stationName, stationLink, stationLang, stationTotaleps))
			readStations.close()
			writeTmp.close()
			shutil.move(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist.tmp", config.mediaportal.watchlistpath.value+"mp_m4k_watchlist")
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()
		
class m4kSucheAlleFilmeListeScreen(Screen):
	
	def __init__(self, session, searchUrl, searchData):
		self.session = session
		self.searchUrl = searchUrl
		self.searchData = searchData
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultPageListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultPageListeScreen.xml"
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
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber,
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label("1")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = self.searchUrl
		sData = self.searchData
		getPage(url,method='POST',postdata=urllib.urlencode({'search':sData}),headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		kino = re.findall('<TR id="coverPreview(.*?)">.*?<a href="(.*?)">(.*?)     ', data, re.S)
		if kino:
			self.filmliste = []
			for image, teil_url, title in kino:
				url = '%s%s' % ('http://www.movie4k.to/', teil_url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))

	def loadPic(self):
		url = self['filmList'].getCurrent()[0][1]
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPicData).addErrback(self.dataError)
		
	def loadPicData(self, data):
		filmdaten = re.findall('<div style="float:left">.*?<img src="(.*?)".*?<div class="moviedescription">(.*?)</div>', data, re.S)
		if filmdaten:
			streamPic, handlung = filmdaten[0]
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			self['handlung'].setText(decodeHtml(handlung))
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()

		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()

		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()

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
		self.close()

class m4kKinoAlleFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultPageListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultPageListeScreen.xml"
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
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber,
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.XXX = False
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label("1")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = ''
		if self.streamGenreLink == 'http://www.movie4k.to/genres-xxx.html':
			url = str(self.streamGenreLink)
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadXXXPageData).addErrback(self.dataError)
		else:
			url = '%s%s%s' % (self.streamGenreLink, self.page, '.html')
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadXXXPageData(self, data):
		self.XXX = True
		xxxGenre = re.findall('<TD id="tdmovies" width="155">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		if xxxGenre:
			self.filmliste = []
			for teil_url, title in xxxGenre:
				url = '%s%s' % ('http://www.movie4k.to/', teil_url)
				title.replace("\t","")
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))

	def loadPageData(self, data):
		print "daten bekommen"
		kino = re.findall('<TR id="coverPreview(.*?)">.*?<a href="(.*?)">(.*?)     ', data, re.S)
		if kino:
			self.filmliste = []
			for image, teil_url, title in kino:
				url = '%s%s' % ('http://www.movie4k.to/', teil_url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))
			if self.XXX == False:
				self.loadPic()

	def loadPic(self):
		url = self['filmList'].getCurrent()[0][1]
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPicData).addErrback(self.dataError)
		
	def loadPicData(self, data):
		filmdaten = re.findall('<div style="float:left">.*?<img src="(.*?)".*?<div class="moviedescription">(.*?)</div>', data, re.S)
		if filmdaten:
			streamPic, handlung = filmdaten[0]
			downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
			self['handlung'].setText(decodeHtml(handlung))
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()

	def keyOK(self):
		if self.keyLocked:
			return
		if self.XXX == False:
			streamName = self['filmList'].getCurrent()[0][0]
			streamLink = self['filmList'].getCurrent()[0][1]
			self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")
		else:
			xxxGenreName = self['filmList'].getCurrent()[0][0]
			xxxGenreLink = self['filmList'].getCurrent()[0][1]
			self.session.open(m4kXXXUpdateFilmeListeScreen, xxxGenreLink, 'X')

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		if self.XXX == False:
			self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		if self.XXX == False:
			self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		if self.XXX == False:
			self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		if self.XXX == False:
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
		self.close()

class m4kKinoFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print self.streamGenreLink
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		kino = re.findall('<div style="float:left"><a href="(.*?)" ><img src="(.*?)" border=0 style="width:105px;max-width:105px;max-height:160px;min-height:140px;" alt=".*?kostenlos" title="(.*?).kostenlos"></a>', data, re.S)
		if kino:
			for url,image,title in kino:
				url = "%s%s" % ("http://www.movie4k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kVideoFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		video = re.findall('<div style="float: left;"><a href="(.*?)" ><img src="(.*?)" alt=".*?" title="(.*?)" border="0" style="width:105px;max-width:105px;max-height:160px;min-height:140px;"></a>', data, re.S)
		if video:
			for url,image,title in video:
				url = "%s%s" % ("http://www.movie4k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kupdateFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		updates = re.findall('<td valign="top" height="100%"><a href="(.*?)" ><font color="#000000" size="-1"><strong>(.*?)</strong></font></a></td>', data, re.S)
		if updates:
			for url,title in updates:
				url = "%s%s" % ("http://www.movie4k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kTopSerienFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kTopSerienFilmeListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kTopSerienFilmeListeScreen.xml"
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
			"green" : self.keyAdd
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Serien Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keckse = {}
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.m4kcookie)

	def m4kcookie(self):
		url = "http://www.movie4k.to/index.php?lang=de"
		getPage(url, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getm4kcookie).addErrback(self.dataError)
		
	def getm4kcookie(self, data):
		self.loadPage()

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		print "daten bekommen"
		serien = re.findall('<div style="float:left"><a href="(.*?)"><img src="(.*?)" border=0 width=105 height=150 alt=".*?" title="(.*?)"></a>.*?<img src="http://img.movie4k.to/img/(.*?).png"', data, re.S)
		if serien:
			for url,image,title,lang in serien:
				url = "%s%s" % ("http://www.movie4k.to/", url)
				print title
				self.filmliste.append((decodeHtml(title), url, image, lang))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/Icon.jpg").addCallback(self.ShowCover)
		
	def showHandlung(self, data):
		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamName, streamLink
		self.session.open(m4kEpisodenListeScreen, streamLink, streamName)

	def keyAdd(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		self.mTitle = self['filmList'].getCurrent()[0][0]
		self.mUrl = self['filmList'].getCurrent()[0][1]
		self.mLang = self['filmList'].getCurrent()[0][3]
		
		if not fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			os.system("touch "+config.mediaportal.watchlistpath.value+"mp_m4k_watchlist")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			writePlaylist = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist","a")
			if self.mLang == "us_ger_small":
				Lang = "de"
			elif self.mLang == "us_flag_small":
				Lang = "en"
			else:
				Lang = ""
				
			print self.mUrl, self.mTitle, Lang
			writePlaylist.write('"%s" "%s" "%s" "0"\n' % (self.mTitle, self.mUrl, Lang))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kSerienUpdateFilmeListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kTopSerienFilmeListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kTopSerienFilmeListeScreen.xml"
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
			"green" : self.keyAdd
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Serien Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.m4kcookie)

	def m4kcookie(self):
		url = "http://www.movie4k.to/index.php?lang=de"
		getPage(url, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getm4kcookie).addErrback(self.dataError)
		
	def getm4kcookie(self, data):
		self.loadPage()

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen2"
		serien = re.findall('<td id="tdmovies"> <img style="vertical-align:top;".*?<a href="(.*?)">.*?<font color="#000000">(.*?)</font></a>', data, re.S)
		if serien:
			for url,title in serien:
				url = "http://www.movie4k.to/"+url
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamName, streamLink
		
		if re.match('.*?,.*?,.*?', streamName):
			cname = re.findall('(.*?),.*?,.*?', streamName, re.S)
			if cname:
				streamName = cname[0]

		self.session.open(m4kEpisodenListeScreen, streamLink, streamName)

	def keyAdd(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		mTitle = self['filmList'].getCurrent()[0][0]
		mUrl = self['filmList'].getCurrent()[0][1]
		
		if re.match('.*?,.*?,.*?', mTitle):
			cname = re.findall('(.*?),.*?,.*?', mTitle, re.S)
			if cname:
				mTitle = cname[0]
				
		if not fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			os.system("touch "+config.mediaportal.watchlistpath.value+"mp_m4k_watchlist")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
			writePlaylist = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist","a")
			print mUrl, mTitle
			writePlaylist.write('"%s" "%s" "%s" "0"\n' % (mTitle, mUrl, "de"))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
			
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kStreamListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink, streamName, which):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		self.which = which
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Stream Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "link:", self.streamGenreLink
		req = urllib2.Request(self.streamGenreLink)
		try:
			res = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
			return
		else:
			url = res.geturl()
			print "link resolved:", url
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print "error:", error
		
	def loadPageData(self, data):
		print "daten bekommen"
		if self.which == "movie":
			hoster = re.findall('<tr id=.*?tablemoviesindex2.*?><td height=.*?20.*?width.*?"150.*?><a href.*?"(.*?.html).*?>(.*?).<.*?src.*?"http://img.movie4k.to/img/.*?\..*?> \&nbsp;(.*?)</a>.*?alt.*?"(Movie quality.*?)" title=', data, re.S)
			if hoster:
				for url,datum,hostername,quali in hoster:
					url = "%s%s" % ("http://www.movie4k.to/", url)
					print hostername, url
					if re.match('.*?(putme|limevideo|stream2k|played|putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Zooupload|Wupfile|BitShare|Userporn)', hostername, re.S|re.I):
						self.filmliste.append((url, datum, hostername, quali.replace('Movie quality ','').replace('\\','')))
						
				if len(self.filmliste) == 0:
					self.filmliste.append(("nix", "No supported streams found."))
					self.chooseMenuList.setList(map(self.m4kStream2ListEntry, self.filmliste))
					self.loadPic()
				else:
					self.chooseMenuList.setList(map(self.m4kStreamListEntry, self.filmliste))
					self.keyLocked = False
					self.loadPic()
		else:
			hoster = re.findall('"tablemoviesindex2.*?<a href.*?"(.*?.html).*?style.*?src.*?"http://img.movie4k.to/img/.*?.[gif|png].*?> \&nbsp;(.*?)</a></td></tr>', data, re.S)
			if hoster:
				for url,hostername in hoster:
					url = "%s%s" % ("http://www.movie4k.to/", url)		
					print hostername, url
					if re.match('.*?(putme|limevideo|stream2k|played|putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Zooupload|Wupfile|BitShare|Userporn)', hostername, re.S|re.I):
						self.filmliste.append((url, hostername))
						
				if len(self.filmliste) == 0:
					self.filmliste.append(("nix", "No supported streams found."))
					self.chooseMenuList.setList(map(self.m4kStream2ListEntry, self.filmliste))
					self.loadPic()
				else:
					self.chooseMenuList.setList(map(self.m4kStream2ListEntry, self.filmliste))
					self.keyLocked = False
					self.loadPic()
		
	def m4kStreamListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
			(eListboxPythonMultiContent.TYPE_TEXT, 250, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
			(eListboxPythonMultiContent.TYPE_TEXT, 450, 0, 430, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
			]
			
	def m4kStream2ListEntry(self, entry):
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1])
			]

	def loadPic(self):
		req = urllib2.Request(self.streamGenreLink)
		try:
			res = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
			return
		else:
			url = res.geturl()
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamLink = self['filmList'].getCurrent()[0][0]
		print self.streamName, streamLink
		try:
			req = urllib2.Request(streamLink)
			res = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.code
			return
		else:
			url = res.geturl()
			print "link resolved:", url
			getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_streamlink, url).addErrback(self.dataError)
		
	def get_streamlink(self, data, streamLink):
		if re.match('.*?(http://img.movie4k.to/img/parts/teil1_aktiv.png|http://img.movie4k.to/img/parts/teil1_inaktiv.png|http://img.movie4k.to/img/parts/part1_active.png|http://img.movie4k.to/img/parts/part1_inactive.png)', data, re.S):
			self.session.open(m4kPartListeScreen, streamLink, self.streamName)
		else:
			link_found = False
		
			link = re.findall('<a target="_blank" href="(.*?)"', data, re.S)
			if link:
				link_found = True
				print link
				get_stream_link(self.session).check_link(link[0], self.got_link, False)
				
			link = re.findall('<div id="emptydiv"><iframe.*?src=["|\'](.*?)["|\']', data, re.S)
			if link:
				link_found = True
				print link[0]
				get_stream_link(self.session).check_link(link[0], self.got_link, False)
				
			link = re.findall('<div id="emptydiv"><script type="text/javascript" src=["|\'](.*?)["|\']>', data, re.S)
			if link:
				link_found = True
				print link[0].replace('?embed','')
				get_stream_link(self.session).check_link(link[0].replace('?embed',''), self.got_link, False)

			link = re.findall('<object\sid="vbbplayer".*?src=["|\'](.*?)["|\']', data, re.S)
			if link:
				link_found = True
				print link[0]
				get_stream_link(self.session).check_link(link[0], self.got_link, False)
				
			link = re.findall('<iframe width=".*?" height=".*?" frameborder=".*?" src="(.*?)" scrolling="no"></iframe>', data, re.S)
			if link:
				link_found = True
				print link[0]
				get_stream_link(self.session).check_link(link[0], self.got_link, False)
				
			link = re.findall('<iframe src="(.*?)" width=".*?" height=".*?" frameborder=".*?" scrolling="no"></iframe>', data, re.S)
			if link:
				link_found = True
				print link[0]
				get_stream_link(self.session).check_link(link[0], self.got_link, False)
				
			if not link_found:
				message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=5)
			
	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			if not fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watched"):
				os.system("touch "+config.mediaportal.watchlistpath.value+"mp_m4k_watched")
				
			self.update_liste = []
			leer = os.path.getsize(config.mediaportal.watchlistpath.value+"mp_m4k_watched")
			if not leer == 0:
				self.updates_read = open(config.mediaportal.watchlistpath.value+"mp_m4k_watched" , "r")
				for lines in sorted(self.updates_read.readlines()):
					line = re.findall('"(.*?)"', lines)
					if line:
						print line[0]
						self.update_liste.append("%s" % (line[0]))
				self.updates_read.close()
				
				updates_read2 = open(config.mediaportal.watchlistpath.value+"mp_m4k_watched" , "a")
				check = ("%s" % self.streamName)
				if not check in self.update_liste:
					print "update add: %s" % (self.streamName)
					updates_read2.write('"%s"\n' % (self.streamName))
					updates_read2.close()
				else:
					print "dupe %s" % (self.streamName)
			else:
				updates_read3 = open(config.mediaportal.watchlistpath.value+"mp_m4k_watched" , "a")
				print "update add: %s" % (self.streamName)
				updates_read3.write('"%s"\n' % (self.streamName))
				updates_read3.close()
				
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.streamName)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()

class m4kPartListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink, streamName):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Part Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(41)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		id = re.findall('[film-|movie-](\d+)\.html', self.streamGenreLink, re.S)
		if id:
			print id
			url1 = "%s%s%s" % ("http://www.movie4k.to/movie.php?id=", id[0], "&part=1")
			url2 = "%s%s%s" % ("http://www.movie4k.to/movie.php?id=", id[0], "&part=2")
			self.filmliste.append(("1", url1))
			self.filmliste.append(("2", url2))
			self.chooseMenuList.setList(map(self.m4kPartsListEntry, self.filmliste))
			self.keyLocked = False
		else:
			print "id fehler.."

	def m4kPartsListEntry(self, entry):
		part = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/teil%s.png" % entry[0]
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 396, 3, 108, 35, LoadPixmap(part))
			]

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamPart = self['filmList'].getCurrent()[0][0]
		streamLinkPart = self['filmList'].getCurrent()[0][1]
		self.sname = "%s - Teil %s" % (self.streamName, streamPart)
		print self.sname, streamLinkPart
		getPage(streamLinkPart, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_streamlink).addErrback(self.dataError)

	def get_streamlink(self, data):
		link_found = False

		link = re.findall('<a target="_blank" href="(.*?)"', data, re.S)
		if link:
			link_found = True
			print link
			get_stream_link(self.session).check_link(link[0], self.got_link, False)
			
		link = re.findall('<div id="emptydiv"><iframe.*?src=["|\'](.*?)["|\']', data, re.S)
		if link:
			link_found = True
			print link[0]
			get_stream_link(self.session).check_link(link[0], self.got_link, False)
			
		link = re.findall('<div id="emptydiv"><script type="text/javascript" src=["|\'](.*?)["|\']>', data, re.S)
		if link:
			link_found = True
			print link[0].replace('?embed','')
			get_stream_link(self.session).check_link(link[0].replace('?embed',''), self.got_link, False)

		link = re.findall('<object\sid="vbbplayer".*?src=["|\'](.*?)["|\']', data, re.S)
		if link:
			link_found = True
			print link[0].replace('?embed','')
			get_stream_link(self.session).check_link(link[0].replace('?embed',''), self.got_link, False)
			
		if not link_found:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=5)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.sname)
			self.session.open(MoviePlayer, sref)

	def dataError(self, error):
		print error
		
	def keyCancel(self):
		self.close()

class m4kEpisodenListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink, streamName):
		self.session = session
		self.streamGenreLink = streamGenreLink
		self.streamName = streamName
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Episoden Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		self.watched_liste = []
		self.mark_last_watched = []
		if not fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watched"):
			os.system("touch "+config.mediaportal.watchlistpath.value+"mp_m4k_watched")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watched"):
			leer = os.path.getsize(config.mediaportal.watchlistpath.value+"mp_m4k_watched")
			if not leer == 0:
				self.updates_read = open(config.mediaportal.watchlistpath.value+"mp_m4k_watched" , "r")
				for lines in sorted(self.updates_read.readlines()):
					line = re.findall('"(.*?)"', lines)
					if line:
						self.watched_liste.append("%s" % (line[0]))
				self.updates_read.close()
				
		print "daten bekommen"
		folgen = re.findall('<FORM name="episodeform(.*?)">(.*?)</FORM>', data, re.S)
		if folgen:
			for staffel,ep_data in folgen:
				episodes = re.findall('<OPTION value="(.*?)".*?>Episode.(.*?)</OPTION>', ep_data, re.S)
				if episodes:
					for url_to_streams, episode in episodes:
						url_to_streams = "%s%s" % ("http://www.movie4k.to/", url_to_streams)
						if int(staffel) < 10:
							staffel3 = "S0"+str(staffel)
						else:
							staffel3 = "S"+str(staffel)
							
						if int(episode) < 10:
							episode3 = "E0"+str(episode)
						else:
							episode3 = "E"+str(episode)
						staffel_episode = "%s - %s%s" % (self.streamName,staffel3,episode3)
						if staffel_episode in self.watched_liste:
							self.filmliste.append((staffel_episode,url_to_streams,True))
							self.mark_last_watched.append(staffel_episode)
						else:
							self.filmliste.append((staffel_episode,url_to_streams,False))
			self.chooseMenuList.setList(map(self.m4kStreamListEntry, self.filmliste))
			
			# jump to last watched episode
			if len(self.mark_last_watched) != 0:
				counting_watched = 0
				for (name,url,watched) in self.filmliste:
					counting_watched += 1
					if self.mark_last_watched[-1] == name:
						counting_watched = int(counting_watched) - 1
						print "last watched episode: %s" % counting_watched
						break
				self["filmList"].moveToIndex(int(counting_watched))
			else:
				if len(self.filmliste) != 0:
					jump_last = len(self.filmliste) -1
				else:
					jump_last = 0
				print "last episode: %s" % jump_last
				self["filmList"].moveToIndex(int(jump_last))

			self.keyLocked = False
			self.loadPic()
			
	def m4kStreamListEntry(self, entry):
		if entry[2]:
			png = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/watched.png"
			watched = LoadPixmap(png)
			return [entry,
				(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 39, 3, 100, 22, watched),
				(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
				]
		else:
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
				]

	def loadPic(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamEpisode = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamEpisode, streamLink
		self.session.open(m4kStreamListeScreen, streamLink, streamEpisode, "tv")

	def keyCancel(self):
		self.close()

class m4kXXXUpdateFilmeListeScreen(Screen):
	
	def __init__(self, session, streamXXXLink, genre):
		self.session = session
		self.streamXXXLink = streamXXXLink
		self.genre = False
		if genre == 'X':
			self.genre = True
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"green" : self.keyPageNumber,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("XXX Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label("1")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print 'load xxx updates...'
		print 'Link...', self.streamXXXLink
		if self.genre == True:
			shortUrl = re.findall('http://www.movie4k.to/xxx-genre-[0-9]*[0-9]*.*?',self.streamXXXLink)
			shortUrlC = str(shortUrl[0])
			url = shortUrlC + '-' + str(self.page) + '.html'
			print url
		else:
			url = str(self.streamXXXLink)
		getPage(url, agent=std_headers, headers={'Cookie': 'xxx2=ok', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def dataError(self, error):
		print error
		
	def loadPageData(self, data):
		print "daten bekommen"
		self.filmliste = []
		if self.genre == False:
			serien = re.findall('<TD id="tdmovies" width="380">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		else:
			serien = re.findall('<TD width="550" id="tdmovies">.*?<a href="(.*?)">(.*?)</a>', data, re.S)
		if serien:
			for url,title in serien:
				url = "%s%s" % ("http://www.movie4k.to/", url)
				title.replace("\t","")
				self.filmliste.append((decodeHtml(title), url))
			self.chooseMenuList.setList(map(m4kFilmListEntry, self.filmliste))
			self.keyLocked = False
			self['page'].setText(str(self.page))
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamUrl = self['filmList'].getCurrent()[0][1]
		getPage(streamUrl, agent=std_headers, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showHandlung).addErrback(self.dataError)
		
	def showHandlung(self, data):
		image = re.findall('<meta property="og:image" content="(.*?)"', data, re.S)
		if image:
			downloadPage(image[0], "/tmp/Icon.jpg").addCallback(self.ShowCover)

		handlung = re.findall('<div class="moviedescription">(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			self['handlung'].setText(decodeHtml(handlung))
		else:
			self['handlung'].setText("Keine infos gefunden.")
			
	def ShowCover(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			self.page = int(answer)
			self.loadPage()
				
	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamName, "movie")
		
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
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
			
	def keyCancel(self):
		self.close()

class m4kSerienABCAuswahl(Screen):
	
	def __init__(self, session, m4kGotLink):
		self.m4kGotLink = m4kGotLink
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kAuswahl.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kAuswahl.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Movie4k.to")
		if self.m4kGotLink == 'FilmeAZ':
			self['leftContentTitle'] = Label("Filme A-Z")
		else:
			self['leftContentTitle'] = Label("Serien A-Z") 
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","#"]
		for letter in abc:
			self.streamList.append((letter))
		self.streamMenuList.setList(map(m4kLetterEntry, self.streamList))
		self.keyLocked = False
					
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0]
		if auswahl == '#':
			auswahl = '1'
		print auswahl
		if self.m4kGotLink == 'SerienAZ':
			streamGenreLink = "http://www.movie4k.to/tvshows-all-%s.html" % auswahl
			self.session.open(m4kSerienABCListe, streamGenreLink)
		elif self.m4kGotLink == 'FilmeAZ':
			streamGenreLink = 'http://www.movie4k.to/movies-all-%s-' % auswahl
			self.session.open(m4kKinoAlleFilmeListeScreen, streamGenreLink)
		
	def keyCancel(self):
		self.close()

class m4kSerienABCListe(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kSerienABCListe.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kSerienABCListe.xml"
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
			"green" : self.keyAdd
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Serie Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label(" ")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		print self.streamGenreLink
		serien = re.findall('<TD id="tdmovies" width="538"><a href="(.*?)">(.*?)<.*?src="(.*?)"', data, re.S)
		if serien:
			self.streamList = []
			for urlPart, title, landImage in serien:
				url = '%s%s' % ('http://www.movie4k.to/', urlPart)
				self.filmliste.append((decodeHtml(title), url, landImage))
			self.chooseMenuList.setList(map(m4kSerienABCEntry, self.filmliste))
			self.keyLocked = False
			#self.loadPic()
		else:
			print "parsen - Keine Daten gefunden"

	def dataError(self, error):
		print error

	def loadPic(self):
		landImageUrl = self['filmList'].getCurrent()[0][2]
		downloadPage(landImageUrl, "/tmp/Icon.jpg").addCallback(self.ShowCoverFlag)

	def ShowCoverFlag(self, picData):
		if fileExists("/tmp/Icon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/Icon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kSerienABCListeStaffeln, streamLink)

	def keyAdd(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		self.mTitle = self['filmList'].getCurrent()[0][0]
		self.mUrl = self['filmList'].getCurrent()[0][1]
		self.mLang = self['filmList'].getCurrent()[0][2]
		self.flag_stored = self.mLang.replace('http://img.movie4k.to/img/','').replace('.png','')
		print self.flag_stored

		getPage(self.mUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_final).addErrback(self.dataError)
		
	def get_final(self, data):
		print "final"
		season_link = False
		series = re.findall('<TD id="tdmovies" width="538"><a href="(.*?)">(.*?)\t.*?<TD id="tdmovies"><img border=0 src="http://img.movie4k.to/img/(.*?)\..*?"', data, re.S)
		if series:
			for each in series:
				(link, seriesname, flag) = each
				if flag == self.flag_stored:
					season_link = "http://www.movie4k.to/%s" % link
		else:
			message = self.session.open(MessageBox, _("No Link FOUND."), MessageBox.TYPE_INFO, timeout=3)
			
		if season_link:
			print season_link
			getPage(season_link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_final2).addErrback(self.dataError)
		else:
			message = self.session.open(MessageBox, _("No Link FOUND."), MessageBox.TYPE_INFO, timeout=3)

			
	def get_final2(self, data):
		print "final2"
		series = re.findall('<TD id="tdmovies" width="538"><a href="(.*?)">(.*?)\t.*?<TD id="tdmovies"><img border=0 src="http://img.movie4k.to/img/(.*?)\..*?"', data, re.S)
		if series:
			for each in series:
				(link, seriesname, flag) = each
				if flag == self.flag_stored:
					season_link = "http://www.movie4k.to/%s" % link
		else:
			message = self.session.open(MessageBox, _("No Link FOUND."), MessageBox.TYPE_INFO, timeout=3)

		if season_link:
			if not fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
				os.system("touch "+config.mediaportal.watchlistpath.value+"mp_m4k_watchlist")
			if fileExists(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist"):
				writePlaylist = open(config.mediaportal.watchlistpath.value+"mp_m4k_watchlist","a")
				if self.mLang == "http://img.movie4k.to/img/us_ger_small.png":
					Lang = "de"
				elif self.mLang == "http://img.movie4k.to/img/us_flag_small.png":
					Lang = "en"
				else:
					Lang = ""
					
				print season_link, seriesname.replace('    ',''), Lang
				writePlaylist.write('"%s" "%s" "%s" "0"\n' % (seriesname.replace('    ',''), season_link, Lang))
				writePlaylist.close()
				message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
		else:
			message = self.session.open(MessageBox, _("No Link FOUND."), MessageBox.TYPE_INFO, timeout=3)
			
	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		#self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		#self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		#self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		#self.loadPic()

	def keyCancel(self):
		self.close()

class m4kSerienABCListeStaffeln(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Staffel Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label(" ")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		print self.streamGenreLink
		staffeln = re.findall('<TD id="tdmovies" width="538"><a href="(.*?)".*?Season:(.*?)<', data, re.S)
		if staffeln:
			print "staffeln parsen gefunden"
			self.streamList = []
			for urlPart, season in staffeln:
				url = '%s%s' % ('http://www.movie4k.to/', urlPart)
				formatTitle = 'Season %s' % season
				self.filmliste.append((decodeHtml(formatTitle), url))
			self.chooseMenuList.setList(map(m4kSerienABCStaffelnEntry, self.filmliste))
			self.keyLocked = False
		else:
			print "parsen - Keine Daten gefunden"

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kSerienABCListeStaffelnFilme, streamLink)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()

	def keyCancel(self):
		self.close()

class m4kSerienABCListeStaffelnFilme(Screen):

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
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
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("movie4k.to")
		self['name'] = Label("Staffel Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		self.page = 1
		self['page'] = Label(" ")
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.streamGenreLink, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		print error

	def loadPageData(self, data):
		print self.streamGenreLink
		staffeln = re.findall('<TD id="tdmovies" width="538"><a href="(.*?)">(.*?), Season:(.*?), Episode:(.*?)<', data, re.S)
		if staffeln:
			print "episode parsen gefunden"
			self.streamList = []
			for urlPart, title, season, episode in staffeln:
				url = '%s%s' % ('http://www.movie4k.to/', urlPart)
				formatTitle = 'Season %s Episode %s' % (season, episode)
				print url
				self.filmliste.append((decodeHtml(formatTitle), url, title))
			self.chooseMenuList.setList(map(m4kSerienABCStaffelnEntry, self.filmliste))
			self.keyLocked = False
		else:
			print "parsen - Keine Daten gefunden"

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return
		streamEpisode = self['filmList'].getCurrent()[0][2] + self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(m4kStreamListeScreen, streamLink, streamEpisode, "tv")

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()

	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()

	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()

	def keyCancel(self):
		self.close()

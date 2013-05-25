from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.yt_url import *
import Plugins.Extensions.MediaPortal.resources.tools as mechanize

def cannaGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
def cannaListEntry(entry):
	#TYPE_TEXT, x, y, width, height, fnt, flags, string [, color, backColor, backColorSelected, borderWidth, borderColor])
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
		
def cannaYearListEntry(entry):
	#TYPE_TEXT, x, y, width, height, fnt, flags, string [, color, backColor, backColorSelected, borderWidth, borderColor])
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]	

class cannaGenreScreen(Screen):
	
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
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red": self.keyCancel
		}, -1)
		
		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		self.playing = False
		
		self.keyLocked = True
		self['title'] = Label("Canna.to")
		self['ContentTitle'] = Label("Alben:")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):	
		self.genreliste = [('TOP100 Single Charts',"http://ua.canna.to/canna/single.php","1"),
							('Austria Single Charts',"http://ua.canna.to/canna/austria.php","1"),
							('Black Charts Top 40',"http://ua.canna.to/canna/black.php","1"),
							('US Billboard Country Charts Top 30',"http://ua.canna.to/canna/country.php","1"),
							('Offizielle Dance Charts Top 50',"http://ua.canna.to/canna/odc.php","1"),
							('Party Schlager Charts Top 30',"http://ua.canna.to/canna/psc.php","1"),
							('Reggae Charts Top 20',"http://ua.canna.to/canna/reggae.php","1"),
							('Rock & Metal Single Charts Top 40',"http://ua.canna.to/canna/metalsingle.php","1"),
							('Swiss Single Charts Top 75',"http://ua.canna.to/canna/swiss.php","1"),
							('UK Single Charts Top 40',"http://ua.canna.to/canna/uksingle.php","1"),
							('US Billboard Single Charts Top 100',"http://ua.canna.to/canna/ussingle.php","1"),
							('-- Jahrescharts --', "dump","1"),
							('Single Jahrescharts',"http://ua.canna.to/canna/jahrescharts.php","2"),
							('Austria Jahrescharts',"http://ua.canna.to/canna/austriajahrescharts.php","2"),
							('Black Jahrescharts',"http://ua.canna.to/canna/blackjahrescharts.php","2"),
							('Dance Jahrescharts',"http://ua.canna.to/canna/dancejahrescharts.php","2"),
							('Party Schlager Jahrescharts',"http://ua.canna.to/canna/partyjahrescharts.php","2"),
							('Swiss Jahrescharts',"http://ua.canna.to/canna/swissjahrescharts.php","2")]
							
		self.chooseMenuList.setList(map(cannaGenreListEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked or self['genreList'].getCurrent()[0][1] == "dump":
			return
		cannahdGenre = self['genreList'].getCurrent()[0][0]
		cannahdUrl = self['genreList'].getCurrent()[0][1]
		cannahdID = self['genreList'].getCurrent()[0][2]
		print cannahdGenre, cannahdUrl, cannahdID
		
		if cannahdID == "1":
			self.session.open(cannaMusicListeScreen, cannahdGenre, cannahdUrl)
		else:
			self.session.open(cannaJahreScreen, cannahdGenre, cannahdUrl)
		
	def keyCancel(self):
		self.session.nav.stopService()
		self.session.nav.playService(self.lastservice)
		self.playing = False
		self.close()
		
class cannaMusicListeScreen(Screen, InfoBarBase, InfoBarSeek):
	
	def __init__(self, session, genreName, genreLink):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/showSongstoAll.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/showSongstoAll.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		InfoBarBase.__init__(self)
		InfoBarSeek.__init__(self)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self.keyLocked = True
		self["title"] = Label("Canna.to - %s" % self.genreName)
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("%s" % self.genreName)

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['streamlist'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
			
	def loadPage(self):
		self.keyLocked = True
		print self.genreLink
		getPage(self.genreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		print "drin"
		match = re.findall('<tr>.*?<font>(.*?)</font>.*?class="obutton" onClick="window.open..(.*?)...CannaPowerChartsPlayer.*?</tr>', data, re.S)
		if match:
			for title,url in match:
				url = "http://ua.canna.to/canna/"+url
				self.filmliste.append((decodeHtml(title),url))
			self.chooseMenuList.setList(map(cannaListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def getDLurl(self, url):
		try:
			content = self.getUrl(url)
			match = re.findall('flashvars.playlist = \'(.*?)\';', content)
			if match:
				for url in match:
					url = 'http://ua.canna.to/canna/'+url
					content = self.getUrl(url)
					match = re.findall('<location>(.*?)</location>', content)
					if match:
						for url in match:
							url = 'http://ua.canna.to/canna/'+url
							req = mechanize.Request('http://ua.canna.to/canna/single.php')
							response = mechanize.urlopen(req)
							req = mechanize.Request(url)
							req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
							response = mechanize.urlopen(req)
							response.close()
							code=response.info().getheader('Content-Location')
							url='http://ua.canna.to/canna/avzt/'+code
							print url
							return url
							
		except urllib2.HTTPError, error:
			print error
			message = self.session.open(MessageBox, ("Fehler: %s" % error), MessageBox.TYPE_INFO, timeout=3)
			return False

		except urllib2.URLError, error:
			print error.reason
			message = self.session.open(MessageBox, ("Fehler: %s" % error), MessageBox.TYPE_INFO, timeout=3)
			return False
				
	def getUrl(self, url):
		req = mechanize.Request(url)
		req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = mechanize.urlopen(req)
		link = response.read()
		response.close()
		return link	
		
	def keyOK(self):
		if self.keyLocked:
			return
		cannaName = self['streamlist'].getCurrent()[0][0]
		cannaUrl = self['streamlist'].getCurrent()[0][1]
		print cannaName, cannaUrl
		playinfos = cannaName.split(' - ')
		if playinfos:
			self["artist"].setText(playinfos[0])
			self["songtitle"].setText(playinfos[1])

		stream_url = self.getDLurl(cannaUrl)
		if stream_url:
			print stream_url
			sref = eServiceReference(0x1001, 0, stream_url)
			self.session.nav.playService(sref)
			self.playing = True
			
	def doEofInternal(self, playing):
		print "Play Next Song.."
		self['streamlist'].down()
		self.keyOK()

	def lockShow(self):
		pass
		
	def unlockShow(self):
		pass
		
	def keyCancel(self):
		self.close()
		
		
class cannaJahreScreen(Screen):
	
	def __init__(self, session, genreName, genreLink):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red": self.keyCancel
		}, -1)
			
		self.keyLocked = True
		self['title'] = Label("Canna.to")
		self['ContentTitle'] = Label("Jahre:")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		print self.genreLink
		getPage(self.genreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		print "drin"
		match = re.compile('<b><font face="Arial" size="5" color="#FFCC00"><a href="(.*?)">(.*?)</a></font></b>').findall(data, re.S)
		if match:
			for url, title in match:
				url = "http://ua.canna.to/canna/"+url
				self.filmliste.append((decodeHtml(title),url))
			self.filmliste.reverse()
			self.chooseMenuList.setList(map(cannaYearListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def keyOK(self):
		if self.keyLocked:
			return
		cannahdGenre = self['genreList'].getCurrent()[0][0]
		cannahdUrl = self['genreList'].getCurrent()[0][1]
		self.session.open(cannaMusicListeScreen2, cannahdGenre, cannahdUrl)
		
	def keyCancel(self):
		self.playing = False
		self.close()
		
class cannaMusicListeScreen2(Screen, InfoBarBase, InfoBarSeek):
	
	def __init__(self, session, genreName, genreLink):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"
		
		path = "%s/%s/showSongstoAll.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/showSongstoAll.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		InfoBarBase.__init__(self)
		InfoBarSeek.__init__(self)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self.keyLocked = True
		self["title"] = Label("Canna.to - %s" % self.genreName)
		self["coverArt"] = Pixmap()
		self["songtitle"] = Label ("")
		self["artist"] = Label ("")
		self["album"] = Label ("%s" % self.genreName)

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['streamlist'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)
			
	def loadPage(self):
		self.keyLocked = True
		print self.genreLink
		getPage(self.genreLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)
		
	def loadPageData(self, data):
		print "drin"
		raw = re.findall('<td align="left" style="border-style:solid; border-width:1px;">(.*?)>>  Player  <<', data, re.S)
		if raw:
			for each in raw:
				match = re.findall('<font size="1" face="Arial"><b>(.*?)</b></font>.*?<font size="1" face="Arial"><b>(.*?)</b></font>.*?(jc_player.php.*?)\'', each, re.S)
				if match:
					for (artist,title,url) in match:
						url = "http://ua.canna.to/canna/"+url
						title = "%s - %s" % (artist, title)
						self.filmliste.append((decodeHtml(title),url))
			self.chooseMenuList.setList(map(cannaListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		print error

	def getDLurl(self, url):
		try:
			content = self.getUrl(url)
			match = re.findall('flashvars.playlist = \'(.*?)\';', content)
			if match:
				for url in match:
					url = 'http://ua.canna.to/canna/'+url
					content = self.getUrl(url)
					match = re.findall('<location>(.*?)</location>', content)
					if match:
						for url in match:
							url = 'http://ua.canna.to/canna/'+url
							req = mechanize.Request('http://ua.canna.to/canna/single.php')
							response = mechanize.urlopen(req)
							req = mechanize.Request(url)
							req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
							response = mechanize.urlopen(req)
							response.close()
							code=response.info().getheader('Content-Location')
							url='http://ua.canna.to/canna/avzt/'+code
							print url
							return url
							
		except urllib2.HTTPError, error:
			print error
			message = self.session.open(MessageBox, ("Fehler: %s" % error), MessageBox.TYPE_INFO, timeout=3)
			return False

		except urllib2.URLError, error:
			print error.reason
			message = self.session.open(MessageBox, ("Fehler: %s" % error), MessageBox.TYPE_INFO, timeout=3)
			return False
				
	def getUrl(self, url):
		req = mechanize.Request(url)
		req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = mechanize.urlopen(req)
		link = response.read()
		response.close()
		return link	
		
	def keyOK(self):
		if self.keyLocked:
			return
		cannaName = self['streamlist'].getCurrent()[0][0]
		cannaUrl = self['streamlist'].getCurrent()[0][1]
		print cannaName, cannaUrl
		playinfos = cannaName.split(' - ')
		if playinfos:
			self["artist"].setText(playinfos[0])
			self["songtitle"].setText(playinfos[1])

		stream_url = self.getDLurl(cannaUrl)
		if stream_url:
			print stream_url
			sref = eServiceReference(0x1001, 0, stream_url)
			self.session.nav.playService(sref)
			self.playing = True
			
	def doEofInternal(self, playing):
		print "Play Next Song.."
		self['streamlist'].down()
		self.keyOK()

	def lockShow(self):
		pass
		
	def unlockShow(self):
		pass
		
	def keyCancel(self):
		self.close()
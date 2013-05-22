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
		
		self.keyLocked = True
		self['title'] = Label("Canna.to")
		self['ContentTitle'] = Label("Genre:")
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
		self.genreliste = [('TOP100 Single Charts',"http://ua.canna.to/canna/single.php"),
							('Austria Single Charts',"http://ua.canna.to/canna/austria.php"),
							('Black Charts Top 40',"http://ua.canna.to/canna/black.php"),
							('US Billboard Country Charts Top 30',"http://ua.canna.to/canna/country.php"),
							('Offizielle Dance Charts Top 50',"http://ua.canna.to/canna/odc.php"),
							('Party Schlager Charts Top 30',"http://ua.canna.to/canna/psc.php"),
							('Reggae Charts Top 20',"http://ua.canna.to/canna/reggae.php"),
							('Rock & Metal Single Charts Top 40',"http://ua.canna.to/canna/metalsingle.php"),
							('Swiss Single Charts Top 75',"http://ua.canna.to/canna/swiss.php"),
							('UK Single Charts Top 40',"http://ua.canna.to/canna/uksingle.php"),
							('US Billboard Single Charts Top 100',"http://ua.canna.to/canna/ussingle.php")]

		self.chooseMenuList.setList(map(cannaGenreListEntry, self.genreliste))
		self.keyLocked = False

	def dataError(self, error):
		print error

			
	def keyOK(self):
		if self.keyLocked:
			return
		cannahdGenre = self['genreList'].getCurrent()[0][0]
		cannahdUrl = self['genreList'].getCurrent()[0][1]
		print cannahdGenre, cannahdUrl
		self.session.open(cannaMusicListeScreen, cannahdGenre, cannahdUrl)
		
	def keyCancel(self):
		self.close()
		
class cannaMusicListeScreen(Screen):
	
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
			"cancel": self.keyCancel
		}, -1)
		
		self.keyLocked = True
		self['title'] = Label("Canna.to")
		self['ContentTitle'] = Label("%s:" % self.genreName)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
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
		cannaName = self['genreList'].getCurrent()[0][0]
		cannaUrl = self['genreList'].getCurrent()[0][1]
		print cannaName, cannaUrl
		stream_url = self.getDLurl(cannaUrl)
		if stream_url:
			print stream_url
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(cannaName)
			self.session.open(MoviePlayer, sref)
		
		
	def keyCancel(self):
		self.close()
		
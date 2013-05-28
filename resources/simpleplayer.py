#	-*-	coding:	utf-8	-*-

from Screens.InfoBarGenerics import *
from Plugins.Extensions.MediaPortal.resources.imports import *

class SimplePlayer(Screen, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):
	ENABLE_RESUME_SUPPORT = True
	ALLOW_SUSPEND = True
	
	def __init__(self, session, playList, playIdx=0, playAll=False):
		Screen.__init__(self, session)
		print "SimplePlayer:"
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		
		InfoBarNotifications.__init__(self)
		InfoBarBase.__init__(self)
		InfoBarShowHide.__init__(self)

		self["actions"] = ActionMap(["WizardActions"],
		{
			"up": 		self.openPlaylist,
			"back":		self.exitPlayer,
			"left":		self.playPrevStream,
			"right":	self.playNextStream

		}, -1)
		
		self.allowPiP = False
		InfoBarSeek.__init__(self)

		self.skinName = 'MoviePlayer'
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()

		self.playAll = playAll
		self.playList = playList
		self.playIdx = playIdx
		self.playLen = len(playList)
		self.returning = False
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
	
	def exitPlayer(self):
		print "exitPlayer:"
		self.close()

	def doEofInternal(self, playing):
		print "doEofInt:"
		if playing == True:
			self.playNextStream()
				
	def playExit(self):
		print "playExit:"
		self.session.nav.playService(self.lastservice)

	def getVideo(self):
		print "getVideo:"
		self.close()

	def openPlaylist(self):
		self.session.openWithCallback(self.cb_Playlist, SimplePlaylist, self.playList, self.playIdx)
		
	def cb_Playlist(self, data):
		if data != -1:
			self.playIdx = data
			self.getVideo()
		
def playListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
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

	def showPlaylist(self):
		print 'showPlaylist:'
		if self.listTitle != None:
			self['ContentTitle'].setText(self.listTitle)
		else:
			self['ContentTitle'].setText("Auswahl")

		self.chooseMenuList.setList(map(playListEntry, self.playList))
		self['genreList'].moveToIndex(self.playIdx)

	def exit(self):
		self.close(-1)

	def ok(self):
		idx = self['genreList'].getSelectedIndex()
		self.close(idx)

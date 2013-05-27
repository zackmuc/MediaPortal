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

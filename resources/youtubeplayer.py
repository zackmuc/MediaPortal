#	-*-	coding:	utf-8	-*-

from Components.config import config
from Plugins.Extensions.MediaPortal.resources.yt_url import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer

class YoutubePlayer(SimplePlayer):

	def __init__(self, session, playList, playIdx=0, playAll=False, listTitle=None, plType='local', title_inr=0):
		print "YoutubePlayer:"
		self.videoPrio = int(config.mediaportal.youtubeprio.value)-1
		
		SimplePlayer.__init__(self, session, playList, playIdx, playAll, listTitle, plType, title_inr)
		
	def getVideo(self):
		print "getVideo:"
		dhTitle = self.playList[self.playIdx][self.title_inr]
		dhVideoId = self.playList[self.playIdx][2]
		print "Title: ",dhTitle
		#print "VideoId: ",dhVideoId
		y = youtubeUrl(self.session)
		y.addErrback(self.dataError)
		dhLink = y.getVideoUrl(dhVideoId, self.videoPrio)
		if dhLink:
			self.playStream(dhTitle, dhLink)

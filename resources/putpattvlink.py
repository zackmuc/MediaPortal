#	-*-	coding:	utf-8	-*-

from Plugins.Extensions.MediaPortal.resources.imports import *

class PutpattvLink:

	def __init__(self, session):
		print "PutpattvLink:"
		self.session = session
		self._callback = None
		self.title = ''

	def getLink(self, cb_play, cb_err, title, url, token):
		self._callback = cb_play
		self.title = title
		
		if url != None:
			self._callback(title, url)
		else:
			url = 'http://www.putpat.tv/ws.xml?client=putpatplayer&partnerId=1&token=%s=&streamingMethod=http&method=Asset.getClipForToken' % token
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getToken).addErrback(cb_err)

	def getToken(self, data):
		phClip = re.findall('<medium>(.*?)</medium>', data, re.S)
		url = None
		if phClip:
			for phUrl in phClip:
				url = phUrl.replace('&amp;','&')
				
		self._callback(self.title, url)

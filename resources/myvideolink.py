#	-*-	coding:	utf-8	-*-

from base64 import b64decode
from binascii import unhexlify
import hashlib, re, os, sha
from urllib import unquote, urlencode
from Plugins.Extensions.MediaPortal.resources.imports import *

class MyvideoLink:
	def __init__(self, session):
		print "MyvideoLink:"
		self.session = session
		self._callback = None
		self._errback = None
		self.GK = ('WXpnME1EZGhNRGhpTTJNM01XVmhOREU0WldNNVpHTTJOakpt'
			'TW1FMU5tVTBNR05pWkRaa05XRXhNVFJoWVRVd1ptSXhaVEV3'
			'TnpsbA0KTVRkbU1tSTRNdz09')

	def getLink(self, cb_play, cb_err, title, url, token, imgurl=''):
		self._callback = cb_play
		self._errback = cb_err
		self.myvideoTitle = title
		"""
		id = re.findall('/watch/(.*?)/', url)
		if id:
			mv_url = "http://www.myvideo.de/dynamic/get_player_video_xml.php?ID=" + id[0]
			print self.myvideoTitle, url, id[0]
		
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream, id[0]).addErrback(cb_err)
		else:
			cb_err('No ID found')
		"""
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream, title, token, imgurl).addErrback(cb_err)
			
	def __md5(self, s):
		return hashlib.md5(s).hexdigest()

	def __rc4crypt(self, data, key):
		x = 0
		box = range(256)
		for i in range(256):
			x = (x + box[i] + ord(key[i % len(key)])) % 256
			box[i], box[x] = box[x], box[i]
		x = 0
		y = 0
		out = []
		for char in data:
			x = (x + 1) % 256
			y = (y + box[x]) % 256
			box[x], box[y] = box[y], box[x]
			out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
		return ''.join(out)
		
	def getStream(self, data, title, token, imgurl):
		data = data.replace("_encxml=","")
		enc_data_b = unhexlify(data)
		sk = self.__md5(b64decode(b64decode(self.GK)) + self.__md5(str(token)))
		dec_data = self.__rc4crypt(enc_data_b, sk)
		link = None
		
		pos = title.find('. ', 0, 5)
		if pos > 0:
			pos += 2
			title = title[pos:]
			
		scArtist = ''
		scTitle = title
		p = title.find(' -- ')
		if p > 0:
			scArtist = title[:p].strip()
			scTitle = title[p+4:].strip()
			
		if dec_data:
			if "rtmp" not in dec_data:
				self._errback("getStream: No rtmp url found!")
				
			url = re.findall("connectionurl='(.*?)'", dec_data, re.S)
			source = re.findall("source='(.*?)'", dec_data, re.S)
			url =  unquote(url[0])
			source =  unquote(source[0])
			vorne = re.findall('(.*?)\.', source, re.S)
			hinten = re.findall('\.(.*[a-zA-Z0-9])', source, re.S)
			string23 = "/%s playpath=%s" % (hinten[0], vorne[0])
			link = "%s%s" % (url, string23)
			
		self._callback(scTitle, link, imgurl=imgurl, artist=scArtist)

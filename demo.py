#cyxomo
#2018.10.10

import urllib
import urllib2
import zlib
import re 

'''
key:
	By commend: response.headers.get('Content-Encoding') 
				[response is the return urllib.urlopen()]
				return  a str is the name of Compression format
				I know 3 type   1. deflate
								2. zlib
								3. gzip
	unzip by zlib.decompress(html, wbits)
				deflate: wbits = -zlib.MAX_WBITS
				zlib:    wbits = zlib.MAX_WBITS
				gzip:    wbits = zlib.MAX_WBITS | 16

error analysis:
	ERROR:    urllib.error.HTTPError: HTTP Error 403: Forbidden
	need the 'UserAgent'
	by add headers for request to solve this issue

'''


def unzip(data, ziptype):
	if ziptype == 'gzip':
		wbits = 16+zlib.MAX_WBITS
	elif ziptype == 'zlib':
		wbits = zlib.MAX_WBITS
	elif ziptype == 'deflate':
		wbits = -zlib.MAX_WBITS
	try:
		return zlib.decompress(data, wbits)
	except zlib.error:
		return zlib.decompress(data)

avurl = 'https://www.bilibili.com/video/av33381919'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
avrequest = urllib2.Request(url = avurl, headers=headers)
#print type(avrequest)
avrequest.add_header('Accept-encoding', 'gzip')
avopener = urllib2.build_opener()
avresponse = avopener.open(avrequest)
#print type(avresponse)
avhtml = avresponse.read()
avziptype = avresponse.headers.get('Content-Encoding')
avhtml = unzip(avhtml, avziptype)
#print avhtml

#cidpatten = re.compile(r'cid=(\d+)&aid=')
#cidlist = cidpatten.findall(avhtml)
#cidn = cidlist[0]
cidn = re.search(r'cid=(\d+)&aid=', avhtml)
cidnum = cidn.groups()[0]
print cidnum

'''
avid=33381919


avurl = 'https://www.bilibili.com/video/av'+str(avid)
vpagezip = urllib.urlopen(avurl)
print type(vpagezip)
vcode = vpagezip.read()
#print vcode
cidpatten = re.compile(r'cid=(.*)&aid=')
cidn = cidpatten.match(vcode)
print cidn

'''
#cidnum = 58225057
cidurl = 'http://comment.bilibili.com/'+str(cidnum)+'.xml'

cidresponse = urllib2.urlopen(cidurl)

cidziptype = cidresponse.headers.get('Content-Encoding')
cidpage = cidresponse.read()
cidhtml = unzip(cidpage, cidziptype)
print type(cidhtml)


patten = re.compile(r'">(.*?)</d>')
op =patten.findall(cidhtml)
print(len(op))

with open('kkkkp', 'w') as f:
	for ele in op:
		f.write(ele+'\n')

#print kk






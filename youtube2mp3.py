# -*- coding: utf-8 -*-
import requests, re, sys
import js2py, time, json, os
import urlparse

def spider_downloader(MP3_URL, filename):
	r = requests.get(MP3_URL, stream=True)
	filename = os.path.join(filename)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=32):
			f.write(chunk)
            
server = {
        1: "odg", 5: "uuj", 9: "ebr",  13: "hrh",
        2: "ado", 6: "bkl", 10: "asx", 14: "quq",
        3: "jld", 7: "fnw", 11: "ghn", 15: "zki",
        4: "tzg", 8: "eeq", 12: "eal", 16: "tff",

        17: "aol", 21: "yyd", 25: "ihi", 29: "omp",
        18: "eeu", 22: "hdi", 26: "heh", 30: "eez",
        19: "kkr", 23: "ddb", 27: "xaa", 31: "rpx",
        20: "yui", 24: "iir", 28: "nim", 32: "cxq",
         
        33: "typ", 37: "vro",
        34: "amv", 38: "pfg",
        35: "rlv", 39: "xbo",
        36: "xnx", 40: "bas"  
}

def get_k(key):
    f = js2py.eval_js(
    """o = function(t) {
            var e, r, o = t.split("").length, n = [65, 91, 96, 122, 1], s = "";
            for (e = 0; e < o; e++)
                r = t.charCodeAt(e),
                s += n[0] < r && r < n[1] ? String.fromCharCode(r - n[4]) : n[2] < r && r < n[3] ? String.fromCharCode(r + n[4]) : 48 < r && r < 53 ? 2 * parseInt(String.fromCharCode(r)) : 45 == r || 95 == r ? 45 == r ? String.fromCharCode(95) : String.fromCharCode(45) : String.fromCharCode(r),
                r = "";
                return s
    }('%s')""" % key
    )
    return f

def youtube2mp3_downloader(url): 
   
    parsed = urlparse.urlparse(url)
    serial = urlparse.parse_qs(parsed.query)['v'][0]
    
    
    s = requests.Session()
    res = s.get('https://ytmp3.cc/')
    
    content = res.text
    
    for line in content.split('\n'):
        m = re.match('.*^.*\/js\/ytmp3\.js\?.=(.*?)&', line)
        if m:
            k = get_k(m.group(1))
    
    p = {
        'callback': 'jQuery33105214746472378784_%d' % int(time.time()*1000),
        'v': serial,
        'f': 'mp3',
        'k': k,
        '_': '%d' % int(time.time()*1000+2)
    }
    
    h = {
        'Host': 'd.ymcdn.cc',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://ytmp3.cc/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9'
    }
    
    res = s.get('https://d.ymcdn.cc/check.php', headers=h, params=p)
    
    m = re.match('jQuery33105214746472378784_.*?\((.*)\)', res.content)
    #print res.content
    info = json.loads(m.group(1))
    
    # https://ebr.ymcdn.cc/3714bd4c62dbf1ad88833a44721a92d7/id56eoDIPK4
    sid = server[int(info['sid'])]
    download_link = 'https://%s.ymcdn.cc/%s/%s' % (sid, info['hash'], serial)
    print 'link', download_link
    spider_downloader(download_link, info['title'] + '.mp3')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'Please give youtube link'
        exit(1)

    url = sys.argv[1]
    youtube2mp3_downloader(url)
    

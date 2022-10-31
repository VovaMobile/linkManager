import config
import re
url_re = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ][^ \r]*")
bad_chars = '\'\\.,[](){}:;"'
gp = None

def GetUrl(text):
 return [s.strip(bad_chars) for s in url_re.findall(text)]



def ConfigInit():
	confspec = {
		"read_urls":"boolean(default=true)"
	}
	config.conf.spec["link_manager"] = confspec

def get(key):
		return config.conf["link_manager"][key]

def set(key, value):
	config.conf["link_manager"][key] = value


import http.cookiejar, urllib.request
import re, os
username = "PG@example.com"
password = "123456"
captcha = ""


# Create the opener, which is using cookiejar for processing cookies.
cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 
first_page = opener.open("http://share.dmhy.org/user/login").read().decode("utf-8")
m = re.search("common\/generate\-captcha\?code=([0-9]+)", first_page)
captcha_pic = opener.open("http://share.dmhy.org/common/generate-captcha?code=" + m.group(1)).read()
open("PG.jpg", 'wb').write(captcha_pic)
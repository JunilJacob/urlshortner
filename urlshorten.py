import webapp2
import random
import urllib
from google.appengine.ext import db


class urlshort(db.Model):
  
  url = db.StringProperty()
  code = db.StringProperty()
def gencode(url):
	Rcode="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	code = str(random.randint(0,9))
	while checkCode(code):
			code += Rcode[random.randint(0, len(Rcode) - 1)]
	return code

def checkCode(code):
		if len(code) < 6:
			return 1
		back = urlshort.gql("WHERE code = :1 LIMIT 1",code)
		return back.count(1) > 0
	
class MainPage(webapp2.RequestHandler):
	def get(self):

		code=self.request.get('uc')
		if code:
			urls=urlshort.gql("WHERE code = :1 LIMIT 1",code)
			url = urls[0].url
			url=str(url)
			if url.lower().startswith('http'):
				self.redirect(url)
			else:
				self.redirect("http://" + url)
			
                	
        		
		else:

			self.response.headers['content-Type'] = 'html'
			self.response.write("""<html><form action="/shorturl" method="post" >Url<br><br><input name="url">
						<br><br><input type=submit value="Shorten Url" ></form>	</html>""")


class Database(webapp2.RequestHandler):

	def post(self):
		self.response.headers['content-Type'] = 'html'
		Url=self.request.get('url')
		if not Url:
			self.redirect("/")
		back = urlshort.gql("WHERE url = :1 LIMIT 1",Url)
		if back.count(1) == 0:
			Code=gencode(Url)
			instance =urlshort(url=Url,code=Code)
			instance.put()
		else:
			data=urlshort.gql("WHERE url = :1 LIMIT 1",Url)
			Code = ""
        		for i in data:
                		Code = i.code
		siteurl=self.request.url.split("/")[:-1]
		self.response.write('<html><body><a href=')
		self.response.write("/".join(siteurl)+"/?uc="+Code)
		self.response.write('>')
		self.response.write("/".join(siteurl)+"/?uc="+Code)
		self.response.write('</a></body></html>')
app = webapp2.WSGIApplication([('/', MainPage),('/shorturl', Database)],debug=True)

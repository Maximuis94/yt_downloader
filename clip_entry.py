
class ClipEntry():
	def __init__(self, url, title="", name="", artist="", contartist="", album="", genre="", year="", imageurl = "", image=None):
		self.url = url
		self.title = title
		self.name = name
		self.artist = artist
		self.contartist = contartist
		self.album = album
		self.genre = genre
		self.year = year
		self.imageurl = imageurl
		self.image = image
		self.filename = title + ".mp3"
	
	def get_dict(self):
		return {'url':self.url,'title':self.title,'name':self.name,'artist':self.artist,'contartist':self.contartist,'album':self.album,'genre':self.genre,'year':self.year,'image':self.image}
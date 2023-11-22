import pytube
from pytube import YouTube
import time
from moviepy.editor import *
import eyed3


class MP3Downloader:
	def __init__(self, entry, file_name=None, infolabel=None):
		cd = str(os.getcwd().replace('\\', '/')) + '/'
		self.out_folder = cd+'tracks/'
		self.temp_folder = cd+'temp/'
		
		for next_dir in self.out_folder, self.temp_folder:
			if not os.path.exists(next_dir):
				os.mkdir(next_dir)
		
		self.filename = f"{entry.artist} - {entry.name}" if file_name is None else file_name
		self.entry = entry
		self.infolabel = infolabel
		self.download_start = 0
		self.file_size = 0
 
	# on_progress_callback takes 4 parameters.
	def progress_check(self, stream = None, chunk = None, file_handle = None, remaining = None):
		if remaining is None:
			return ''
		downloaded = (self.file_size - remaining)
		cur = time.time()
		elapsed_time = int(cur - self.download_start)
		dl_speed = (downloaded / (cur - self.download_start))//1000
		p = int(downloaded / self.file_size * 100)
		
		label = str(downloaded//1000) + "/" + str(self.file_size//1000) + "kb downloaded at " + str(dl_speed) + "kb/s (" + str(p) + "%) Time taken: " + str(elapsed_time) + "s"
		#self.update_infolabel(label)
		print(label,end="\r")
		#print(str(downloaded//1000) + "/" + str(file_size//1000) + "kb downloaded at " + str(dl_speed) + "kb/s (" + str(p) + "%) Time taken: " + str(elapsed_time) + "s",end="\r")
		time.sleep(.01)
		
	# Check the streams in the YouTube URL, check the bitrate qualities and download best quality audio stream
	# URL = youtube URL (e.g. 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
	# fname = output file name (def=video title)
	# first_stream = set True to download the first stream (faster download / lower quality) (def=False)
	def download_best_mp3(self, first_stream=True, remove_temp: bool = None):
		# yt = YouTube(self.entry.url, on_progress_callback=self.progress_check)
		yt = YouTube(self.entry.url)
		streams = yt.streams.all()
		
		# Get stream w/ highest abr
		highest_abr, idx = -1, -1
		for s in streams:
			if isinstance(s, pytube.Stream):
				if s.abr is not None:
					# print(s.__dict__)
					abr = int(s.abr[:-4])
					if abr > highest_abr:
						idx, highest_abr = streams.index(s), abr
		stream = streams[idx]
		
		label = "Processing " + self.entry.title + "... Filesize = " + str(int(self.file_size)//1000) + "kb"
		self.update_infolabel(label)
		#for s in streams:
		#    print(str(s) + "\tFilesize: " + str(s.filesize) + "Bitrate: " + str(s.abr))
		start = time.time()

		if self.filename == "":
			self.filename = stream.title
		print("Best stream:")
		print(stream)
		print("File size: " + str(stream.filesize))
		print("Bitrate: " + stream.abr)
		print("Output filename: " + self.filename + ".mp3")
		ext = "." + stream.subtype
		temp_file = self.temp_folder + self.filename + ext
		print("Downloading stream...")
		global file_size
		self.file_size = stream.filesize
		self.download_start = time.time()
		self.update_infolabel("Downloading stream... This might take a while!")
		# stream.download(filename=self.filename+ext)
		stream.download(filename=temp_file)
		
		# Extract the audio stream from the video
		if stream.subtype == "video":
			# video = VideoFileClip(self.filename+ext)
			video = VideoFileClip(temp_file)
			video.reader.close()
			audio = video.audio
			print(audio)
		else:
			# audio = AudioFileClip(self.filename+ext)
			audio = AudioFileClip(temp_file)
		br_str = str(highest_abr) + "k"
		self.update_infolabel("Stream downloaded! Creating mp3... elapsed time: " + str(int(time.time()-start)) + " seconds")
		#print("Stream downloaded! Creating mp3... elapsed time: " + str(int(time.time()-start)) + " seconds")
		
		audio.write_audiofile(self.out_folder+self.filename+".mp3", bitrate=br_str)
		audio.close()
		if remove_temp:
			os.remove(temp_file)
		print("Elapsed time: " + str(int(time.time()-start)) + " seconds")
		self.set_mp3_metadata()
		return self.filename+".mp3"
		
	def set_mp3_metadata(self):
		audio = eyed3.load(self.out_folder + self.filename + ".mp3")
		if self.entry.name != "":
			audio.tag.title = self.entry.name
		if self.entry.artist != "":
			audio.tag.album_artist = self.entry.artist
		if self.entry.year != "":
			audio.tag.release_date = self.entry.year
		if self.entry.album != "":
			audio.tag.album = self.entry.album
		if self.entry.genre != "":
			audio.tag.genre = self.entry.genre
		if self.entry.imageurl != "":
			audio.tag.images.set(type_=3, img_data=None, mime_type='image/jpg', img_url=self.entry.imageurl)
		audio.tag.save()
		if audio.tag.album_artist is not None and audio.tag.title is not None:
			fnew = f"{audio.tag.album_artist} - {audio.tag.title}.mp3"
		else:
			fnew = self.filename + '.mp3'
		os.rename(self.out_folder + self.filename + ".mp3", self.out_folder + fnew)
		
	def update_infolabel(self, text):
		self.infolabel.configure(text=text)
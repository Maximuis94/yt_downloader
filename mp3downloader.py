import pytube
from pytube import YouTube
import time
from moviepy.editor import *
import eyed3


class MP3Downloader:
	def __init__(self, entry, file_name=None, info_label=None):
		cd = str(os.getcwd().replace('\\', '/')) + '/'
		self.out_folder = cd+'tracks/'
		self.temp_folder = cd+'temp/'
		
		# Create output and temp folders, if they do not exist
		for next_dir in self.out_folder, self.temp_folder:
			if not os.path.exists(next_dir):
				os.mkdir(next_dir)
		
		self.filename = f"{entry.artist} - {entry.name}" if file_name is None else file_name
		self.entry = entry
		self.info_label = info_label
		self.download_start = 0
		self.file_size = 0
 
	def progress_check(self, stream=None, chunk=None, file_handle=None, remaining=None):
		""" Callback for YouTube class, currently not in use as it produced errors. Can be deleted(?) """
		if remaining is None:
			return ''
		downloaded = (self.file_size - remaining)
		cur = time.time()
		elapsed_time = int(cur - self.download_start)
		dl_speed = (downloaded / (cur - self.download_start))//1000
		p = int(downloaded / self.file_size * 100)
		
		label = str(downloaded//1000) + "/" + str(self.file_size//1000) + "kb downloaded at " + str(dl_speed) + \
		        "kb/s (" + str(p) + "%) Time taken: " + str(elapsed_time) + "s"
		# self.update_infolabel(label)
		print(label,end="\r")
		# print(str(downloaded//1000) + "/" + str(file_size//1000) + "kb downloaded at " + str(dl_speed) +
		# "kb/s (" + str(p) + "%) Time taken: " + str(elapsed_time) + "s",end="\r")
		time.sleep(.01)

	def download_mp3(self, first_stream: bool = False, remove_temp: bool = True):
		"""
		Extract the audio stream from the given YouTube URL and export it as an mp3 file with the configured metadata.
		
		Parameters
		----------
		first_stream : bool, optional, False by default
			Flag to determine whether to use the first stream or not. First stream is typically of lower quality.
		remove_temp : bool, optional, True by default
			Flag to determine whether or not temporary files should be removed, e.g. intermediate mp4 files that as they
			are saved before extracting the audio component if the source stream is a video.
		"""
		# yt = YouTube(self.entry.url, on_progress_callback=self.progress_check)
		yt = YouTube(self.entry.url)
		if first_stream:
			stream = yt.streams.first()
			br_str = stream.abr[:-3]
		else:
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
			br_str = f"{highest_abr}k"
		
		label = "Processing " + self.entry.title + "... Filesize = " + str(int(self.file_size)//1000) + "kb"
		self.update_infolabel(label)
		start = time.time()

		if self.filename == "":
			self.filename = stream.title
		ext = "." + stream.subtype
		temp_file = self.temp_folder + self.filename + ext
		
		print("Best stream:")
		print(stream)
		print("File size: " + str(stream.filesize))
		print("Bitrate: " + stream.abr)
		print("Output filename: " + self.filename + ".mp3")
		print("Downloading stream...")
		# global file_size
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
		
		self.update_infolabel(f"Stream downloaded! Creating mp3... elapsed time: {int(time.time()-start)} seconds")
		
		audio.write_audiofile(self.out_folder+self.filename+".mp3", bitrate=br_str)
		audio.close()
		if remove_temp:
			os.remove(temp_file)
		print("Elapsed time: " + str(int(time.time()-start)) + " seconds")
		self.set_mp3_metadata()
		
	def set_mp3_metadata(self):
		""" Insert the metadata configured by the user and rename the file to {artist} - {title}.mp3 format """
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
		if self.entry.image_url != "":
			audio.tag.images.set(type_=3, img_data=None, mime_type='image/jpg', img_url=self.entry.image_url)
		audio.tag.save()
		if audio.tag.album_artist is not None and audio.tag.title is not None:
			f_new = f"{audio.tag.album_artist} - {audio.tag.title}.mp3"
		else:
			f_new = self.filename + '.mp3'
		os.rename(self.out_folder + self.filename + ".mp3", self.out_folder + f_new)
		
	def update_infolabel(self, text):
		""" Update the string of the GUI info label """
		self.info_label.configure(text=text)


class ClipEntry:
	def __init__(self, url, title="", name="", artist="", cont_artist="", album="", genre="", year="", image_url="",
	             image=None):
		self.url = url
		self.title = title
		self.name = name
		self.artist = artist
		self.cont_artist = cont_artist
		self.album = album
		self.genre = genre
		self.year = year
		self.image_url = image_url
		self.image = image
		self.filename = title + ".mp3"
	
	# Use ClipEntry.__dict__...?
	def get_dict(self):
		return {
			'url': self.url,
			'title': self.title,
			'name': self.name,
			'artist': self.artist,
			'cont_artist': self.cont_artist,
			'album': self.album,
			'genre': self.genre,
			'year': self.year,
			'image': self.image
		}

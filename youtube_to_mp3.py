from pytube import YouTube
import os
import subprocess
import time
import sys
from moviepy.editor import *
 
def get_mp4(url, fname):
	url = input("URL: ")

    # Title and Time
	print("...")
    #print(((YouTube(url)).title), "//", (int(var1)/60),"mins")
	print("...")

    # Filename specification
    # Prevents any errors during conversion due to illegal characters in name
	_filename = fname

    # Downloading
	print("Downloading....")
	YouTube(url).streams.first().download(filename=_filename)
	time.sleep(1)

    # Converting
	mp4a = "%s.mp4" % _filename
	mp3a = "%s.mp3" % _filename
	mp4 = "'%s'.mp4" % _filename
	mp3 = "'%s'.mp3" % _filename
	ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3)
	subprocess.call(ffmpeg, shell=True)
	
def get_mp3(path):
	video = VideoFileClip(path+".mp4")
	audio = video.audio # 3.
	del video
	os.remove(path+".mp4")
	audio.write_audiofile(path+".mp3")
 
 
def main():
	# Confirm the script is called with the required params
	if len(sys.argv) != 3:
		print('Usage: python video_to_mp3.py URL FILE_NAME')
		exit(1)
 
	url = sys.argv[1]
	fname = sys.argv[2]
 
	print("URL = " + url)
	print("FILE NAME = " + fname)
	get_mp4(url,fname)
	print("MP4 downloaded!")
	get_mp3(fname)
	print("MP3 downloaded!")
	time.sleep(1)
 
 
if __name__ == '__main__':
	main()
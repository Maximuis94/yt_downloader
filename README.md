# yt_downloader
GUI for extracting audio/video files from YouTube URLs

# Usage
Paste a URL in the top entry and press the Load URL button. The title displayed below the URL can be used to verify the given URL. Additionally, after loading the URL you can configure metadata that is to be inserted for the output mp3 file. The URL + metadata (if it was given) can be queued by pressing the Save / add to queue button. If you wish to view or alter previous insertions, click on the Previous entry button. The Save temp file checkbox can be checked to save temporary files, if the mp3 is extracted from a video stream, this means the source video file is saved as well. 

If you wish to download the queued URLs, press Start downloading. It will then process the queued submissions one by one. Output mp3 files are saved in the tracks/ folder and temporary files (if checked) are saved in temp/ folder of the project folder.

The queue is designed for sequentially processing a list of URLs that is configured beforehand, which may get time-consuming for larger files.

# Errors
In some cases, an AgeRestrictionError is thrown for an unknown reason. This pytube github page (https://github.com/pytube/pytube/issues/1712) contains suggestions on how to deal with this error.

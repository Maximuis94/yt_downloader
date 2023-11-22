import tkinter as tk
from tkinter import ttk

import mp3downloader as mdl
import clip_entry as ce
import time
import os
from pytube import YouTube

simulating = False


class GUI(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.frame_width, self.frame_height = 600, 600
        self.entries = []
        self.queueposition = 1
        self.artimage = None
        self.link_loaded = False


        self.root = root
        self.root.title("YouTube Downloader")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='x')

        tk.Label(self.frame, text="YouTube URL:").pack(side='left')
        self.url_input = tk.Entry(self.frame, width=60)
        self.url_input.pack(padx=10, side='left')
        self.url_input.insert(0, 'http://www.youtube.com/watch?v=dQw4w9WgXcQ')


        self.show_button = tk.Button(self.frame, text='Load URL')
        self.show_button.pack(side='left', padx=2)
        self.show_button.bind('<Button-1>', self.show_button_click)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')

        self.cliptitlelabeltext = "Title"
        self.cliptitlelabel = tk.Label(self.frame2, text=self.cliptitlelabeltext, width=50)
        self.cliptitlelabel.pack(pady=10, side='left')

        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(fill='x')

        self.namelabeltext = "Track name:"
        self.namelabel = tk.Label(self.frame3, text=self.namelabeltext, width=15)
        self.namelabel.pack(side='left')
        self.name_input = tk.Entry(self.frame3, width=40)
        self.name_input.pack(padx=10, side='left')
        self.name_input.insert(0, '')

        self.artistlabeltext = "Artist:"
        self.artistlabel = tk.Label(self.frame3, text=self.artistlabeltext, width=15)
        self.artistlabel.pack(side='left')
        self.artist_input = tk.Entry(self.frame3, width=40)
        self.artist_input.pack(padx=10, side='left')
        self.artist_input.insert(0, '')

        self.frame4 = tk.Frame(self.root)
        self.frame4.pack(fill='x')

        self.albumlabeltext = "Album:"
        self.albumlabel = tk.Label(self.frame4, text=self.albumlabeltext, width=15)
        self.albumlabel.pack(side='left')
        self.album_input = tk.Entry(self.frame4, width=40)
        self.album_input.pack(padx=10, side='left')
        self.album_input.insert(0, '')

        self.contartistlabeltext = "Contributing artist:"
        self.contartistlabel = tk.Label(self.frame4, text=self.contartistlabeltext, width=15)
        self.contartistlabel.pack(side='left')
        self.contartist_input = tk.Entry(self.frame4, width=40)
        self.contartist_input.pack(padx=10, side='left')
        self.contartist_input.insert(0, '')

        self.frame5 = tk.Frame(self.root)
        self.frame5.pack(fill='x')

        self.genrelabeltext = "Genre:"
        self.genrelabel = tk.Label(self.frame5, text=self.genrelabeltext, width=15)
        self.genrelabel.pack(side='left')
        self.genre_input = tk.Entry(self.frame5, width=40)
        self.genre_input.pack(padx=10, side='left')
        self.genre_input.insert(0, '')

        self.yearlabeltext = "Year:"
        self.yearlabel = tk.Label(self.frame5, text=self.yearlabeltext, width=15)
        self.yearlabel.pack(side='left')
        self.year_input = tk.Entry(self.frame5, width=40)
        self.year_input.pack(padx=10, side='left')
        self.year_input.insert(0, '')

        self.frame6 = tk.Frame(self.root)
        self.frame6.pack(pady=10,fill='x')

        self.artlabeltext = "Album artwork"
        self.artlabel = tk.Label(self.frame6,text=self.artlabeltext)
        self.artlabel.pack(side='left')

        self.art_upload_button = tk.Button(self.frame6, text='Upload')
        self.art_upload_button.pack(side='left', padx=4)
        self.art_upload_button.bind('<Button-1>', self.art_upload_button_click)

        self.thumbnail_art_button = tk.Button(self.frame6, text='Thumbnail')
        self.thumbnail_art_button.pack(side='left', padx=4)
        self.thumbnail_art_button.bind('<Button-1>', self.thumbnail_art_button_click)

        self.art_url_input = tk.Entry(self.frame6, width=40)
        self.art_url_input.pack(padx=10, side='left')
        self.art_url_input.insert(0, 'Insert artwork image URL here')
        
        # self.save_temp_file = tk.Checkbutton(self.frame6, text='Save temp file')
        self.remove_temp = False
        self.save_temp_file = tk.Checkbutton(self.frame6, text='Save temp file', command=self.checkbox_click, onvalue=True, offvalue=False)
        self.save_temp_file.pack(padx=5, side='right')

        self.frame7 = tk.Frame(self.root)
        self.frame7.pack(fill='x')

        self.queuepositionlabeltext = "Current position in queue: 1/0"
        self.queuepositionlabel = tk.Label(self.frame7, text=self.queuepositionlabeltext, width=25)
        self.queuepositionlabel.pack(padx=10,side='left')

        self.start_button = tk.Button(self.frame7, text='Start downloading')
        self.start_button.pack(side='left', padx=4)
        self.start_button.bind('<Button-1>', self.start_button_click)

        self.previous_button = tk.Button(self.frame7, text='Previous entry')
        self.previous_button.pack(side='right',padx=30)
        self.previous_button.bind('<Button-1>', self.previous_button_click)

        self.save_button = tk.Button(self.frame7, text='Save / add to queue')
        self.save_button.pack(side='right',padx=90)
        self.save_button.bind('<Button-1>', self.save_button_click)

    def get_root(self):
        return self.root

    def update_queue_text(self):
        self.queuepositionlabeltext = "Current position in queue: " + str(self.queueposition) + "/" + str(len(self.entries))
        self.queuepositionlabel.configure(text=self.queuepositionlabeltext)

    def read_input(self):
        artinput = self.art_url_input.get()
        if artinput == 'Insert artwork image URL here':
            artinput = ''

        return ce.ClipEntry(self.url_input.get(),title=self.cliptitlelabel.cget('text'),name=self.name_input.get(),
                             artist=self.artist_input.get(),contartist=self.contartist_input.get(),
                             album=self.album_input.get(),genre=self.genre_input.get(),year=self.year_input.get(),
                            imageurl=artinput)


    def reset_input(self):
        END=999
        self.url_input.delete(0, END)
        self.cliptitlelabeltext = ""
        self.cliptitlelabel.configure(text=self.cliptitlelabeltext)
        self.name_input.delete(0, END)
        self.artist_input.delete(0, END)
        self.contartist_input.delete(0, END)
        self.album_input.delete(0, END)
        self.genre_input.delete(0, END)
        self.year_input.delete(0, END)
        self.art_url_input.delete(0, END)
        self.artimage = None
        self.link_loaded = False

    def load_entry(self,entry):
        END = 999
        self.url_input.delete(0, END)
        self.url_input.insert(0, entry.url)
        self.cliptitlelabeltext = entry.title
        self.cliptitlelabel.configure(text=self.cliptitlelabeltext)
        self.name_input.delete(0, END)
        self.name_input.insert(0, entry.name)
        self.artist_input.delete(0, END)
        self.artist_input.insert(0, entry.artist)
        self.contartist_input.delete(0, END)
        self.contartist_input.insert(0, entry.contartist)
        self.album_input.delete(0, END)
        self.album_input.insert(0, entry.album)
        self.genre_input.delete(0, END)
        self.genre_input.insert(0, entry.genre)
        self.year_input.delete(0, END)
        self.year_input.insert(0, entry.year)
        self.art_url_input.delete(0, END)
        self.art_url_input.insert(0, entry.imageurl)
        self.artimage = None
        self.link_loaded = True

    # Tested
    # Load the URL and show the title
    # Create YouTube object from URL, extract title
    # Title is shown so the user can verify the URL
    def show_button_click(self, event):
        print("getting title of " + self.url_input.get())
        print(type(self.url_input.get()))
        yt = YouTube(self.url_input.get())
        self.cliptitlelabeltext = yt.title
        self.cliptitlelabel.configure(text=self.cliptitlelabeltext)
        self.link_loaded = True

    #TO DO
    # Open a menu to allow the user to upload album artwork
    def art_upload_button_click(self, event):
        print("ART UPLOAD CLICKED")

    #TO DO
    def thumbnail_art_button_click(self, event):
        print("THUMBNAIL ART CLICKED")

    def save_button_click(self, event):
        # Safeguard for invalid YouTube links
        if self.link_loaded is False:
            self.cliptitlelabel.configure(text="*** Please paste a YouTube URL and click Load URL ***")
            return
        # Im on the highest position in queue possible; this is a new entry
        if self.queueposition == len(self.entries)+1:
            self.entries.append(self.read_input())
        # Modify the entry on the index of queueposition-1
        else:
            self.entries[self.queueposition-1] = self.read_input()

        self.reset_input()

        # Set position to no. of entries+1 (= new entry)
        self.queueposition = len(self.entries) + 1
        self.update_queue_text()

    # Open a menu to allow the user to upload album artwork
    def previous_button_click(self, event):
        self.queueposition = self.queueposition - 1
        if self.queueposition < 1:
            self.queueposition = len(self.entries)+1
        self.queuepositionlabeltext = "Position in queue: " + str(self.queueposition) + "/" + str(len(self.entries)+1)
        if self.queueposition > len(self.entries):
            self.reset_input()
        else:
            self.load_entry(self.entries[self.queueposition-1])
        self.update_queue_text()
        print("PREVIOUS CLICKED")

    # Start button is clicked; set simulation to true and save the parameters that have been set so that they can be
    # used in the simulation
    def start_button_click(self, event):
        self.cliptitlelabeltext = "Processing queue..."
        self.cliptitlelabel.configure(text=self.cliptitlelabeltext)
        to_remove = []
        if len(self.entries) == 0:
            return
        time.sleep(1)
        #os.chdir('./Tracks/')
        for e in self.entries:
            mp3dl = mdl.MP3Downloader(file_name=e.title, entry=e, infolabel=self.cliptitlelabel)
            mp3dl.download_best_mp3(first_stream=False, remove_temp=not self.remove_temp)
            print("Downloaded MP3")
            # Execute MP3 download code
            to_remove.append(e)
        # If downloaded, remove from list
        for e in to_remove:
            self.entries.remove(e)
        self.queueposition = len(self.entries)+1
        self.update_queue_text()



    def stop_button_click(event):
        print("STOP!")
        
    def checkbox_click(self, e=None):
        self.remove_temp = not self.remove_temp

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root = gui.get_root()
    root.mainloop()
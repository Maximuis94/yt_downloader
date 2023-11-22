"""
This module contains the implementation for the graphical user interface. The GUI widgets and their callbacks are
defined here. Furthermore, this module is executable for creating the GUI.
"""

import tkinter as tk

import mp3downloader as mdl
from mp3downloader import ClipEntry
import time
from pytube import YouTube

simulating = False


class GUI(tk.Frame):
    def __init__(self, root, **kw):
        """ Implementation of the Graphical User Interface; runs on a tk loop """
        super().__init__(**kw)
        self.frame_width, self.frame_height = 700, 250
        self.entries = []
        self.queue_position = 1
        self.art_image = None
        self.link_loaded = False

        self.root = root
        self.root.title("YouTube Downloader")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='x')

        tk.Label(self.frame, text="YouTube URL:").pack(side='left')
        self.url_input = tk.Entry(self.frame, width=60)
        self.url_input.pack(padx=10, side='left')
        self.url_input.insert(0, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        self.show_button = tk.Button(self.frame, text='Load URL')
        self.show_button.pack(side='left', padx=2)
        self.show_button.bind('<Button-1>', self.show_button_click)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(fill='x')

        self.clip_title_label_text = ""
        self.clip_title_label = tk.Label(self.frame2, text=self.clip_title_label_text, width=50)
        self.clip_title_label.pack(pady=10, side='left')

        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(fill='x')

        self.name_label_text = "Track name:"
        self.name_label = tk.Label(self.frame3, text=self.name_label_text, width=15)
        self.name_label.pack(side='left')
        self.name_input = tk.Entry(self.frame3, width=40)
        self.name_input.pack(padx=10, side='left')
        self.name_input.insert(0, '')

        self.artist_label_text = "Artist:"
        self.artist_label = tk.Label(self.frame3, text=self.artist_label_text, width=15)
        self.artist_label.pack(side='left')
        self.artist_input = tk.Entry(self.frame3, width=40)
        self.artist_input.pack(padx=10, side='left')
        self.artist_input.insert(0, '')

        self.frame4 = tk.Frame(self.root)
        self.frame4.pack(fill='x')

        self.album_label_text = "Album:"
        self.album_label = tk.Label(self.frame4, text=self.album_label_text, width=15)
        self.album_label.pack(side='left')
        self.album_input = tk.Entry(self.frame4, width=40)
        self.album_input.pack(padx=10, side='left')
        self.album_input.insert(0, '')

        self.cont_artist_label_text = "Contributing artist:"
        self.cont_artist_label = tk.Label(self.frame4, text=self.cont_artist_label_text, width=15)
        self.cont_artist_label.pack(side='left')
        self.cont_artist_input = tk.Entry(self.frame4, width=40)
        self.cont_artist_input.pack(padx=10, side='left')
        self.cont_artist_input.insert(0, '')

        self.frame5 = tk.Frame(self.root)
        self.frame5.pack(fill='x')

        self.genre_label_text = "Genre:"
        self.genre_label = tk.Label(self.frame5, text=self.genre_label_text, width=15)
        self.genre_label.pack(side='left')
        self.genre_input = tk.Entry(self.frame5, width=40)
        self.genre_input.pack(padx=10, side='left')
        self.genre_input.insert(0, '')

        self.year_label_text = "Year:"
        self.year_label = tk.Label(self.frame5, text=self.year_label_text, width=15)
        self.year_label.pack(side='left')
        self.year_input = tk.Entry(self.frame5, width=40)
        self.year_input.pack(padx=10, side='left')
        self.year_input.insert(0, '')

        self.frame6 = tk.Frame(self.root)
        self.frame6.pack(pady=10, fill='x')

        self.art_label_text = "Album artwork"
        self.art_label = tk.Label(self.frame6, text=self.art_label_text)
        self.art_label.pack(side='left')

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
        self.save_temp_file = tk.Checkbutton(self.frame6, text='Save temp file', command=self.checkbox_click)
        self.save_temp_file.pack(padx=5, side='right')

        self.frame7 = tk.Frame(self.root)
        self.frame7.pack(fill='x')

        self.start_button = tk.Button(self.frame7, text='Start downloading')
        self.start_button.pack(side='left', padx=25)
        self.start_button.bind('<Button-1>', self.start_button_click)

        self.save_button = tk.Button(self.frame7, text='Save / add to queue')
        self.save_button.pack(side='left', padx=10)
        self.save_button.bind('<Button-1>', self.save_button_click)

        self.queue_position_label_text = "Current position in queue: 1/0"
        self.queue_position_label = tk.Label(self.frame7, text=self.queue_position_label_text, width=25)
        self.queue_position_label.pack(padx=10, side='left')

        self.previous_button = tk.Button(self.frame7, text='Previous entry')
        self.previous_button.pack(side='left', padx=10)
        self.previous_button.bind('<Button-1>', self.previous_button_click)

    def get_root(self):
        """ Return the root frame of the GUI """
        return self.root

    def update_queue_text(self):
        """ Update the queue position label """
        self.queue_position_label_text = f"Current position in queue: {self.queue_position}/{len(self.entries)}"
        self.queue_position_label.configure(text=self.queue_position_label_text)

    def parse_input(self):
        """ Parse input fields for mp3 metadata """
        art_input = self.art_url_input.get()
        if art_input == 'Insert artwork image URL here':
            art_input = ''

        return ClipEntry(self.url_input.get(), title=self.clip_title_label.cget('text'), name=self.name_input.get(),
                         artist=self.artist_input.get(), cont_artist=self.cont_artist_input.get(),
                         album=self.album_input.get(), genre=self.genre_input.get(), year=self.year_input.get(),
                         image_url=art_input)

    def reset_input(self):
        """ Reset input fields to their default (empty) values """
        str_end = 999
        self.url_input.delete(0, str_end)
        self.clip_title_label_text = ""
        self.clip_title_label.configure(text=self.clip_title_label_text)
        self.name_input.delete(0, str_end)
        self.artist_input.delete(0, str_end)
        self.cont_artist_input.delete(0, str_end)
        self.album_input.delete(0, str_end)
        self.genre_input.delete(0, str_end)
        self.year_input.delete(0, str_end)
        self.art_url_input.delete(0, str_end)
        self.art_image = None
        self.link_loaded = False

    def load_entry(self, entry: ClipEntry):
        """ Fill the input fields with the given ClipEntry """
        self.reset_input()
        self.url_input.insert(0, entry.url)
        self.clip_title_label_text = entry.title
        self.clip_title_label.configure(text=self.clip_title_label_text)
        self.name_input.insert(0, entry.name)
        self.artist_input.insert(0, entry.artist)
        self.cont_artist_input.insert(0, entry.cont_artist)
        self.album_input.insert(0, entry.album)
        self.genre_input.insert(0, entry.genre)
        self.year_input.insert(0, entry.year)
        self.art_url_input.insert(0, entry.image_url)
        self.art_image = None
        self.link_loaded = True

    def show_button_click(self, event):
        """ Load URL button callback -- Show URL title for user to verify the given URL """
        self.clip_title_label_text = YouTube(self.url_input.get()).title
        self.clip_title_label.configure(text=self.clip_title_label_text)
        self.link_loaded = True

    def art_upload_button_click(self, event):
        """ TO-DO --- callback for uploading image artwork (open dialogue for selecting image?) """
        print("ART UPLOAD CLICKED")
        self.art_image = None

    def thumbnail_art_button_click(self, event):
        """ TO-DO --- callback for setting thumbnail image """
        print("THUMBNAIL ART CLICKED")
        self.art_image = None

    def save_button_click(self, event):
        """ Save button callback -- Add url + metadata to queue and reset input fields """
        # Safeguard for invalid YouTube links
        if self.link_loaded is False:
            self.clip_title_label.configure(text="*** Please paste a YouTube URL and click Load URL ***")
            return
        # Im on the highest position in queue possible; this is a new entry
        if self.queue_position == len(self.entries)+1:
            self.entries.append(self.parse_input())
        # Modify the entry on the index of queueposition-1
        else:
            self.entries[self.queue_position - 1] = self.parse_input()

        self.reset_input()

        # Set position to no. of entries+1 (= new entry)
        self.queue_position = len(self.entries) + 1
        self.update_queue_text()

    # Open a menu to allow the user to upload album artwork
    def previous_button_click(self, event):
        """ Previous button callback -- Load entry from previous queue index """
        self.queue_position = self.queue_position - 1
        if self.queue_position < 1:
            self.queue_position = len(self.entries) + 1
        self.queue_position_label_text = "Position in queue: " + str(self.queue_position) + "/" + str(len(self.entries) + 1)
        if self.queue_position > len(self.entries):
            self.reset_input()
        else:
            self.load_entry(self.entries[self.queue_position - 1])
        self.update_queue_text()
        print("PREVIOUS CLICKED")

    # Start button is clicked; set simulation to true and save the parameters that have been set so that they can be
    # used in the simulation
    def start_button_click(self, event):
        """ Start button callback -- Download all queued mp3s """
        self.clip_title_label_text = "Processing queue..."
        self.clip_title_label.configure(text=self.clip_title_label_text)
        to_remove = []
        if len(self.entries) == 0:
            return
        time.sleep(1)
        #os.chdir('./Tracks/')
        for e in self.entries:
            mp3dl = mdl.MP3Downloader(file_name=e.title, entry=e, info_label=self.clip_title_label)
            mp3dl.download_mp3(first_stream=False, remove_temp=not self.remove_temp)
            print("Downloaded MP3")
            # Execute MP3 download code
            to_remove.append(e)
        # If downloaded, remove from list
        for e in to_remove:
            self.entries.remove(e)
        self.queue_position = len(self.entries) + 1
        self.update_queue_text()



    def stop_button_click(event):
        print("STOP!")
        
    def checkbox_click(self, e=None):
        self.remove_temp = not self.remove_temp


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.geometry(f"{gui.frame_width}x{gui.frame_height}")
    root = gui.get_root()
    root.mainloop()

import os
import string
import eyed3
from xmlrpc.client import Boolean
import customtkinter as ctk
from tkinter import N, X, NSEW,filedialog
import pygame
from PIL import Image

class MusicApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.geometry("600x400")
        self.root.iconbitmap(r"Icons\dvd_19098.ico")

        self.root.after(1, lambda: root.wm_state('zoomed'))

        ctk.set_appearance_mode("dark")
        self.font = "Convection"

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.grid_rowconfigure((1), weight=1, minsize=800)
        self.root.grid_columnconfigure((1, 2), weight=1, minsize=600)

        pygame.mixer.init()

        self.paused = True
        self.previous_song = None
        self.current_song = None
        self.folder_selected = None
        self.file_list = None
        self.loop = True

        self.background = ctk.CTkImage(dark_image=Image.open(r"Images\Minecraft Wallpaper.jpg"), size=(screen_width, screen_height))
        self.pause_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\pause2.png"), size=(25, 25))
        self.play_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\play2.png"), size=(25, 25))
        self.stop_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\media-playback-stop.256x256.png"), size=(25, 25))
        self.foward_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\set_foward3.png"), size=(25, 25))
        self.backward_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\step_backward_icon.png"), size=(25, 25))
        self.loop_off_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\loop.png"), size=(25,25))
        self.loop_track_list_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\loop_track_list.png"), size=(25,25))

        self.wallpaper = ctk.CTkLabel(self.root, image=self.background)
        self.wallpaper.grid(row=0, column=0, columnspan=4, rowspan=3)

        self.main_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.main_frame.grid(column=1, columnspan=2, row=1, sticky=NSEW, pady=(screen_height // 6.5), padx=screen_width // 6)


        self.main_frame.grid_rowconfigure((0), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        self.playback_and_display = ctk.CTkFrame(self.main_frame, fg_color = "white",
                                                 border_color="black", border_width=1, corner_radius=0)
        self.playback_and_display.grid(row=0, column=0, sticky=NSEW)

        self.track_list = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=0, 
                                                border_color="black", border_width=1)
        self.track_list.grid(row=0, column=1, sticky= NSEW)

        self.playback_menu = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent", 
                                          border_color="black", border_width=1, corner_radius=0)
        self.playback_menu.pack(side=ctk.TOP, anchor = ctk.NW, ipady = 20, fill = X)

        self.pause_and_play_button = ctk.CTkButton(self.playback_menu, image=self.play_icon, command=self.pause_or_play_song, 
                                                   width=80, height=50, border_color="black", border_width=1,
                                                   fg_color="transparent", text="", corner_radius=0, hover_color="lightgreen")
        self.pause_and_play_button.pack(side = ctk.LEFT, padx = (20,5))

        self.backward_button = ctk.CTkButton(self.playback_menu, image=self.backward_icon, command=lambda: self.change_track(backward = True), 
                                         width=80, height=50, border_color="black", border_width=1, 
                                         fg_color = "transparent" , text="", corner_radius=0, hover_color="lightgreen")
        self.backward_button.pack(side=ctk.LEFT , padx=5)

        self.stop_button = ctk.CTkButton(self.playback_menu, image=self.stop_icon, command=self.stop_song, 
                                         width=80, height=50, border_color="black", border_width=1, 
                                         fg_color = "transparent" , text="", corner_radius=0, hover_color="lightgreen")
        self.stop_button.pack(side=ctk.LEFT , padx=5)

        self.foward_button = ctk.CTkButton(self.playback_menu, image=self.foward_icon, command=lambda: self.change_track(foward= True), 
                                         width=80, height=50, border_color="black", border_width=1, 
                                         fg_color = "transparent" , text="", corner_radius=0, hover_color="lightgreen")
        self.foward_button.pack(side=ctk.LEFT , padx=5)

        self.loop_button = ctk.CTkButton(self.playback_menu, image=self.loop_track_list_icon, command=self.set_loop_value, 
                                         width=80, height=50, border_color="black", border_width=1, 
                                         fg_color = "transparent" , text="", corner_radius=0, hover_color="lightgreen")
        self.loop_button.pack(side=ctk.LEFT , padx=5)

        self.middle_frame = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent")
        self.middle_frame.pack(side=ctk.TOP, anchor = ctk.NW, ipady = 10, padx = 1, fill = X)

        self.load_button = ctk.CTkButton(self.middle_frame, text="Load Album or Playlist", command=self.load_tracks, 
                                        fg_color="transparent", text_color="black", 
                                        font=(self.font, 18), hover_color = "light green", 
                                        hover = True, corner_radius=0)
        self.load_button.pack(side=ctk.LEFT, padx = 20, fill = X)

        self.information_frame = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent",
                          border_color="black", border_width=1, corner_radius=0)
        self.information_frame.pack(fill = ctk.BOTH, anchor = ctk.NW, expand = True)

        self.track_title_frame = ctk.CTkFrame(self.information_frame, fg_color = "transparent",
                        corner_radius=0)
        self.track_title_frame.pack(fill = X, anchor = ctk.NW, pady = 1, padx = 1)

        self.track_artist_frame = ctk.CTkFrame(self.information_frame, fg_color = "transparent",
                        corner_radius=0)
        self.track_artist_frame.pack(fill = X, anchor = ctk.NW, pady = 1, padx = 1)

        self.track_title = ctk.CTkLabel(self.track_title_frame, text="Select a song from track file_list",
                                        fg_color="transparent", font=(self.font, 24), text_color = "Black")
        self.track_title.pack(side = ctk.LEFT, padx = 20, pady = (10,0), anchor = N)
        self.track_artist = ctk.CTkLabel(self.track_artist_frame, text="",
                                        fg_color="transparent", font=(self.font, 24), text_color = "Black")
        self.track_artist.pack(side = ctk.LEFT, padx = 20, pady = (10,0), anchor = N)
        self.track_image = ctk.CTkLabel(self.information_frame, text="", fg_color="transparent")
        self.track_image.pack(side = ctk.LEFT, padx = 20)

        self.root.after(100, self.check_for_song_end)

    def get_track_info(self, path: string = None, get_title: Boolean = None, get_album_name: Boolean = None, get_artist: Boolean = None):
        audiofile = eyed3.load(path)
        if(get_title):
            return audiofile.tag.title
        if(get_artist):
            return audiofile.tag.artist
        if(get_album_name):
            if len(audiofile.tag.album) > 50:
                return audiofile.tag.album[:50]
            return audiofile.tag.album

    def set_loop_value(self):
        if not self.loop:
            self.loop = True
            self.loop_button.configure(image = self.loop_track_list_icon)
        else:
            self.loop = False
            self.loop_button.configure(image = self.loop_off_icon)
    
    def load_tracks(self):
        folder_selected = filedialog.askdirectory()
        self.folder_selected = folder_selected
        if folder_selected:
            os.chdir(folder_selected)
            songs = os.listdir(folder_selected)
            for widget in self.track_list.winfo_children():
                widget.destroy()  
            self.file_list = []
            self.previous_song = None
            self.current_song = None
            for song in songs:
                if song.endswith(".mp3"):
                    song_title = self.get_track_info(path = rf"{folder_selected}\{song}", get_title = True)
                    song_button = ctk.CTkButton(self.track_list, text=song_title, 
                                                command=lambda s=song: self.start_song(s),
                                                fg_color="transparent", border_color = "black", border_width= 1, 
                                                text_color= "black", corner_radius=0, hover_color="lightgreen"
                                                ,font=(self.font, 12))
                    song_button.pack(fill = ctk.X)
                    self.file_list.append(song)
            images = songs
            #print(images)
            for image in images:
                if image.endswith((".png",".jpg")):
                    print(image)
                    self.track_image.configure(image=ctk.CTkImage(Image.open(image), size=(250,250)))
                    break
        self.load_button.configure(text = self.get_track_info(path = rf"{self.folder_selected}\{self.file_list[0]}", get_album_name = True))

    def start_song(self, song):
        if song != self.current_song:
            self.previous_song = self.current_song
            self.current_song = song
            if self.previous_song is None:
                self.previous_song = self.current_song
            pygame.mixer.music.load(song)
            print(f"Starting {self.current_song}")
            pygame.mixer.music.play()
            self.pause_and_play_button.configure(image=self.pause_icon)
            self.paused = False
            self.update_display(self.previous_song, self.current_song)
          

    def pause_or_play_song(self):
        print(self.paused)
        if self.paused and self.current_song:
            pygame.mixer.music.unpause()
            self.pause_and_play_button.configure(image=self.pause_icon)
            self.paused = False
        elif self.paused and self.current_song is None:
            self.start_song(self.file_list[0])
            self.pause_and_play_button.configure(image=self.pause_icon)
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.pause_and_play_button.configure(image=self.play_icon)
            self.paused = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.paused = True
        self.pause_and_play_button.configure(image=self.play_icon)
        self.update_display(self.current_song)
        self.current_song = None 

    def check_for_song_end(self):
        if pygame.mixer.music.get_busy() is False and self.paused is False and self.current_song:
            self.play_next_track()
        self.root.after(100, self.check_for_song_end)

    def play_next_track(self):
        current_title = self.get_track_info(self.current_song, get_title=True)

        current_selection = [index for index, widget in enumerate(self.track_list.winfo_children()) if widget.cget("text") == current_title]
        
        if self.loop is False and current_selection[0] == len(self.track_list.winfo_children()) - 1:
            self.stop_song(self)
            return
                                              
        if current_selection:
            next_index = (current_selection[0] + 1) % len(self.track_list.winfo_children())
        else:
            next_index = 0
        
        next_song = self.file_list[next_index]
        print(f"Switching to {next_song}")
        self.start_song(next_song)
        #print(self.file_list)
    
    def play_previous_track(self):
        current_title = self.get_track_info(self.current_song, get_title=True)
        
        current_selection = [index for index, widget in enumerate(self.track_list.winfo_children()) if widget.cget("text") == current_title]

        if self.loop is False and current_selection[0] == 0:
            self.stop_song(self)
            return
        
        if current_selection:
            next_index = (current_selection[0] - 1) % len(self.track_list.winfo_children())
        else:
            next_index = 0
        next_song = self.file_list[next_index]
        print(f"Switching to {next_song}")
        self.start_song(next_song)

    def update_display(self, previous = None, current = None):
        # print(previous)
        track_path = rf"{self.folder_selected}\{self.current_song}"
        track_title = self.get_track_info(path = track_path, get_title = True)

        self.track_title.configure(text = track_title)
        track_artist = self.get_track_info(path = track_path, get_artist = True)
        self.track_artist.configure(text = track_artist)

        if previous is None:
            return
        self.track_list.winfo_children()[self.file_list.index(previous)].configure(fg_color = "transparent")
        if current is None:
            return
        self.track_list.winfo_children()[self.file_list.index(current)].configure(fg_color = "lightgreen")

    def change_track(self, foward: Boolean = False, backward: Boolean = False):
        if foward is True:
            self.play_next_track()
        if backward is True:
            self.play_previous_track()

    
if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicApplication(root)
    root.mainloop()

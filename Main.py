import os
import customtkinter as ctk

import tkinter as tk
from tkinter import NSEW, NW, filedialog, messagebox
import pygame
from PIL import Image 

class MusicApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.geometry("600x400")

        self.root.after(0, lambda: root.wm_state('zoomed'))

        ctk.set_appearance_mode("dark")
        self.font = "Convection Bold"

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.grid_rowconfigure((1), weight = 1, minsize = 800)
        self.root.grid_columnconfigure((1,2),weight = 1, minsize = 600)


        pygame.mixer.init()

        self.paused = False
        self.current_song = None

        self.background = ctk.CTkImage(dark_image=Image.open(r"Images\Minecraft Wallpaper.jpg"), size=(screen_width, screen_height))
        self.pause_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\pause2.png"), size=(25,25))
        self.play_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\play2.png"), size=(25,25))
        self.stop_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\media-playback-stop.256x256.png"), size=(25,25))

        self.wallpaper = ctk.CTkLabel(root, image=self.background, text="")
        self.wallpaper.grid(row=0, column=0, 
                            columnspan = 4, rowspan = 3)

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.grid(column = 1, columnspan = 2,  row = 1, sticky = NSEW, pady = screen_height // 6.5,  padx = screen_width // 6)

        self.main_frame.grid_rowconfigure((1), weight = 1)
        self.main_frame.grid_columnconfigure((1,2), weight = 1)

        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.grid(row = 1, column = 1, sticky = NSEW)

        self.songs_listbox = tk.Listbox(self.main_frame, selectmode=ctk.SINGLE, bg="black", fg="white", font=('arial', 12))
        self.songs_listbox.grid(row = 1, column = 2, sticky= NSEW)
        self.songs_listbox.bind("<<ListboxSelect>>", self.on_song_select)
        self.songs_listbox.bind("<Return>", self.on_song_select)

        self.playback_menu = ctk.CTkFrame(self.left_frame)
        self.playback_menu.pack(side=ctk.TOP, pady=10, anchor=NW)

        self.pause_and_play_button = ctk.CTkButton(self.playback_menu, image=self.play_icon, command=self.pause_or_play_song, 
                                                   width=50, height=50, border_color="black", border_width=1,
                                                   fg_color="grey", text="")
        self.pause_and_play_button.pack(side=ctk.LEFT, padx=5)

        self.stop_button = ctk.CTkButton(self.playback_menu, image=self.stop_icon, command=self.stop_song, 
                                         width=50, height=50, border_color="black", border_width=1,
                                         text="")
        self.stop_button.pack(side=ctk.LEFT, padx=5)

        self.load_button = ctk.CTkButton(self.left_frame, text="Load Songs", command=self.load_songs, fg_color="green", text_color="white", font=('arial', 12))
        self.load_button.pack(side=ctk.BOTTOM, pady=10)


    def load_songs(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            os.chdir(folder_selected)
            songs = os.listdir(folder_selected)
            self.songs_listbox.delete(0, ctk.END)
            for song in songs:
                if song.endswith(".mp3"):
                    self.songs_listbox.insert(ctk.END, song)

    def on_song_select(self, event):
        selected_song = self.songs_listbox.get(ctk.ACTIVE)
        if selected_song:
            self.start_song(selected_song)

    def start_song(self, song):
        try:
            if song != self.current_song:
                self.current_song = song
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.pause_and_play_button.configure(image=self.pause_icon)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_or_play_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
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
        self.current_song = None

        
if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicApplication(root)
    root.mainloop()
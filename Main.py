from email.mime import image
import os
import tkinter as tk
from tkinter import ANCHOR, BOTH, filedialog, messagebox
import tkinter
from turtle import Screen, screensize
import pygame
from PIL import ImageTk, Image 

class MusicApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.state('zoomed')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        pygame.mixer.init()

        self.paused = False
        self.current_song = None

        background = Image.open(r".\Wallpapers\Minecraft Wallpaper.jpg")
        background.resize((screen_width,screen_height))
        self.background = ImageTk.PhotoImage(background)

        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background)

        self.main_frame = tk.Frame(root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.songs_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=30, height=15)
        self.songs_listbox.pack(expand=True, fill=tk.BOTH)

        self.playback_menu = tk.Frame(self.left_frame)
        self.playback_menu.pack(side=tk.TOP, pady=10)

        self.play_button = tk.Button(self.playback_menu, text="Play", command=self.play_song, bg="blue", fg="white", font=('arial', 12))
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.playback_menu, text="Pause/Unpause", command=self.pause_song, bg="yellow", fg="black", font=('arial', 12))
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.playback_menu, text="Stop", command=self.stop_song, bg="red", fg="white", font=('arial', 12))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(self.right_frame, text="Load Songs", command=self.load_songs, bg="green", fg="white", font=('arial', 12))
        self.load_button.pack(side=tk.BOTTOM, pady=10)

    def load_songs(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            os.chdir(folder_selected)
            songs = os.listdir(folder_selected)
            self.songs_listbox.delete(0, tk.END)
            for song in songs:
                if song.endswith(".mp3"):
                    self.songs_listbox.insert(tk.END, song)
    def play_song(self):
        try:
            selected_song = self.songs_listbox.get(tk.ACTIVE)
            if selected_song != self.current_song:
                self.current_song = selected_song
                pygame.mixer.music.load(selected_song)
                pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def pause_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.current_song = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApplication(root)
    root.mainloop()
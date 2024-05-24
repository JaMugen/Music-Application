import os
import customtkinter as ctk
from tkinter import BOTH, X, NSEW, NW, Y, filedialog, messagebox
import pygame
from PIL import Image

class MusicApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.geometry("600x400")

        self.root.after(0, lambda: root.wm_state('zoomed'))

        ctk.set_appearance_mode("dark")
        self.font = "Convection"

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.grid_rowconfigure((1), weight=1, minsize=800)
        self.root.grid_columnconfigure((1, 2), weight=1, minsize=600)

        pygame.mixer.init()

        self.paused = False
        self.current_song = None
        self.manually_paused = False

        self.background = ctk.CTkImage(dark_image=Image.open(r"Images\Minecraft Wallpaper.jpg"), size=(screen_width, screen_height))
        self.pause_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\pause2.png"), size=(25, 25))
        self.play_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\play2.png"), size=(25, 25))
        self.stop_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\media-playback-stop.256x256.png"), size=(25, 25))

        self.wallpaper = ctk.CTkLabel(self.root, image=self.background, text="Now Playing", 
                                      font=(self.font, 28), text_color="White")
        self.wallpaper.grid(row=0, column=0, columnspan=4, rowspan=3)

        self.main_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.main_frame.grid(column=1, columnspan=2, row=1, sticky=NSEW, pady=(screen_height // 6.5), padx=screen_width // 6)


        self.main_frame.grid_rowconfigure((0), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        self.playback_and_display = ctk.CTkFrame(self.main_frame, fg_color = "white",
                                                 border_color="black", border_width=1, corner_radius=0)
        self.playback_and_display.grid(row=0, column=0, sticky=NSEW)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=0)
        self.scrollable_frame.grid(row=0, column=1, sticky= NSEW)

        self.playback_menu = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent", 
                                          border_color="black", border_width=1, corner_radius=0)
        self.playback_menu.pack(side=ctk.TOP, anchor = ctk.NW, ipady = 20, fill = X)

        self.pause_and_play_button = ctk.CTkButton(self.playback_menu, image=self.play_icon, command=self.pause_or_play_song, 
                                                   width=80, height=50, border_color="black", border_width=1,
                                                   fg_color="transparent", text="", corner_radius=0, hover_color="lightgreen")
        self.pause_and_play_button.pack(side = ctk.LEFT, padx = (20,0))

        self.stop_button = ctk.CTkButton(self.playback_menu, image=self.stop_icon, command=self.stop_song, 
                                         width=80, height=50, border_color="black", border_width=1, 
                                         fg_color = "transparent" , text="", corner_radius=0, hover_color="lightgreen")
        self.stop_button.pack(side=ctk.LEFT , padx=5)

        self.middle_frame = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent")
        self.middle_frame.pack(side=ctk.TOP, anchor = ctk.NW, ipady = 10, padx = 1, fill = X)
        self.load_button = ctk.CTkButton(self.middle_frame, text="Load Album or Playlist", command=self.load_songs, 
                                        fg_color="transparent", text_color="black", 
                                        font=(self.font, 24), hover = False)
        self.load_button.pack(side=ctk.LEFT, padx = 14, fill = X)

        self.bottom_frame = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent",
                          border_color="black", border_width=1, corner_radius=0)
        self.bottom_frame.pack(fill = BOTH, anchor = ctk.NW, expand = True)

        self.root.after(100, self.check_for_song_end)

    def load_songs(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            os.chdir(folder_selected)
            songs = os.listdir(folder_selected)
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()  
            for song in songs:
                if song.endswith(".mp3"):
                    song_button = ctk.CTkButton(self.scrollable_frame, text=song, 
                                                command=lambda s=song: self.start_song(s),
                                                fg_color="transparent", border_color = "black", border_width= 1, 
                                                text_color= "black", corner_radius=0, hover_color="lightgray")
                    song_button.pack(fill=ctk.X)

    def on_song_select(self, event):
        selected_song = event.widget.cget("text")
        if selected_song:
            self.start_song(selected_song)

    def start_song(self, song):
        try:
            if song != self.current_song:
                self.current_song = song
                pygame.mixer.music.load(song)
                print(f"Starting {self.current_song}")
                pygame.mixer.music.play()
                self.pause_and_play_button.configure(image=self.pause_icon)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_or_play_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.pause_and_play_button.configure(image=self.pause_icon)
            self.paused = False
            self.manually_paused = False
        else:
            pygame.mixer.music.pause()
            self.pause_and_play_button.configure(image=self.play_icon)
            self.paused = True

    def stop_song(self):
        pygame.mixer.music.stop()
        self.paused = True
        self.pause_and_play_button.configure(image=self.play_icon)
        self.current_song = None

    def check_for_song_end(self):
        if not pygame.mixer.music.get_busy() and not self.paused and self.current_song:
            self.play_next_song()
        self.root.after(100, self.check_for_song_end)

    def play_next_song(self):
        current_selection = [index for index, widget in enumerate(self.scrollable_frame.winfo_children()) if widget.cget("text") == self.current_song]
        if current_selection:
            next_index = (current_selection[0] + 1) % len(self.scrollable_frame.winfo_children())
        else:
            next_index = 0
        next_song_button = self.scrollable_frame.winfo_children()[next_index]
        next_song = next_song_button.cget("text")
        print(f"Switching to {next_song}")
        self.start_song(next_song)
        
if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicApplication(root)
    root.mainloop()

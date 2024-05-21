import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

class MusicApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.geometry("400x350")

        pygame.mixer.init()

        self.paused = False
        self.current_song = None

        self.songs_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg="")
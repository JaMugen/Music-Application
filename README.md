# Music Player Notes

## Install Magick(Was not used yet.)

Allows for the converting of large image formats down to ico format.

> [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows)

## Setup python virtual environment

### pygame

```python
python -m pip install pygame
```

### customtkinter

```python
python -m pip install customtkinter
```

### PIL

```python
python -m pip install pillow
```

### eyeD3

``` python

python -m pip install eyeD3

```

eyeD3 allows for the reading and writing of mp3 files information. The script uses this to read the title of the track, the artist, and the album name.

## Class Music Application

Define the application as a class, so it can be ran as an instance. Best wasy to  manage the methods or functions of the application.

```python
def __init__(self, root):
        self.root = root
        self.root.title("Music Application")
        self.root.geometry("600x400")

        self.root.after(1, lambda: root.wm_state('zoomed'))

        ctk.set_appearance_mode("dark")
        self.font = "Convection"
```

The class is initialized with init this is where the layout and public variables are defined/created. First pass the object as itself this allows for the use of instance variables. Then pass root which is the CTk class of the ctk module, allowing for the application to inherit from the CTk class, which is the initialized application. Then assign the root to a public variable. The title, which is displayed at the top of the window is defined. Afterword, the size of the initialized window is set as 600 x 400(W x H). Following that is a call to the after method which waits a period of time before calling a function.

### Lambda

> It calls lambda which is a method that allows for the passing of arguments are methods to be called from it. Used when needing to cal more than one defined method or passing arguments.

Lastly, some appearance adjustments are made to set the app to the dark mode if not set it is defined by the system to either be light or dark. Then the font is set to Convection, which must be installed on system to be used.

```python
screen_width = self.root.winfo_screenwidth()
screen_height = self.root.winfo_screenheight()
```

Defines the width and height of the screen as local variables to the init method.

```python
self.root.grid_rowconfigure((1), weight=1, minsize=800)
self.root.grid_columnconfigure((1, 2), weight=1, minsize=600)
```

Here the row and grid are bing configured. For starters the minimum size is being set to 800 and 600 respectively. Back to the first parameter, this is assigning which row or column is being configured. For example column 1 and 2 are being configured. The weight parameter determines which row gets priority on screen size.

### Instance Variables

```python

pygame.mixer.init()

self.paused = True
self.previous_song = None
self.current_song = None
self.folder_selected = None
self.file_list = None
self.loop = True

```

Moving from top to bottom, first there is a variable for if the song is paused. The next two define are the file names of the previous song played and the current one. Moving on to the next variable is for name of the folder the music is stored in, or the playlist/album folder. The file list is the list of the name of the song files in the folder. Lastly, the final variable checks if the music player is set to loop the playlist/album.

```python

self.background = ctk.CTkImage(dark_image=Image.ope(r"Images\Minecraft Wallpaper.jpg"), size=(screen_width, screen_height))
self.pause_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\pause2.png"), size=(25, 25))
self.play_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\play2.png"), size=(25, 25))
self.stop_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\media-playback-stop.256x256.png"), size=(25, 25))
self.foward_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\set_foward3.png"), size=(25, 25))
self.backward_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\step_backward_icon.png"), size=(25, 25))
self.loop_off_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\loop.png"), size=(25,25))
self.loop_track_list_icon = ctk.CTkImage(dark_image=Image.open(r"Icons\loop_track_list.png"), size=(25,25))

```

Instance variables for images to be used in the application. CTK assigns the image type for the application setting and resizes the image. The dark_image is given the image by using open method of Image, passing in the path to the image.

## Application GUI

``` python

self.wallpaper = ctk.CTkLabel(self.root, image=self.background)
self.wallpaper.grid(row=0, column=0, columnspan=4, rowspan=3)

```

The first defined widget of the application is a label. The label is set to span the entirety of the root grid which is 3 rows by 4 columns. For the application the root is the window itself. The label is assigned an image as it is going to be a wallpaper for the application.

``` python

self.main_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.main_frame.grid(column=1, columnspan=2, row=1, sticky=NSEW, pady=(screen_height //5), padx=screen_width // 6)


self.main_frame.grid_rowconfigure((0), weight=1)
self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

```

Frames are like the application window, they can house widgets inside them, having their own grid. Here the main frame for the music player or in other words the functional space is defined. The frame is place in the center row and spans the middle two columns of the root grid. It size is defined as a division of the screen dimensions. The main frame also gets its own grid which is 1 row and 2 columns. They are set to a self named category called equal. When parts of a grid are apart of the same uniform group there dimensions are made equal.

### Sticky 

Finally, the parameter sticky defines to which sides of the grid space should the widget stick two, in this case it is sticking to all directions. CustomTkinter uses compass directions to define sides.

``` python

self.playback_and_display = ctk.CTkFrame(self.main_frame, fg_color = "white",
                                                 border_color="black", border_width=1, corner_radius=0)
self.playback_and_display.grid(row=0, column=0, sticky=NSEW)

self.track_list = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=0, 
                                        border_color="black", border_width=1)
self.track_list.grid(row=0, column=1, sticky= NSEW)

```

Here each halves of the main frame is getting their own frames. The left side is getting the playback and display halve, which has the playback menu and song information. On the other side, is the list of tracks for the playlist/album.

``` python

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

```

For the left side the top of this halve is the playback menu consisting of, backward button, pause button, foward button, stop button, and loop button. Here the buttons are using the pack method inside the frame instead of the grid method. Here the pack method works well with padding to get hte buttons to appear next to each other inside there own frame. The command parameter passes the method that triggers when the button is clicked. The foward and backward buttons use the lambda function to pass arguments to the "change_track" method.

``` python

self.middle_frame = ctk.CTkFrame(self.playback_and_display, fg_color = "transparent")
self.middle_frame.pack(side=ctk.TOP, anchor = ctk.NW, ipady = 10, padx = 1, fill = X)

self.load_button = ctk.CTkButton(self.middle_frame, text="Load Album or Playlist", command=self.load_tracks, 
                                fg_color="transparent", text_color="black", 
                                font=(self.font, 18), hover_color = "light green", 
                                hover = True, corner_radius=0)
self.load_button.pack(side=ctk.LEFT, padx = 20, fill = X)

```

Here is the middle frame for storing the clickable text for loading the music folder.

``` python

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

```

Finally, there is the information portion that displays the track name, the artist, and an image for the track. Additionally, there is a call to after method to a method for checking for track end.

``` python

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

```

The first method defined is gor getting the track information. This method is not used by the app, but is called within methods for getting specific track information. The parameters ask for the path to the tack which can be provided using the folder selected variable and track name. Then the rest is boolean variables for checking which piece of information wanted. The method will only return a string of one piece of information.

``` python

def set_loop_value(self):
    if not self.loop:
        self.loop = True
        self.loop_button.configure(image = self.loop_track_list_icon)
    else:
        self.loop = False
        self.loop_button.configure(image = self.loop_off_icon)

```

This method sets the loop instance variable and change the button icon to match the value. It is called when the loop button is pressed.

``` python

def load_tracks(self):
    folder_selected = filedialog.askdirectory()
    self.folder_selected = folder_selected
    if folder_selected:
        os.chdir(folder_selected)
        songs = os.listdir(folder_selected)
        for widget in self.track_list.winfo_children():
            widget.destroy()  
        self.file_list = []
        self.song_title_to_song = {}
        self.song_to_song_title = {}
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
    self.load_button.configure(text = self.get_track_info(path = rf"{folder_selected}\{self.file_list[0]}", get_album_name = True))

```

Using "filedialog" imported from tkinter a select file request is prompted for the user. Once they ed a directory or a folder that folder will be assigned to the local "folder_selected" variable. The instance variable will then be assigned this value. Now if the folder was properly assigned to the variable, so not null it will continue the rest of the method. Using the operating system standard library for python the directory is changed to the one selected. Once inside the names of content of the n directory is assigned as a list. Before doing any assigned their is some cleaning that is done first which includes destroying the widgets inside "track_list" frame, the file list, and the tracked songs. With the cleaning done there is a for loop for that goes through each item of the directory. If the item is a mp3 a button will be created for it that is placed in the "track_list" frame. The button allows for the tracks in the track list to be clicked on to play it. Once all the songs are placed in the track list the directory is looped through again to assign an image for the playlist/album. At the end the text for the clickable text is now changed to the name of the playlist/album. Currently is uses the first track as the means fo getting the name so it will not work properly for playlists. This method could be improved to only use one loop for making the track list, getting an image, and checking if tracks come from different albums. If the tracks come from different albums the text could be assigned the name of the directory instead of the album value for the mp3.

``` python

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

```

Method called for starting the track.
The method will run if the song passed to it is not the same as the current song.
First the method will change the values of the previous song and current song.
Then the song is loaded into pygame mixer and played.
The method concludes with setting the variables to proper values and updating the display to give song details.

``` python

def stop_song(self):
        pygame.mixer.music.stop()
        self.paused = True
        self.pause_and_play_button.configure(image=self.play_icon)
        self.update_display(self.current_song)
        self.current_song = None

```

When the stop button is pressed the method tells the mixer to stop the music and unassign the song.

``` python

def check_for_song_end(self):
        if pygame.mixer.music.get_busy() is False and self.paused is False and self.current_song:
            self.play_next_track()
        self.root.after(100, self.check_for_song_end)

```

A recursive function for checking if track in the mixer is no longer playing. When that is true it calls the method for playing the next track.

``` python

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

```

These two methods are for changing the track that is playing. One moves to the track ahead and the other moves to the track before.
The title of the track is assigned to a variable. It then looks for the index of the button the track is assigned to. Then uses a modulus calculation to get the next track and will loop if the track exceeds the bounds. 
The new index is used to fetch the song file name from the file list and plays it.


``` python

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

```

The last two functions are updating the song information and calling one of the two methods for changing tracks. To start with the last of the two the method takes a boolean value as  parameter which is passed when the function is called by th foward button or backward button.
The foward button will send true for foward and the backward button will assign backward as true. Now for the previous method updating the display, this method handles changing the information of the labels present in the display frame.
This method will set get the track title and artist and assign it using the information passed by the parameters. The method also updates the track list by changing the current song to lightgreen when it is selected and the previous song to transparent. The method will early return if the values or null.

``` python

if __name__ == "__main__":
    root = ctk.CTk()
    app = MusicApplication(root)
    root.mainloop()

```

For the main function of the script the class will be used to build an application instance by initializing the application with customtkinter then passing the root into the class call.
After that the "mainloop" method is called on the root or application so that it is constantly refreshing. This allows for the script to react to user input.
## Resources

> [https://www.tutorialspoint.com/python/python_gui_programming.htm](https://www.tutorialspoint.com/python/python_gui_programming.htm)
> [https://docs.python.org/3/library/tkinter.html#a-hello-world-program](https://docs.python.org/3/library/tkinter.html#a-hello-world-program)
> [https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton](https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton)

### Supplementary Resources

> [https://www.tutorialspoint.com/python/index.htm](https://www.tutorialspoint.com/python/index.htm)
> [https://code.visualstudio.com/docs/python/python-tutorial#_next-steps](https://code.visualstudio.com/docs/python/python-tutorial#_next-steps)

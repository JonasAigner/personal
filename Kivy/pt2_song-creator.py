from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
import gc
import random
import time
import os

class RootWidget(PageLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        self.playtime = 0
        self.page = 0
        #self.size_hint_y = 0.5
        
        self.help_screen = Label(text="[b]Help[/b]\nFor creating a new song just tap 'New Song'")
        self.help_screen.text_size = (self.help_screen.width, None)
        self.help_screen.height = self.help_screen.texture_size[1]
        self.home_screen = Label(text="Welcome",font_size="75sp")
        self.add_widget(self.home_screen)
        RootWidget.home_screen = self.home_screen
 
        
    def update(self, dt):    
        self.playtime += dt
            
        

class BoxWidget_page1(BoxLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(BoxWidget_page1, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        #self.cols = 5
        self.orientation = "vertical"
        
        self.songname_input = TextInput(font_size="15sp",size_hint_y=0.3)
        self.add_widget(self.songname_input)
        
        self.button_new = Button(
            text="New",font_size="25sp")
        self.add_widget(self.button_new)
        
        self.button_new.bind(on_press = self.action_new)
        
    def action_new(self, dummy):
        song_number = 0
        for root, folder, files in os.walk("custom_songs"):
            for f in files:
                if f == self.songname_input.text+".json" or f == self.songname_input.text+str(song_number)+".json":
                    song_number += 1
        if song_number == 0:
            song_number = ""
        BoxWidget_page1.song_filename = self.songname_input.text+str(song_number)+".json"
        BoxWidget_page1.songfile = open(os.path.join("custom_songs", BoxWidget_page1.song_filename), "w")
        print("[*]: Created new file: '{}'".format(BoxWidget_page1.song_filename))
        
class GridWidget_page2(GridLayout):
    song_code = ""
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(GridWidget_page2, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        self.cols = 2
        self.noten = []
        GridWidget_page2.noten = self.noten
        
        self.button_addnote = Button(
            text="add note",font_size="20sp",background_color=(0.3,0.3,0.3,1))
        self.add_widget(self.button_addnote)
        
        self.n_input = TextInput(font_size="15sp")
        self.add_widget(self.n_input)
        
        self.button_notetype = Button(
            text="note-type",font_size="20sp",background_color=(0.3,0.3,0.3,1))
        self.add_widget(self.button_notetype)
        
        self.note_input = TextInput(font_size="15sp")
        self.add_widget(self.note_input)
        
        self.button_savenote = Button(
            text="save note",font_size="20sp",background_color=(0.3,0.3,0.3,1))
        self.add_widget(self.button_savenote)
        
        self.button_removenote = Button(
            text="delete note",font_size="20sp",background_color=(0.3,0.3,0.3,1))
        self.add_widget(self.button_removenote)
        
        self.button_addnote.bind(on_press = self.action_addnote)
        self.button_notetype.bind(on_press = self.action_notetype)
        self.button_savenote.bind(on_press = self.action_savenote)
        self.button_removenote.bind(on_press = self.action_removenote)
        
    def action_addnote(self, dummy):
        if self.n_input.text == "":
            pass
        else:
            try:
                if self.noten[0] == "(":
                    self.noten.append(".")
                    self.noten.append(self.n_input.text)
            except IndexError:
                self.noten.append("(")
                self.noten.append(self.n_input.text)
            print("[*]: Added note '{}' to notes".format(self.n_input.text))
            self.n_input.text = ""
            print("[*]: Notes: {}".format(self.noten))
            
    def action_savenote(self, dummy):
        # ~ if self.noten.__class__.__name__ == "str":
            # ~ self.song_code += self.noten
        # ~ elif self.noten.__class__.__name__ == "list":
            # ~ for n in self.noten:
                # ~ self.song_code.append(n)
        if list(self.noten)[-1] == ">;" or list(self.noten)[-1] == ">,":
            for n in list(self.noten):
                self.song_code += n
        else:
            notenlist = list(self.noten)
            notenlist.append(",")
            for n in notenlist:
                GridWidget_page2.song_code += n
        print("[*]: Saved notes {} to the song code".format(self.noten))
        self.noten = []
        
    def action_removenote(self, dummy):
        print("[*]: Removed notes {}".format(self.noten))
        self.noten = []
            
    def action_notetype(self, dummy):
        newnoten = []
        if len(self.noten) == 2:
            newnoten = str(self.noten[1])
            if self.note_input.text == "normal":
                newnoten += "[L]"
            elif self.note_input.text == "long3":
                newnoten += "[K]"
            elif self.note_input.text == "long5":
                newnoten += "[J]"
            elif self.note_input.text == "long9":
                newnoten += "[I]"
            elif self.note_input.text == "long4":
                newnoten += "[JK]"
            elif self.note_input.text == "space":
                newnoten = "[U]"
        else:
            self.noten.append(")")
            for n in self.noten:
                newnoten.append(n)
            print(newnoten)
            if self.note_input.text == "normal":
                newnoten.append("[L]")
            # ------------------------------------
            elif self.note_input.text == "long3":
                newnoten.append("[K]")
            # ------------------------------------
            elif self.note_input.text == "long5":
                newnoten.append("[J]")
            # ------------------------------------
            elif self.note_input.text == "long9":
                newnoten.append("[I]")
            # ------------------------------------
            elif self.note_input.text == "long4":
                newnoten.append("[JK]")
            # ------------------------------------
            elif self.note_input.text == "space":
                newnoten = "[U]"
            # ------------------------------------
            elif self.note_input.text == "double" and len(newnoten) == 5:
                newnoten = []
                newnoten.append("5<")
                newnoten.append(self.noten[1])
                newnoten.append("[M]")
                for n in self.noten[3:]:
                    if n == "." or n == ")":
                        continue
                    newnoten.append(",")
                    newnoten.append(n)
                    newnoten.append("[M]")
                newnoten.append(">")
            # ------------------------------------
            elif self.note_input.text == "big":
                newnoten = []
                newnoten.append("3<")
                newnoten.append(self.noten[1])
                newnoten.append("[M]")
                for n in self.noten[3:]:
                    if n == "." or n == ")":
                        continue
                    newnoten.append(",")
                    newnoten.append(n)
                    newnoten.append("[M]")
                newnoten.append(">;")
            # ------------------------------------
            elif self.note_input.text == "slide":
                newnoten = []
                newnoten.append("8<")
                newnoten.append(self.noten[1])
                newnoten.append("[N]")
                for n in self.noten[3:]:
                    if n == "." or n == ")":
                        continue
                    newnoten.append(",")
                    newnoten.append(n)
                    newnoten.append("[N]")
                newnoten.append(">")
        print("[*]: Tryed to apply type '{}'".format(self.note_input.text))
        self.note_input.text = ""
        print("[*]: Notes are now {}".format(newnoten))
        self.noten = newnoten
            
class GridWidget_page3(GridLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(GridWidget_page3, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        self.cols = 2
        self.actual_id = 1
        
        self.button_makestart = Button(
            text="Start",font_size="20sp",background_color=(0,0,0,1))
        self.add_widget(self.button_makestart)
        
        self.startspeed_input = TextInput(text="Change bpm / speed.\n 100 = 6 Tiles/second",font_size="15sp")
        self.add_widget(self.startspeed_input)
        
        self.button_addstar = Button(
            text="add checkpoint",font_size="20sp",background_color=(0,0,0,1))
        self.add_widget(self.button_addstar)
        
        self.speed_input = TextInput(text="Change bpm / speed.\n 100 = 6 Tiles/second",font_size="15sp")
        self.add_widget(self.speed_input)
        
        
        
        self.button_addstar.bind(on_press = self.action_addstar)
        self.button_makestart.bind(on_press = self.action_makestart)
        
    def action_addstar(self, dummy):
        new = ""
        songlist = list(GridWidget_page2.song_code)
        if songlist[-1] == ",":
            songlist[-1] = ""
        for n in songlist:
            new += n
        GridWidget_page2.song_code = new
        songlist = []
        if self.actual_id == 3:
            songlist.append('"],"id":' + str(self.actual_id) + '}],"audition":{"end":[0,27],"start":[0,0]}}')
            print("[*]: Added End with id ", self.actual_id)
        elif self.actual_id > 3:    
            print("[*]: No more checkpoints can be added")
        else:
            songlist.append('"],"id":' + str(self.actual_id) +'},{"bpm":' + str(self.speed_input.text) + ',"baseBeats":0.5,"scores":["')
            print("[*]: Added Checkpoint with id ", self.actual_id)
        self.actual_id += 1
        for n in songlist:
            GridWidget_page2.song_code += n
    
    def action_makestart(self,dummy):
        if list(GridWidget_page2.song_code) == []:
            GridWidget_page2.song_code += '{"baseBpm":' + str(self.startspeed_input.text) + ',"musics":[{"bpm":' + str(self.startspeed_input.text) + ',"BaseBeats":0.5,"scores":["'
        else:
            newcode = ""
            newcode += '{"baseBpm":' + str(self.startspeed_input.text) + ',"musics":[{"BaseBeats":0.5,"scores":["'
            for n in list(GridWidget_page2.song_code):
                newcode += n
            GridWidget_page2.song_code = newcode
        print("[*]: Added start with {} baseBpm".format(self.startspeed_input.text))
        

class GridWidget_page4(GridLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(GridWidget_page4, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        self.cols = 2
        
        self.button_savesong = Button(
            text="Save",font_size="40sp",background_color=(1,1,1,1),color=(0.1,0.1,0.1,1))
        self.add_widget(self.button_savesong)
        
        
        self.button_savesong.bind(on_press = self.action_savesong)
        
    def action_savesong(self, dummy):
        BoxWidget_page1.songfile.write(GridWidget_page2.song_code)
        BoxWidget_page1.songfile.close() 
        print("[*]: Saved song")       
        
class MainApp(App):

    def build(self):
        self.root = root = RootWidget()
        self.box1 = BoxWidget_page1()
        self.grid2 = GridWidget_page2()
        self.grid3 = GridWidget_page3()
        self.grid4 = GridWidget_page4()
        self.root.add_widget(self.box1)
        self.root.add_widget(self.grid3)
        self.root.add_widget(self.grid2)
        self.root.add_widget(self.grid4)
        # ~ self.box1.add_widget(self.grid1)
        root.bind(size=self._update_rect, pos=self._update_rect)
        # ~ with root.canvas.before:
            # ~ Color(0, 1, 0, 1) # green; colors range from 0-1 not 0-255
            # ~ self.rect = Rectangle(size=root.size, pos=root.pos)
        # ~ with root.canvas:
            # ~ Color(1, 0, 0, 1)
            #self.line = Line(points=[root.center_x*8,root.center_y-root.center_y,root.center_x*8,root.center_y*12],width=5)
        Clock.schedule_interval(root.update, 1.0/30.0)
        return root

    def _update_rect(self, instance, value):
        pass


if __name__ == '__main__':
    MainApp().run()

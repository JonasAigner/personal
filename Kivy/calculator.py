from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import gc
import random

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout

        self.player1_height = 0.1
        self.player2_height = 0.1
        self.player1_list = []
        self.player2_list = []
        self.player1_destroying = False
        self.player2_destroying = False
        self.playtime = 0
        self.end_of_effect1 = 0
        self.end_of_effect2 = 0
        self.flash_points1 = []
        self.flash_points2 = []
        self.orientation = "vertical"
        #self.size_hint_y = 0.5
        
        self.screen1 = Label(text="",font_size="40sp")
        self.add_widget(self.screen1)
        RootWidget.screen1 = self.screen1
 
        
    def update(self, dt):
        #Clock.schedule_interval(self.clean_memory, 10)    
        self.playtime += dt
        #if self.end_of_effect1 + 0.1 or self.end_of_effect2 + 0.1 >= self.playtime:
            #self.renew_screen()
   
class GridWidget(GridLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(GridWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout

        self.player1_height = 0.1
        self.player2_height = 0.1
        self.player1_list = []
        self.player2_list = []
        self.player1_destroying = False
        self.player2_destroying = False
        self.playtime = 0
        self.end_of_effect1 = 0
        self.end_of_effect2 = 0
        self.flash_points1 = []
        self.flash_points2 = []
        self.cols = 5


        self.zahl1 = Button(
            text="1",font_size="25sp")
        self.add_widget(self.zahl1)
        
        self.zahl2 = Button(
            text="2",font_size="25sp")
        self.add_widget(self.zahl2) 
        
        self.zahl3 = Button(
            text="3",font_size="25sp")
        self.add_widget(self.zahl3)
        
        self.symbol1 = Button(
            text="+",color=(0,1,0,1),font_size="25sp")
        self.add_widget(self.symbol1)
        
        self.symbol2 = Button(
            text="-",color=(0,1,0,1),font_size="25sp")
        self.add_widget(self.symbol2)
        
        self.zahl4 = Button(
            text="4",font_size="25sp")
        self.add_widget(self.zahl4) 
        
        self.zahl5 = Button(
            text="5",font_size="25sp")
        self.add_widget(self.zahl5)
        
        self.zahl6 = Button(
            text="6",font_size="25sp")
        self.add_widget(self.zahl6)
        
        self.symbol3 = Button(
            text="*",color=(0,1,0,1),font_size="25sp")
        self.add_widget(self.symbol3)
        
        self.symbol4 = Button(
            text="/",color=(0,1,0,1),font_size="25sp")
        self.add_widget(self.symbol4)
        
        self.zahl7 = Button(
            text="7",font_size="25sp")
        self.add_widget(self.zahl7)
        
        self.zahl8 = Button(
            text="8",font_size="25sp")
        self.add_widget(self.zahl8) 
        
        self.zahl9 = Button(
            text="9",font_size="25sp")
        self.add_widget(self.zahl9)
        
        self.zahl0 = Button(
            text="0",font_size="25sp")
        self.add_widget(self.zahl0)
        
        self.symbol5 = Button(
            text=".",color=(0,1,0,1),font_size="40sp")
        self.add_widget(self.symbol5)
        
        self.symbol6 = Button(
            text="AC",color=(1,0,0,1),font_size="25sp")
        self.add_widget(self.symbol6)
        
        self.symbol7 = Button(
            text="Del",color=(1,0,0,1),font_size="25sp")
        self.add_widget(self.symbol7)
        
        self.symbol8 = Button(
            text="(",color=(1,1,0,1),font_size="25sp")
        self.add_widget(self.symbol8)
        
        self.symbol9 = Button(
            text=")",color=(1,1,0,1),font_size="25sp")
        self.add_widget(self.symbol9)
        
        self.symbol10 = Button(
            text="=",color=(0,1,0,1),font_size="25sp")
        self.add_widget(self.symbol10)
        
        self.zahl0.bind(on_press = self.action0)
        self.zahl1.bind(on_press = self.action1)
        self.zahl2.bind(on_press = self.action2)
        self.zahl3.bind(on_press = self.action3)
        self.zahl4.bind(on_press = self.action4)
        self.zahl5.bind(on_press = self.action5)
        self.zahl6.bind(on_press = self.action6)
        self.zahl7.bind(on_press = self.action7)
        self.zahl8.bind(on_press = self.action8)
        self.zahl9.bind(on_press = self.action9)
        self.symbol1.bind(on_press = self.action_plus)
        self.symbol2.bind(on_press = self.action_minus)
        self.symbol3.bind(on_press = self.action_mal)
        self.symbol4.bind(on_press = self.action_divi)
        self.symbol5.bind(on_press = self.action_punkt)
        self.symbol6.bind(on_press = self.action_ac)
        self.symbol7.bind(on_press = self.action_del)
        self.symbol8.bind(on_press = self.action_auf)
        self.symbol9.bind(on_press = self.action_zu)
        self.symbol10.bind(on_press = self.action_gleich)
        
    def action0(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "0"
    def action1(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "1"
    def action2(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "2"
    def action3(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "3"
    def action4(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "4"
    def action5(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "5"
    def action6(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "6"
    def action7(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "7"
    def action8(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "8"
    def action9(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "9"
    def action_plus(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "+"
    def action_minus(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "-"
    def action_mal(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "*"
    def action_divi(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "/"
    def action_punkt(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "."
    def action_ac(self, dummy):
        RootWidget.screen1.text = ""
    def action_del(self, dummy):
        textlist = list(RootWidget.screen1.text)
        textlist[-1] = ""
        new = ""
        for x in textlist:
            new += x
        RootWidget.screen1.text = new
    def action_auf(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += "("
    def action_zu(self, dummy):
        if len(list(RootWidget.screen1.text)) < 35:
            RootWidget.screen1.text += ")"
    def action_gleich(self, dummy):
        rechnung = RootWidget.screen1.text
        try:
            result = str(eval(rechnung))
        except:
            result = "Error"
        RootWidget.screen1.text = result
        
    
        
class MainApp(App):

    def build(self):
        self.root = root = RootWidget()
        self.grid1 = GridWidget()
        self.root.add_widget(self.grid1)
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
        #self.rect.pos = instance.pos
        #self.rect.size = instance.size
if __name__ == '__main__':
    MainApp().run()

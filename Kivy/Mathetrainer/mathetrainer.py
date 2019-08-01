from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
import gc
import random
import questionai
import time
            

class RootWidget(BoxLayout):
    age = 0
    start_time = 0
    end_time = 0
    history = []
    IX = 0
    run = True
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout
        self.orientation = "vertical"
        #self.size_hint_y = 1
       
        
        self.screen1 = Label(text=Game.task,font_size="40sp")
            #,text_size=(self.width, None))
        self.add_widget(self.screen1)
        #self.screen1.height = 200
        RootWidget.screen1 = self.screen1
        
        RootWidget.historyscreen = Label(size_hint_y=0.5)

        
    def update(self, dt):
        if RootWidget.run:
            MainApp.game1.game()
            xtime = RootWidget.age - RootWidget.start_time
            with RootWidget.historyscreen.canvas:
                Color(random.random(),random.random(),random.random(),1)
                Rectangle(pos=(0, Window.height-40), size=(int(xtime*20), 40))
            RootWidget.age += dt
        
   
class GridWidget(GridLayout):
    
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(GridWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout
        self.cols = 2
        
        try:
            self.remove_widget(self.answer1)
            self.remove_widget(self.answer2)
            self.remove_widget(self.answer3)
            self.remove_widget(self.answer4)
        except AttributeError:
            pass
            
        self.results = []
        for result in Game.results:
            self.results.append(result)
        random.shuffle(self.results)
        
        
        self.answer1 = Button(
            text=str(self.results[0]),font_size="50sp")
        self.add_widget(self.answer1)
        
        self.answer2 = Button(
            text=str(self.results[1]),font_size="50sp")
        self.add_widget(self.answer2)
        
        self.answer3 = Button(
            text=str(self.results[2]),font_size="50sp")
        self.add_widget(self.answer3)
        
        self.answer4 = Button(
            text=str(self.results[3]),font_size="50sp")
        self.add_widget(self.answer4)
        
        
        self.answer1.bind(on_press = self.action1)
        self.answer2.bind(on_press = self.action2)
        self.answer3.bind(on_press = self.action3)
        self.answer4.bind(on_press = self.action4)
        
    def paint_history(self, button1):
        RootWidget.end_time = RootWidget.age
        RootWidget.history.append(RootWidget.end_time - RootWidget.start_time)
        if RootWidget.IX + 20 > Window.width:
            RootWidget.history = RootWidget.history[1:]
            with RootWidget.historyscreen.canvas:
                RootWidget.historyscreen.canvas.clear()
                for rank,o in enumerate(RootWidget.history):
                    Color(1,1,0,1)
                    Rectangle(pos=(rank*21, 0), size=(20,int(o*10)))
                    
        else:   
            with RootWidget.historyscreen.canvas:
                Color(1,1,0,1)
                Rectangle(pos=(RootWidget.IX, 0), size=(20,int(RootWidget.history[-1]*20)))
                RootWidget.IX += 21
        RootWidget.screen1.text = "Richtig"
        button1.color = (0,1,0,1)
    
    def action1(self, dummy):
        if RootWidget.run == False:
            MainApp.game1.restart_game()
        else:
            if self.answer1.text == str(Game.results[0]):
                self.paint_history(self.answer1)
            else:
                RootWidget.screen1.text = "Falsch"
    def action2(self, dummy):
        if RootWidget.run == False:
            MainApp.game1.restart_game()
        else:
            if self.answer2.text == str(Game.results[0]):
                self.paint_history(self.answer2)
            else:
                RootWidget.screen1.text = "Falsch"
    def action3(self, dummy):
        if RootWidget.run == False:
            MainApp.game1.restart_game()
        else:
            if self.answer3.text == str(Game.results[0]):
                self.paint_history(self.answer3)
            else:
                RootWidget.screen1.text = "Falsch"
    def action4(self, dummy):
        if RootWidget.run == False:
            MainApp.game1.restart_game()
        else:
            if self.answer4.text == str(Game.results[0]):
               self.paint_history(self.answer4)
            else:
                RootWidget.screen1.text = "Falsch"


class BoxWidget(BoxLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(BoxWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout
        self.orientation = "horizontal"
        self.size_hint_y = 0.5
        
        self.pointscreen = Label(text="Points: {}".format(Game.points),font_size="40sp")
        self.add_widget(self.pointscreen)
        BoxWidget.pointscreen = self.pointscreen
        
        self.failscreen = Label(text="",font_size="40sp",color=(1,0,0,1))
        self.add_widget(self.failscreen)
        BoxWidget.failscreen = self.failscreen      
    
        
class Game():
    def __init__(self):
        self.counter = 0
        self.points = 0
        Game.points = self.points
        self.fails = 0
        self.difficulty = None
        self.get_task()
        
    def restart_game(self):
        self.points = 0
        self.fails = 0
        RootWidget.run = True
        MainApp.box1.pointscreen.text = "Points: 0"
        MainApp.box1.failscreen.text = ""
        self.get_task()
        RootWidget.screen1.text = self.task
        MainApp.grid1.__init__()
        RootWidget.historyscreen.canvas.clear()

    def get_task(self):
        if self.difficulty == None:
            if self.points <= 3:
                self.task_list = questionai.generate_question(3)
            elif self.points <= 6:
                self.task_list = questionai.generate_question(7)
            elif self.points <= 9:
                self.task_list = questionai.generate_question(10)
            elif self.points > 9:
                self.task_list = questionai.generate_question(30)   
        elif self.difficulty.__class__.__name__ == "int":
            self.task_list = questionai.generate_question(self.difficulty)
        self.results = questionai.solver(self.task_list)
        task = ""
        for x in self.task_list:
            task += str(x)
        self.task = task
        Game.task = self.task
        Game.results = self.results
        RootWidget.start_time = RootWidget.age
        
            
    def game(self):
        if RootWidget.screen1.text == "Richtig":
            self.counter += 1
            if self.counter >= 40:
                self.counter = 0
                self.get_task()
                displaytext = ""
                for i in self.task:
                    displaytext += i + " "
                RootWidget.screen1.text = displaytext#self.task
                MainApp.grid1.__init__()
                self.points += 1
                MainApp.box1.pointscreen.text = "Points: " + str(self.points)
        elif RootWidget.screen1.text == "Falsch":
            self.counter += 1
            if self.counter >= 40:
                self.counter = 0
                self.fails += 1
                if self.fails == 3:
                    self.task = "R"
                    RootWidget.screen1.text = "Game Over"
                    RootWidget.run = False
                else:
                    self.get_task()
                    RootWidget.screen1.text = self.task
                    MainApp.grid1.__init__()
                    MainApp.box1.failscreen.text += "X"

class MainApp(App):
    
    def build(self):
        self.game1 = Game()
        MainApp.game1 = self.game1
        self.root = root = RootWidget()
        self.grid1 = GridWidget()
        MainApp.grid1 = self.grid1
        self.box1 = BoxWidget()
        MainApp.box1 = self.box1
        self.root.add_widget(self.grid1)
        self.root.add_widget(self.box1)
        self.root.add_widget(RootWidget.historyscreen)
        root.bind(size=self._update_rect, pos=self._update_rect)
        self.game1.game()
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

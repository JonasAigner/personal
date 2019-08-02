from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
import requests
import shutil
#import urllib.request



class MyGui(GridLayout):

    sources = []
    thumbs = []
    i = -1

    def __init__(self, **kwargs):
        super(MyGui, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='insert Pixabay image search words here and press ENTER',  
                             halign= 'left',     valign= 'middle'))
        self.search = TextInput(multiline=False)
        self.add_widget(self.search)
        #self.add_widget(Label(text='password'))
        #self.password = TextInput(password=True, multiline=False)
        #self.add_widget(self.password)
        self.result = Label(text="nothing")
        self.add_widget(self.result)
        self.pic = Image(source=None) #source="https://pixabay.com/get/57e5d0454e55ac14f6da8c7dda79367d1338d9e0534c704c732b7cd69e4acc5e_640.jpg")
        #self.pic2 = AsyncImage(source=None)
        self.add_widget(self.pic)
        #self.add_widget(self.pic2)
        self.button_left = Button(text="previous")
        self.button_right = Button(text="next")
        self.imagename = Label(text="")
        self.add_widget(self.button_left)
        self.add_widget(self.button_right)
        self.add_widget(self.imagename)
        #self.go_button = Button(text="go!")
        #self.add_widget(self.go_button)
        #self.go_button.bind(on_press = self.go)
        self.search.bind(on_text_validate=self.go)
        self.button_right.bind(on_press = self.next_image)
        self.button_left.bind(on_press = self.previous_image)
        
    def next_image(self, event):
        MyGui.i += 1
        if MyGui.i >= len(MyGui.sources):
            MyGui.i = 0
        self.pic.source = MyGui.sources[MyGui.i].split("/")[-1]
        self.imagename.text = MyGui.sources[MyGui.i]
        self.result.text = "image {} of {}: ".format(MyGui.i+1, len(MyGui.sources))
        
    def previous_image(self, event):
        MyGui.i -= 1
        if MyGui.i < 0 :
            MyGui.i = len(MyGui.sources) -1
        
        self.pic.source = MyGui.sources[MyGui.i].split("/")[-1]
        self.imagename.text = MyGui.sources[MyGui.i]
        
        self.result.text = "image {} of {}: ".format(MyGui.i+1, len(MyGui.sources))
        

    #def update(self, dt):
    #    self.result.text = "images: "+ str(len(MyGui.sources))

    def go(self, event):
        MyGui.i = -1
        MyGui.sources = []
        
        #print(self.search.text)
        text = "https://pixabay.com/api/?key=INSERT_YOUR_PIXABAY_KEY_HERE&q=" + self.search.text + "&image_type=photo"
        r = requests.get(text)
        data = r.json()
        #print(r.headers['content-type'])
        #print(r.text)
        print(data)
        with open("json.txt", "w") as jsonfile:
            for key, value in data.items():
                jsonfile.write(str(key))
                jsonfile.write("\n")
                jsonfile.write(str(value))
                jsonfile.write("\n")
        self.result.text = str(len(data["hits"])) + " images found"
        for h in data["hits"]:
            image_url = h["webformatURL"]
            thumb_url = h["previewURL"]
            print("I now try to download {}".format(image_url))
            #self.imagename.text += image_url + "\n"
            MyGui.sources.append(image_url)
            #MyGui.thumbs.append(thumb_url)
            #self.pic2.source=thumb_url
            #html = open(local_f
            #local_filename, headers = urllib.request.urlretrieve(image_url)
            #html = open(local_filename)
            #html.close() 
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                filename = image_url.split("/")[-1]
                #print("converting", image_url, "to filename:", filename)
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                self.pic.source = filename 
                    
        

     

class MyApp(App):

    def build(self):
        root = MyGui()
        #Clock.schedule_interval(root.update, 1.0/30.0)
        return root


if __name__ == '__main__':
    MyApp().run()

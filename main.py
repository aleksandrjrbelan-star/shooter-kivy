from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreenManager
from kivy import platform
from kivy.core.window import Window
from kivy.core import Clock
from kivymd.image import Image
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp,sp
from kivymd.uix.widget import MDWidget

FPS = 60
BULLET_SPEED = dp(10)
SHIP_SPEED = dp(10)

class MainScreen(MDScreen):
    ...

class GameScreen(MDScreen):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_interval(self.update,1/FPS)

        self.eventkeys = {}
        self.bullets = []
    def update(self):
        for key in self.eventkeys:
            if self.eventkeys[key] == True:
                if key == 'left':
                    self.move_left()
                if key == 'right':
                    self.move_right()
                if key == 'up':
                    self.shot()
                    self.eventkeys[key] = False
    def pressKey(self, key):
        self.eventkeys[key] = True

    def releaseKey(self, key):
        self.eventkeys[key] = False

    def move_left(self):
        self.ids.ship.pos[0] -= SHIP_SPEED
    
    def move_right(self):
        self.ids.ship.pos[0] += SHIP_SPEED

    def shot(self):
        shot = Shot(self.ids.ship.centr_x,self.ids.ship.centr_y)
        self.bullets.append(shot)
        self.ids.front.add_widget(shot)

class ShooterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'Orange'

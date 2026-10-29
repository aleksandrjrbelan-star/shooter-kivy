from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreenManager
from kivy import platform
from kivy.core.window import Window, Keyboard
from kivy.core import Clock
from kivymd.image import Image
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp,sp
from kivymd.uix.widget import MDWidget

from kivy.uix.image import image
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import MDDialog

from random import randint

DIR_UP = 1
DIR_DOWN = -1


FPS = 60
BULLET_SPEED = dp(10)
SHIP_SPEED = dp(10)

class MainScreen(MDScreen):
    ...

class Ship(Image):
    def __init__(self,direction=DIR_UP,**kwargs):
        super().__init__(**kwargs)
        self.direction = direction
    def moveL(self):
        self.pos[0] -= SHIP_SPEED
    def moveR(self):
        self.pos[0] += SHIP_SPEED
    def shot(self):
        shot = Shot(self.direction)
        shot.center_x = self.center_x
        shot.y = self.top if self.direction == DIR_UP else self.y - self.height

        self.parent.parent.parent.parent.bullets.append(shot)
        self.parent.add_widget(shot)
    def update(self):
        pass

class Pl_Ship(Ship):
    def __init__(self,**kwargs):
        super().__init__(direction=DIR_UP,**kwargs)

    def update(self,keys):
        for key in keys:
            if keys[key] == True:
                if key == 'left' and self.center_x > 0
                    self.moveL()
                if key == 'right' and self.center_x < Window.width
                    self.moveR()
                if key == 'shoot':
                    self.shot()
                    keys[key] = False

class Enemy_Ship(Ship):
    def __init__(self,*args,**kwargs):
        super().__init__(direction=DIR_DOWN*args,**kwargs)
        self.frame = 0
    def update(self):
        super().update()
        self.pos[1] -= dp(3)
        if self.frame % 100 == 0:
            self.shot()
        self.frame += 1

class GameScreen(MDScreen):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_interval(self.update,1/FPS)

        self.eventkeys = {}
        self.bullets = []

        self.ship = self.ids.ship
        self.enemyShips = []

        self.pauseMenu = None

        Window.bind(On_key_down = self._on_key_down)
        Window.bind(On_key_up = self._on_key_up)
    def _on_key_down(self,window,keycode,*args,**kwargs):
        key = key if (kye := Keyboard.keycode_to_string(window,keycode) ) != 'spacebar' else "shot"
        self.eventkeys[key] = True
    def _on_key_down(self,window,keycode,*args,**kwargs):
        key = key if (kye := Keyboard.keycode_to_string(window,keycode) ) != 'spacebar' else "shot"
        self.eventkeys[key] = False
    def update(self,dt):
        self.ship.update(self.eventkeys)

        self.time_last_spawn += dt
        if self.time_last_spawn >= self.spawn_delay:
            self.spawn_enemy()
            self.time_last_spawn = 0
        
        for ship in self.enemyShips:
            ship.update()
            if ship.top < 0:
                self.remove_enemy(ship)
            
            if ship.collide_widget(self.ship):
                self.game_over()
        self.manage_bullets()

    def game_over(self):
        self.updateEvent.cancel()

        for ship in self.enemyShips:
            self.remove_enemy(ship)
            

        self.manager.current = "game_over"

    def check_collision(self,bullet):
        if bullet.owner == self.ship:
            for enemy in self.enemyShips:
                if bullet.collide_widget(enemy):
                    self.remove_enemy(enemy)
                    self.remove_bullet(bullet)
        else:
            if bullet.collide_widget(self.ship):
                self.remove_bullet(bullet)
                self.game_over()

    def remove_enemy(self,enemy):
        self.enemyShips.remove(ship)
        self.ids.front.remove_widget(ship)

    def remove_bullet(self,bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            self.ids.front.remove_widget(bullet)

    def manage_bullets(self):
        for bullet in self.bullets:
            bullet.y += BULLET_SPEED * bullet.direction
            self.check_collision(bullet)
            if bullet.y > Window.height or bullet.top < 0:
                self.ids.front.remove_widget(bullet)
                self.bullets.remove(bullet)
    def on_enter(self,*args):
        self.updateEvent = Clock.schedule_interval(self.update, 1 / FPS)
        return super().on_enter(*args)

    def spawn_enemy(self,):
        ship = Enemy_Ship(DIR_DOWN)
        ship.pos = (randint(0,int(Window.size[0]-ship.size[0])),Window.size[1])
        self.EnemyShips.append(ship)

        self.ids.front.add_widget(self.EnemyShips[-1])

        
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

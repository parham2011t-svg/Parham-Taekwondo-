from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.utils import platform
import random

# PARHAM TAEKWONDO - Android/Kivy prototype
# Converted from the original Pygame sample.
# Controls: LEFT, RIGHT, JUMP, KICK, BLOCK.

GAME_W, GAME_H = 480.0, 800.0
GROUND = 620.0

class Fighter:
    def __init__(self, x, hp, face):
        self.x = float(x)
        self.y = GROUND
        self.vy = 0.0
        self.hp = hp
        self.face = face
        self.attack = 0
        self.cooldown = 0
        self.hit = False
        self.block = False

class FightCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Fighter(100, 100, 1)
        self.enemy = Fighter(370, 100, -1)
        self.held = set()
        self.tapped = set()
        self.game_over = False
        self.winner = ""
        self._touch_controls = {}
        Clock.schedule_interval(self.update_game, 1.0 / 60.0)
        self.bind(pos=self.redraw, size=self.redraw)
        self.redraw()

    def reset_game(self):
        self.player = Fighter(100, 100, 1)
        self.enemy = Fighter(370, 100, -1)
        self.game_over = False
        self.winner = ""
        self.redraw()

    def start_attack(self, f):
        if f.cooldown <= 0:
            f.attack = 15
            f.cooldown = 35
            f.hit = False

    def update_attack(self, f, target):
        if f.attack > 0:
            f.attack -= 1
            if abs(f.x - target.x) < 105 and not f.hit:
                target.hp = max(0, target.hp - (2 if target.block else 12))
                f.hit = True
        if f.cooldown > 0:
            f.cooldown -= 1

    def update_game(self, dt):
        if self.game_over:
            return
        p, e = self.player, self.enemy
        p.face = 1 if p.x < e.x else -1
        e.face = -p.face

        if "LEFT" in self.held:
            p.x -= 4
        if "RIGHT" in self.held:
            p.x += 4
        if "JUMP" in self.tapped and p.y >= GROUND:
            p.vy = -15
        if "KICK" in self.tapped:
            self.start_attack(p)
        p.block = "BLOCK" in self.held

        for f in (p, e):
            f.vy += 0.7
            f.y += f.vy
            if f.y >= GROUND:
                f.y = GROUND
                f.vy = 0

        distance = abs(e.x - p.x)
        if distance > 85:
            e.x -= 2 * e.face
        if distance < 115 and e.cooldown <= 0:
            self.start_attack(e)

        self.update_attack(p, e)
        self.update_attack(e, p)
        p.x = max(25, min(GAME_W - 25, p.x))
        e.x = max(25, min(GAME_W - 25, e.x))

        if p.hp <= 0:
            self.game_over, self.winner = True, "CPU WINS!"
        elif e.hp <= 0:
            self.game_over, self.winner = True, "PARHAM WINS!"

        self.tapped.clear()
        self.redraw()

    def _map(self, x, y):
        # Game coordinates are 480x800 with origin at top-left.
        sx = self.width / GAME_W
        sy = self.height / GAME_H
        return self.x + x * sx, self.y + self.height - y * sy

    def _rect(self, x, y, w, h):
        px, py = self._map(x, y + h)
        return (px, py, w * self.width / GAME_W, h * self.height / GAME_H)

    def draw_text(self, text, x, y, size=17, color=(1, 1, 1, 1)):
        # Lightweight canvas text using Kivy Label is handled in widget overlay.

    def draw_fighter(self, f, rgb):
        x, y = f.x, f.y
        sx, sy = self.width / GAME_W, self.height / GAME_H
        px, py = self._map(x, y)
        Color(235/255, 190/255, 150/255, 1)
        Ellipse(pos=(px-19*sx, py+81*sy), size=(38*sx, 38*sy))
        Color(*rgb)
        RoundedRectangle(pos=(px-17*sx, py+25*sy), size=(34*sx, 55*sy), radius=[dp(7)])
        Color(20/255, 20/255, 25/255, 1)
        Rectangle(pos=(px-18*sx, py+35*sy), size=(36*sx, 7*sy))

        Color(*rgb)
        if f.attack > 0:
            Line(points=[px, py+30*sy, px+f.face*65*sx, py+40*sy], width=dp(8))
        else:
            Line(points=[px, py+30*sy, px-13*sx, py], width=dp(7))
            Line(points=[px, py+30*sy, px+13*sx, py], width=dp(7))
        Line(points=[px, py+70*sy, px+f.face*28*sx, py+48*sy], width=dp(5))
        Line(points=[px, py+70*sy, px-f.face*23*sx, py+55*sy], width=dp(5))
        if f.block:
            Color(1, 210/255, 50/255, 1)
            Ellipse(pos=(px+f.face*25*sx-9*sx, py+56*sy), size=(18*sx, 18*sy))

    def redraw(self, *args):
        self.canvas.clear()
        if self.width <= 0 or self.height <= 0:
            return
        sx, sy = self.width / GAME_W, self.height / GAME_H
        with self.canvas:
            # Temporary training hall background
            Color(175/255, 205/255, 220/255, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(225/255, 225/255, 215/255, 1)
            Rectangle(pos=self._rect(0, 0, GAME_W, GROUND))
            Color(60/255, 130/255, 165/255, 1)
            Rectangle(pos=self._rect(0, GROUND, GAME_W, GAME_H-GROUND))
            Color(90/255, 160/255, 185/255, 1)
            for x in range(0, int(GAME_W), 60):
                a = self._map(x, GROUND)
                b = self._map(x, GAME_H)
                Line(points=[a[0], a[1], b[0], b[1]], width=dp(1))
            Color(1, 1, 1, 1)
            a, b = self._map(0, GROUND), self._map(GAME_W, GROUND)
            Line(points=[a[0], a[1], b[0], b[1]], width=dp(2))

            # Health bars
            Color(1, 1, 1, 1)
            Rectangle(pos=self._rect(25, 35, 180, 18))
            Rectangle(pos=self._rect(275, 35, 180, 18))
            Color(45/255, 100/255, 230/255, 1)
            Rectangle(pos=self._rect(25, 35, 180*self.player.hp/100, 18))
            Color(220/255, 45/255, 55/255, 1)
            Rectangle(pos=self._rect(275, 35, 180*self.enemy.hp/100, 18))
            Color(20/255, 20/255, 25/255, 1)
            Rectangle(pos=self._rect(25, 35, 180, 2))
            Rectangle(pos=self._rect(25, 51, 180, 2))
            Rectangle(pos=self._rect(25, 35, 2, 18))
            Rectangle(pos=self._rect(203, 35, 2, 18))
            Rectangle(pos=self._rect(275, 35, 180, 2))
            Rectangle(pos=self._rect(275, 51, 180, 2))
            Rectangle(pos=self._rect(275, 35, 2, 18))
            Rectangle(pos=self._rect(453, 35, 2, 18))

            self.draw_fighter(self.player, (45/255, 100/255, 230/255, 1))
            self.draw_fighter(self.enemy, (220/255, 45/255, 55/255, 1))

class TaekwondoApp(App):
    def build(self):
        self.root_layout = FloatLayout()
        self.game = FightCanvas(size_hint=(1, 1))
        self.root_layout.add_widget(self.game)

        # HUD labels
        self.p_label = Label(text="PARHAM", color=(0.15,0.3,0.9,1),
                             font_size="15sp", size_hint=(None,None),
                             pos_hint={"x":0.04,"top":0.99}, size=(dp(100),dp(28)))
        self.cpu_label = Label(text="CPU", color=(0.9,0.15,0.2,1),
                               font_size="15sp", size_hint=(None,None),
                               pos_hint={"right":0.96,"top":0.99}, size=(dp(65),dp(28)))
        self.root_layout.add_widget(self.p_label)
        self.root_layout.add_widget(self.cpu_label)

        controls = [
            ("LEFT", 0.02, 0.02, 0.14, 0.10),
            ("RIGHT", 0.18, 0.02, 0.14, 0.10),
            ("JUMP", 0.38, 0.02, 0.15, 0.10),
            ("KICK", 0.58, 0.02, 0.18, 0.10),
            ("BLOCK", 0.79, 0.02, 0.19, 0.10),
        ]
        self.buttons = {}
        for name, x, y, w, h in controls:
            btn = Button(text=name, size_hint=(w,h), pos_hint={"x":x,"y":y},
                         background_normal="", background_color=(0.22,0.27,0.36,0.95),
                         color=(1,1,1,1), font_size="13sp")
            btn.bind(on_press=lambda instance, n=name: self.press_control(n))
            btn.bind(on_release=lambda instance, n=name: self.release_control(n))
            self.root_layout.add_widget(btn)
            self.buttons[name] = btn

        self.status = Label(text="", color=(1,0.85,0.2,1), font_size="24sp",
                            bold=True, size_hint=(1,None), height=dp(60),
                            pos_hint={"center_x":0.5,"center_y":0.52})
        self.root_layout.add_widget(self.status)

        self.restart_btn = Button(
            text="RESTART",
            size_hint=(0.42, 0.075),
            pos_hint={"center_x": 0.5, "center_y": 0.42},
            opacity=0,
            disabled=True,
            background_normal="",
            background_color=(0.12, 0.14, 0.19, 0.96),
            color=(1, 1, 1, 1),
            font_size="16sp"
        )
        self.restart_btn.bind(on_press=self.restart_game)
        self.root_layout.add_widget(self.restart_btn)

        Clock.schedule_interval(self.refresh_hud, 1/15)
        return self.root_layout

    def press_control(self, name):
        self.game.held.add(name)
        self.game.tapped.add(name)

    def release_control(self, name):
        self.game.held.discard(name)

    def refresh_hud(self, dt):
        if self.game.game_over:
            self.status.text = self.game.winner + "\nTAP TO RESTART"
        else:
            self.status.text = ""
        # Restart by tapping status area after match ends.

    def on_touch_down(self, touch):
        if self.game.game_over:
            self.game.reset_game()
            self.status.text = ""
        return super().on_touch_down(touch)

    def on_pause(self):
        return True

if __name__ == "__main__":
    TaekwondoApp().run()

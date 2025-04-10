import time

from kivy.uix.screenmanager import Screen, SlideTransition
import random
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from utils.U_button_to_show import u_btn_img, u_btn_left
from kivy.graphics import Color, Rectangle
import sqlite3
from kivy.core.audio import SoundLoader

bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()

name_s_p_s = 'Spell'
bk_c.execute(f'select * from now_book_word')
res = bk_c.fetchall()
if len(res) != 0:
    now_book = res[0][0]
    bk_c.execute(f'select * from {now_book}')
    al_wd = bk_c.fetchall()
else:
    al_wd = []


class S_p_s(Screen):
    def __init__(self, **kwargs):
        super(S_p_s, self).__init__(**kwargs)
        self.name = name_s_p_s
        self.al_wd = al_wd
        self.bind(size=self.update)
        self.i_n = 0
        with self.canvas:
            Color(1, 1, 1, .9)
            self.r = Rectangle(pos=(0, 0), size=(self.width, self.height))

    def on_pre_enter(self, *args):
        bk_c.execute("""create table if not exists now_book_word(now_book text,now_word text)""")
        bk_c.execute(f'select * from now_book_word')
        res = bk_c.fetchall()
        if len(res) != 0:
            now_book = res[0][0]
            bk_c.execute(f'select * from {now_book}')
            al_wd = bk_c.fetchall()
        else:
            al_wd = []
        self.al_wd = al_wd
        if len(self.al_wd) != 0:
            self.random_list = random.sample(range(0, len(self.al_wd)), len(self.al_wd))
            self.s_n_w = self.al_wd[int(self.random_list[0])][0]
        self.update()

    def update(self, *args):
        self.clear_widgets()
        self.r.size = (self.width, self.height)
        self.new_w(self.i_n)

    def new_w(self, i):
        self.bk_home = u_btn_img(
            img_p="picture/p10.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.back_home
        )
        self.add_widget(self.bk_home)
        if len(self.al_wd) != 0:
            with self.canvas:
                Color(1, 1, 1, 1)
                self.rect = Rectangle(pos=(0, 0), size=(self.size[0], self.size[1] * 0.1))
            self.list_b_1 = Button(
                text='提示',
                background_color=(1, 1, 1, 0.03),
                size=(self.size[1] * 0.1, self.size[1] * 0.1),
                pos_hint={'x': 0.07, 'y': 0},
                size_hint=(None, None),
                color=(0, 0, 0, 1),
                on_press=self.s_snd
            )
            self.add_widget(self.list_b_1)

            self.list_b_2 = Button(
                text='答案',
                background_color=(1, 1, 1, 0.03),
                size=(self.size[1] * 0.1, self.size[1] * 0.1),
                pos_hint={'x': 0.404, 'y': 0},
                size_hint=(None, None),
                color=(0, 0, 0, 1),
                on_press=self.s_ans
            )
            self.add_widget(self.list_b_2)

            self.list_b_3 = Button(
                text='确认',
                background_color=(1, 1, 1, 0.03),
                size=(self.size[1] * 0.1, self.size[1] * 0.1),
                pos_hint={'x': 0.738, 'y': 0},
                size_hint=(None, None),
                color=(0, 0, 0, 1),
                on_press=self.ok
            )
            self.add_widget(self.list_b_3)

            all_chinese = self.al_wd[int(self.random_list[i])][1].split('|')
            ch = ''
            for i in all_chinese:
                ch += i + '\n'
            self.word_label = u_btn_left(
                text=ch,
                background_color=(1, 1, 1, 0),
                size_hint=(None, None),
                size=(self.size[0], self.size[1] * .3),
                font_size='20sp',
                pos_hint={'x': 0, 'y': .6},
                color=(0, 0, 0),
            )
            self.add_widget(self.word_label)

            self.textinput = TextInput(
                size_hint=(.8, .055),
                pos_hint={'x': .1, 'y': .45},
                hint_text='请输入单词的拼写',
                background_color=(1, 1, 1, 1),
                background_normal='',
                background_active='',
                border=(10, 10, 10, 10),
                font_size='30sp',
                multiline=False,
            )
            self.add_widget(self.textinput)

    def back_home(self, *args):
        self.parent.transition = SlideTransition(direction='down')
        self.parent.current = 'Home'

    def s_snd(self, *args):
        path = 'sound_path/' + self.al_wd[int(self.random_list[self.i_n])][0] + '.mp3'
        sound = SoundLoader.load(path)
        sound.play()

    def s_ans(self, *args):
        self.textinput.text = self.al_wd[int(self.random_list[self.i_n])][0]

    def ok(self, *args):
        if self.textinput.text == self.al_wd[int(self.random_list[self.i_n])][0]:
            self.i_n += 1
            self.i_n = self.i_n % len(self.al_wd)
            self.clear_widgets()
            self.new_w(self.i_n)
        else:
            self.textinput.background_color = (1, 0, 0, 1)

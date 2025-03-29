from kivy.uix.screenmanager import Screen, SlideTransition
import random
from utils.U_button_to_show import u_btn_img, u_btn_left
from kivy.graphics import Color, Rectangle
import sqlite3
from kivy.core.audio import SoundLoader

bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()
bk_c.execute("""create table if not exists now_book_word(now_book text,now_word text)""")
bk_c.execute(f'select * from now_book_word')
res = bk_c.fetchall()
if len(res) != 0:
    now_book = res[0][0]
    bk_c.execute(f'select * from {now_book}')
    al_wd = bk_c.fetchall()
else:
    al_wd =[]
name_s_c_s = 'Select'


class S_c_s(Screen):
    def __init__(self, **kwargs):
        super(S_c_s, self).__init__(**kwargs)
        self.name = name_s_c_s
        self.al_wd = al_wd
        if len(self.al_wd) != 0:
            self.random_list = random.sample(range(0, len(self.al_wd)), len(self.al_wd))
            self.s_n_w = self.al_wd[int(self.random_list[0])][0]
        self.bind(size=self.update)
        self.i_n = 0

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
        self.update(self.i_n)

    def update(self, *args):
        with self.canvas:
            Color(1, 1, 1, .9)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
        self.new_w(self.i_n)

    def new_w(self, i_n):
        self.bk_home = u_btn_img(
            img_p="picture/p10.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.back_home
        )
        self.add_widget(self.bk_home)
        if len(self.al_wd)>=4:
            rand_a = random.sample(range(0, len(self.al_wd)), 4)
            if self.random_list[i_n] in rand_a:
                random.shuffle(rand_a)
            else:
                rand_a.append(self.random_list[i_n])
                rand_a = rand_a[1:]
                random.shuffle(rand_a)
        else:
            rand_a = []
        if len(rand_a) != 0:

            self.word_label = u_btn_left(
                text=self.al_wd[int(self.random_list[i_n])][0],
                background_color=(1, 1, 1, 0),
                size_hint=(None, None),
                size=(self.size[0], self.size[1] * .3),
                font_size='50sp',
                pos_hint={'x': 0, 'y': .6},
                color=(0, 0, 0),
            )
            self.add_widget(self.word_label)
            the_h = [0.1, 0.25, 0.4, 0.55]
            index = 0
            for i in rand_a:
                all_chinese = self.al_wd[i][1].split("|")
                r = all_chinese[0]
                if i == self.random_list[i_n]:
                    self.word_chinese = u_btn_left(
                        text=r,
                        rt='1',
                        background_color=(1, 1, 1, 1),
                        size_hint=(None, None),
                        size=(self.size[0], self.size[1] * .12),
                        font_size='20sp',
                        pos_hint={'x': 0, 'y': the_h[index]},
                        color=(0, 0, 0),
                        on_press=self.check_a
                    )
                    self.add_widget(self.word_chinese)
                    index += 1
                else:
                    self.word_chinese = u_btn_left(
                        text=r,
                        rt='0',
                        background_color=(1, 1, 1, 1),
                        size_hint=(None, None),
                        size=(self.size[0], self.size[1] * .12),
                        font_size='20sp',
                        pos_hint={'x': 0, 'y': the_h[index]},
                        color=(0, 0, 0),
                        on_press=self.check_a
                    )
                    self.add_widget(self.word_chinese)
                    index += 1
            self.out_s_b = u_btn_img(
                img_p="picture/p18.jpg",
                background_color=(1, 1, 1, 1),
                size_hint=(.2, .1),
                pos_hint={'x': .7, 'y': .8},
                on_press=self.out_sound
            )
            self.add_widget(self.out_s_b)

    def out_sound(self, *args):
        path = 'sound_path/' + self.s_n_w + '.mp3'
        sound = SoundLoader.load(path)
        sound.play()

    def back_home(self, *args):
        self.clear_widgets()
        self.parent.transition = SlideTransition(direction='down')
        self.parent.current = 'Home'

    def check_a(self, *args):
        if args[0].rt == '0':
            args[0].color = (1, 0, 0)

        else:
            self.i_n += 1
            self.i_n = self.i_n % len(self.al_wd)
            self.s_n_w = self.al_wd[int(self.random_list[self.i_n])][0]
            self.clear_widgets()
            self.new_w(self.i_n)

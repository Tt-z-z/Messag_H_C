from kivy.uix.screenmanager import Screen, SlideTransition
import random
from kivy.uix.image import Image
from kivy.uix.label import Label
from datetime import datetime
from utils.U_button_to_show import u_btn, u_btn_img
from kivy.graphics import Color, Rectangle
from screen_i_d.search_screen import S_s
import sqlite3

now = datetime.now()
current_hour = now.hour
if current_hour < 12:
    now_t = '上午好'
else:
    now_t = '下午好'

all_p = ['p4.jpg', 'p5.jpg', 'p6.jpg']
random.shuffle(all_p)
now_p = all_p[0]
name_home = 'Home'

bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()


class Home_s(Screen):
    def __init__(self, **kwargs):
        super(Home_s, self).__init__(**kwargs)
        self.name = name_home
        self.image = Image(source='picture/' + now_p, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)
        self.label = Label(text=now_t, color=(1, 1, 1), font_size='73sp', size_hint=(1, .23),
                           pos_hint={'x': 0, 'y': .60})
        self.add_widget(self.label)
        self.learn_b = u_btn(text='learn',
                             size_hint=(.43, .1),
                             pos_hint={'x': .03, 'y': .15},
                             on_press=self.g_t_learn
                             )
        self.search_b = u_btn(text='search',
                              size_hint=(.43, .1),
                              pos_hint={'x': .54, 'y': .15},
                              on_press=self.go_search
                              )
        self.add_widget(self.learn_b)
        self.add_widget(self.search_b)
        self.bind(size=self.update, pos=self.update)

    def g_t_learn(self, *args):
        bk_c.execute("""create table if not exists now_book_word(now_book text,now_word text)""")
        bk_c.execute('select * from now_book_word')
        t_n_b_w_a = bk_c.fetchall()
        if len(t_n_b_w_a) != 0:
            self.parent.transition = SlideTransition(direction='left')
            self.parent.current = 'Learn'

    def go_search(self, *args):
        bk_c.execute("create table if not exists book_data(book_name text)")
        bk_c.execute('select * from book_data')
        bk_y_n = bk_c.fetchall()
        if len(bk_y_n) != 0:
            if self.parent.has_screen('Search'):
                self.parent.remove_widget(self.parent.get_screen('Search'))
            self.parent.add_widget(S_s())
            self.parent.transition = SlideTransition(direction='left')
            self.parent.current = 'Search'

    def update(self, *args):
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=(0, 0), size=(self.size[0], self.size[1] * 0.1))
        self.list_b_1 = u_btn_img(
            img_p='picture/p7.jpg',
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.07, 'y': 0},
            size_hint=(None, None),
            on_press=self.g_t_w_b
        )
        self.add_widget(self.list_b_1)

        self.list_b_2 = u_btn_img(
            img_p='picture/p8.jpg',
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.404, 'y': 0},
            size_hint=(None, None),
            on_press=self.g_t_s_c
        )
        self.add_widget(self.list_b_2)

        self.list_b_3 = u_btn_img(
            img_p='picture/p9.jpg',
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.738, 'y': 0},
            size_hint=(None, None),
            on_press=self.g_t_spell
        )
        self.add_widget(self.list_b_3)


    def g_t_w_b(self, *args):
        self.parent.transition = SlideTransition(direction='up')
        self.parent.current = 'Word_book'

    def g_t_s_c(self, *args):
        self.parent.transition = SlideTransition(direction='up')
        self.parent.current = 'Select'

    def g_t_spell(self, *args):
        self.parent.transition = SlideTransition(direction='up')
        self.parent.current = 'Spell'

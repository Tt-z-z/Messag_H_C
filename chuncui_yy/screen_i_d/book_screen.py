from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from utils.U_button_to_show import u_btn, u_btn_img, u_btn_bk, u_btn_left, smt_btn
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout  # 导入网格布局
from kivy.uix.scrollview import ScrollView
from screen_i_d.learn_screen import Ln_s
import sqlite3
import os
bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()

name_bk = 'Book'


class Bk_s(Screen):
    def __init__(self, **kwargs):
        super(Bk_s, self).__init__(**kwargs)
        self.name = name_bk
        self.bind(size=self.update)
        self.scroll = ScrollView()
        self.label = Label(text=name_bk,
                           color=[0, 0, 0],
                           size_hint=(1, 0.1),
                           pos_hint={'x': 0, 'y': .92},
                           font_size='23sp',
                           )
        self.graph = GridLayout(cols=1, size_hint=(1, None), spacing=3)
        self.graph.bind(minimum_height=self.graph.setter('height'))

    def update(self, *args):
        with self.canvas:
            Color(1, 1, 1, .9)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
        self.book_name = self.parent.now_book
        self.label.text = self.book_name
        self.add_widget(self.label)

        self.b_back_w_b = u_btn_img(
            img_p="picture/p14.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.g_t_w_b
        )
        self.add_widget(self.b_back_w_b)

        bk_c.execute(f'select * from {self.book_name}')
        word_of_book = bk_c.fetchall()
        for i in word_of_book:
            self.graph.add_widget(smt_btn(
                text=str(i[0]),
                size_hint=(1, None),
                size=(self.size[0], self.size[1] * .05),
                valign='middle',
                background_color=(0, 0, 0, .4),
                on_click=self.g_t_learn,
                on_long_press=self.dlt_the_word
            ))

        self.scroll.add_widget(self.graph)
        self.scroll.size_hint = (1, .9)
        self.add_widget(self.scroll)

    def g_t_w_b(self, *args):
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'Word_book'

    def g_t_learn(self, *args):
        bk_c.execute(f'delete from now_book_word')
        bk_c.execute(f'insert into now_book_word values(?,?)', (self.book_name,args[0].text,))
        bk_cmt_sql.commit()
        if self.parent.has_screen('Learn'):
            self.parent.remove_widget(self.parent.get_screen('Learn'))
        self.parent.add_widget(Ln_s())
        self.parent.transition = SlideTransition(direction='down',duration=0.3)
        self.parent.current = 'Learn'
        self.parent.now_word = args[0].text

    def dlt_the_word(self, *args):
        on_clk_word = args[0].text
        bk_c.execute(f'select * from {self.book_name} where english=?', (on_clk_word,))
        word_massage = bk_c.fetchall()
        word_massage = word_massage[0]
        path_s = [f'sound_path/{word_massage[0]}.mp3']
        if word_massage[3] == 'N':
            try:
                os.remove(path_s[0])
            except OSError:
                pass
            bk_c.execute(f'update {self.book_name} set father=? where english=?', (word_massage[3], word_massage[4],))
            bk_c.execute(f'delete from {self.book_name} where english=?', (word_massage[0],))
            bk_cmt_sql.commit()  # 提交数据
            self.graph.remove_widget(args[0])

        else:
            try:
                os.remove(path_s[0])
            except OSError:
                pass
            bk_c.execute(f'update {self.book_name} set children=? where english=?', (word_massage[4], word_massage[3],))
            bk_c.execute(f'update {self.book_name} set father=? where english=?', (word_massage[3], word_massage[4],))
            bk_c.execute(f'delete from {self.book_name} where english=?', (word_massage[0],))
            bk_cmt_sql.commit()  # 提交数据
            self.graph.remove_widget(args[0])
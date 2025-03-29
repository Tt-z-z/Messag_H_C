from kivy.uix.screenmanager import Screen, SlideTransition
from utils.U_button_to_show import u_btn_img, u_btn_left
from kivy.graphics import Color, Rectangle
import sqlite3
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from functools import partial

bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()

name_ln = 'Learn'

class Ln_s(Screen):
    def __init__(self, **kwargs):
        super(Ln_s, self).__init__(**kwargs)
        self.name = name_ln
        self.bind(size=self.update)
        self.on_st = False
        self.l_b_2_img_p = 'picture/p15.jpg'

    def update(self, *args):
        with self.canvas:
            Color(1, 1, 1, .9)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
        self.new_data()
    def new_data(self):
        bk_c.execute('select * from now_book_word')
        nw = bk_c.fetchall()
        nw = nw[0]
        self.now_word = nw[1]
        self.now_book = nw[0]
        self.clear_widgets()
        self.bk_home = u_btn_img(
            img_p="picture/p14.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.back_home
        )
        self.add_widget(self.bk_home)
        bk_c.execute(f'select * from {self.now_book} where english=?', (self.now_word,))
        word_massage = bk_c.fetchone()
        ch = ''
        all_chinese = word_massage[1].split("|")
        for i in all_chinese:
            ch += i + '\n'
        self.word_label = u_btn_left(
            text=word_massage[0],
            background_color=(1, 1, 1, 0),
            size_hint=(None, None),
            size=(self.size[0], self.size[1] * .3),
            font_size='50sp',
            pos_hint={'x': 0, 'y': .6},
            color=(0, 0, 0),
        )
        self.add_widget(self.word_label)

        self.word_chinese = u_btn_left(
            text=ch,
            background_color=(1, 1, 1, 0),
            size_hint=(None, None),
            size=(self.size[0], self.size[1] * .3),
            font_size='20sp',
            pos_hint={'x': 0, 'y': .5},
            color=(0, 0, 0),
        )
        self.add_widget(self.word_chinese)

        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=(0, 0), size=(self.size[0], self.size[1] * 0.1))

        self.list_b_1 = u_btn_img(
            img_p='picture/p14.jpg',
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.07, 'y': 0},
            size_hint=(None, None),
            on_press=self.g_t_father
        )
        self.add_widget(self.list_b_1)

        self.list_b_2 = u_btn_img(
            img_p=self.l_b_2_img_p,
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.404, 'y': 0},
            size_hint=(None, None),
            on_press=self.start_s
        )
        self.add_widget(self.list_b_2)

        self.list_b_3 = u_btn_img(
            img_p='picture/p17.jpg',
            background_color=(1, 1, 1, 1),
            size=(self.size[1] * 0.1, self.size[1] * 0.1),
            pos_hint={'x': 0.738, 'y': 0},
            size_hint=(None, None),
            on_press=self.g_t_children
        )
        self.add_widget(self.list_b_3)

        self.out_s_b = u_btn_img(
            img_p="picture/p18.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.2, .1),
            pos_hint={'x': .7, 'y': .8},
            on_press=self.out_sound
        )
        self.add_widget(self.out_s_b)

    def back_home(self, *args):
        bk_c.execute(f'delete from now_book_word')
        bk_c.execute(f'insert into now_book_word values(?,?)', (self.now_book, self.now_word,))
        bk_cmt_sql.commit()
        self.parent.transition = SlideTransition(direction='up')
        self.parent.current = 'Home'

    def g_t_father(self, *args):
        bk_c.execute(f'select * from {self.now_book} where english=?', (self.now_word,))
        res = bk_c.fetchone()

        if res[3] != 'N':
            bk_c.execute(f'delete from now_book_word')
            bk_c.execute(f'insert into now_book_word values(?,?)', (self.now_book, res[3],))
            bk_cmt_sql.commit()
            self.new_data()

    def g_t_children(self, *args):
        bk_c.execute(f'select * from {self.now_book} where english=?', (self.now_word,))
        res = bk_c.fetchone()
        if res[4] != '0':
            bk_c.execute(f'delete from now_book_word')
            bk_c.execute(f'insert into now_book_word values(?,?)', (self.now_book, res[4],))
            bk_cmt_sql.commit()
            self.new_data()

    def out_sound(self, *args):
        path = 'sound_path/' + args[0].parent.now_word + '.mp3'
        sound = SoundLoader.load(path)
        sound.play()

    def start_s(self, *args):
        if self.on_st:
            self.on_st = False
            self.l_b_2_img_p = 'picture/p15.jpg'
        else:
            self.on_st = True
            self.l_b_2_img_p = 'picture/p16.jpg'
            self.remove_widget(self.list_b_2)
            self.list_b_2 = u_btn_img(
                img_p=self.l_b_2_img_p,
                background_color=(1, 1, 1, 1),
                size=(self.size[1] * 0.1, self.size[1] * 0.1),
                pos_hint={'x': 0.404, 'y': 0},
                size_hint=(None, None),
                on_press=self.start_s
            )
            self.add_widget(self.list_b_2)
            self.wil_sound()
        pass

    def wil_sound(self, *args):
        bk_c.execute(f'select * from {self.now_book} where english=?', (self.now_word,))
        res = bk_c.fetchone()
        path = 'sound_path/' + res[0] + '.mp3'
        sound = SoundLoader.load(path)
        sound.play()
        self.check_playing(sound)

    def check_playing(self, s, *args):
        bk_c.execute(f'select * from {self.now_book} where english=?', (self.now_word,))
        res = bk_c.fetchone()
        if not s.state == 'play':
            if res[4] != '0':
                bk_c.execute(f'delete from now_book_word')
                bk_c.execute(f'insert into now_book_word values(?,?)', (self.now_book, res[4],))
                bk_cmt_sql.commit()
                self.new_data()
                if self.on_st:
                    self.wil_sound()
                else:
                    return False
            else:
                self.l_b_2_img_p = 'picture/p15.jpg'
                self.new_data()

        else:
            Clock.schedule_once(partial(self.check_playing, s), 0.1)  # 每0.1秒检查一次

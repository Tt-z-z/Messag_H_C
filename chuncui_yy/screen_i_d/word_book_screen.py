from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from utils.U_button_to_show import u_btn, u_btn_img, u_btn_bk
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout  # 导入网格布局
from kivy.uix.scrollview import ScrollView
import sqlite3
from screen_i_d.book_screen import Bk_s
from utils.U_img_to_click import u_img_click


bk_cmt_sql = sqlite3.connect('book_cnt.db')
bk_c = bk_cmt_sql.cursor()
bk_c.execute("create table if not exists book_data(book_name text)")
name_w_b = 'Word_book'



class W_b_s(Screen):
    def __init__(self, **kwargs):
        super(W_b_s, self).__init__(**kwargs)
        self.name = name_w_b
        bk_c.execute('select * from book_data')
        self.al_bk_cnt = bk_c.fetchall()
        self.bind(size=self.update)
        self.scroll = ScrollView()
        self.graph = GridLayout(cols=1, size_hint=(1, None), spacing=7)
        self.graph.bind(minimum_height=self.graph.setter('height'))

    #
    def update(self, *args, **kwargs):
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height))

        for i in self.al_bk_cnt:
            self.book_btn = u_btn_bk(
                l_text=i[0],
                size_hint_x=.8,
                size_hint_y=None,
                f_img='picture/p12.jpg',
                s_img='picture/p13.jpg',
                on_press=self.go_to_book
            )
            self.graph.add_widget(self.book_btn)

        sm = [i for i in self.graph.children if type(i).__name__ == 'u_btn_bk']
        for i in sm:
            s = [b for b in i.children if type(b).__name__ == 'Button'][0]
            s.bind(on_press=self.s_b_p)
        self.ad_bk = u_img_click(source='picture/p11.jpg',
                                 size_hint=(1, None),
                                 on_press=self.new_a_bk,
                                 )
        self.graph.add_widget(self.ad_bk)

        self.list_b_1 = u_btn_img(
            img_p="picture/p10.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.g_t_h,
        )
        self.add_widget(Label(text="单词本",
                              font_size="20sp",
                              size_hint=(1, .1),
                              pos_hint={'x': 0, 'y': .9},
                              color=(0, 0, 0, 1)
                              ))
        self.add_widget(self.list_b_1)
        self.scroll.add_widget(self.graph)
        self.add_widget(self.scroll)
        self.scroll.size_hint = (1, .9)

    def new_a_bk(self, *args, **kwargs):
        with self.canvas:
            self.color_cn = Color(1, 1, 1, .5)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
        self.list_b_1.disabled = True
        self.ad_bk.disabled = True
        self.white_bb = u_btn(
            background_color=(0, 0, 0, 1),
            size_hint=(.773 / 1.1, .4 / 1.1),
            pos_hint={'x': .14, 'y': .34},
            disabled=True
        )
        self.add_widget(self.white_bb)

        self.bb_label = Label(text='新建单词本',
                              size_hint=(1, .14),
                              pos_hint={'x': 0, 'y': .59},
                              color=(0, 0, 0, 1),
                              font_size='34sp'
                              )
        self.add_widget(self.bb_label)

        self.bb_textinput = TextInput(size_hint=(.773 / 1.1, .057),
                                      pos_hint={'x': .14, 'y': .54},
                                      hint_text='名称',
                                      background_color=(
                                          0.41568627450980394, 0.788235294117647, 0.9137254901960784, 0.5),
                                      background_normal='',
                                      background_active='',
                                      border=(10, 10, 10, 10),
                                      font_size='30sp',
                                      multiline=False,
                                      )
        self.add_widget(self.bb_textinput)

        self.bb_bcal = u_btn(text='取消',
                             size_hint=(.25, .25 / 4),
                             pos_hint={'x': .19, 'y': .36},
                             color=(0, 0, 0, 1),
                             on_press=self.bb_back
                             )
        self.add_widget(self.bb_bcal)

        self.bb_bok = u_btn(text='确认',
                            size_hint=(.25, .25 / 4),
                            pos_hint={'x': .54, 'y': .36},
                            color=(0, 0, 0, 1),
                            )
        self.bb_bok.bind(on_press=self.bb_ok)
        self.add_widget(self.bb_bok)

    def bb_back(self, *args, **kwargs):
        self.remove_widget(self.bb_textinput)
        self.remove_widget(self.bb_bcal)
        self.remove_widget(self.bb_bok)
        self.remove_widget(self.bb_label)
        self.remove_widget(self.white_bb)
        self.list_b_1.disabled = False
        self.ad_bk.disabled = False
        self.color_cn.rgba = (1, 1, 1, .0)

    def bb_ok(self, *args, **kwargs):
        b_name = self.bb_textinput.text
        if len(b_name) == 0:
            return True
        # print(b_name)
        bk_c.execute("insert into book_data values(?)", (b_name,))
        bk_c.execute("select * from book_data")
        bk_cmt_sql.commit()
        self.bb_back()
        # 开始写数据导入部分
        self.graph.remove_widget(self.ad_bk)
        self.book_btn = u_btn_bk(
            l_text=self.bb_textinput.text,
            size_hint_x=.8,
            size_hint_y=None,
            f_img='picture/p12.jpg',
            s_img='picture/p13.jpg',
            on_press=self.go_to_book
        )
        self.graph.add_widget(self.book_btn)
        self.graph.add_widget(self.ad_bk)  # 显示处理完成
        # 已向book_data中写入数据,开始name为名字的新表格
        bk_c.execute(
            f'CREATE TABLE IF NOT EXISTS {b_name} ('
            'english TEXT, '
            'chinese TEXT, '
            'sound_path TEXT, '
            'father TEXT, '
            'children TEXT)'
        )
        bk_cmt_sql.commit()
        sm = [i for i in self.graph.children if type(i).__name__ == 'u_btn_bk']
        for i in sm:
            s = [b for b in i.children if type(b).__name__ == 'Button'][0]
            s.bind(on_press=self.s_b_p)
    def s_b_p(self, *args):
        bk_cmt_sql = sqlite3.connect('book_cnt.db')
        bk_c = bk_cmt_sql.cursor()
        book_name = args[0].parent.l_text
        bk_c.execute(f'delete from book_data where book_name=?', (book_name,))
        bk_c.execute(f'drop table if exists {args[0].parent.l_text}')
        bk_cmt_sql.commit()
        self.graph.remove_widget(args[0].parent)

    def g_t_h(self, *args, **kwargs):
        self.parent.transition = SlideTransition(direction='down')
        self.parent.current = 'Home'

    def go_to_book(self, *args):
        if self.parent.has_screen('Book'):
            self.parent.remove_widget(self.parent.get_screen('Book'))
        self.parent.add_widget(Bk_s())
        self.parent.transition = SlideTransition(direction='left')
        self.parent.now_book = args[0].l_text
        self.parent.current = 'Book'

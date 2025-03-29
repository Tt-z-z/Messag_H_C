from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from utils.U_button_to_show import u_btn, u_btn_img, u_btn_left
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout  # 导入网格布局
from kivy.uix.scrollview import ScrollView
import sqlite3
import requests
from kivy.uix.spinner import Spinner



name_s = 'Search'


def download_audio(word, save_dir="sound_path"):
    url = "http://dict.youdao.com/dictvoice"
    params1 = {"audio": word, "type": "1"}  # type=2表示美式发音
    list_p = [params1]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0)"}
    for i in list_p:
        response = requests.get(url, params=i, headers=headers)
        with open(f"{save_dir}/{word}.mp3", "wb") as f:
            f.write(response.content)
        response.close()




class S_s(Screen):
    def __init__(self, **kwargs):
        super(S_s, self).__init__(**kwargs)
        self.bk_cmt_sql = sqlite3.connect('book_cnt.db')
        self.bk_c = self.bk_cmt_sql.cursor()
        self.name = name_s
        self.bind(size=self.update)
        self.scroll = ScrollView()
        self.graph = GridLayout(cols=1, size_hint=(1, None), spacing=7)
        self.graph.bind(minimum_height=self.graph.setter('height'))

    def update(self, *args):
        with self.canvas:
            Color(rgba=(1, 1, 1, .9))
            Rectangle(pos=(0, 0), size=(self.width, self.height))

        self.scroll.size_hint = (1, .8)
        self.scroll.add_widget(self.graph)
        self.add_widget(self.scroll)

        self.textinput = TextInput(
            size_hint=(.8, .04),
            pos_hint={'x': .05, 'y': .85},
            hint_text='请输入你想查询的单词',
            background_color=(1, 1, 1, 1),
            background_normal='',
            background_active='',
            border=(10, 10, 10, 10),
            font_size='20sp',
            multiline=False,
        )
        self.add_widget(self.textinput)

        self.sh_button = Button(
            text='搜索',
            size_hint=(.1, .04),
            pos_hint={'x': .86, 'y': .85},
            background_color=(1, 1, 1, 1),
            on_press=self.start_sh
        )
        self.add_widget(self.sh_button)

        self.bk_home = u_btn_img(
            img_p="picture/p14.jpg",
            background_color=(1, 1, 1, 1),
            size_hint=(.11595, .06),
            pos_hint={'x': 0, 'y': .94},
            on_press=self.back_home
        )
        self.add_widget(self.bk_home)

    def back_home(self, *args):
        self.graph.clear_widgets()
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'Home'

    def start_sh(self, *args):
        sh_text = self.textinput.text
        self.textinput.text = ''
        url = f"http://dict.youdao.com/jsonapi?q={sh_text}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Referer": "http://dict.youdao.com/",
        }
        if len(sh_text) < 1:
            return True
        response = requests.get(url, headers=headers)
        data = response.json()
        if "ec" in data:
            self.graph.clear_widgets()
            word_info = data["ec"]["word"][0]
            char =  word_info['return-phrase']['l']['i'] + '\n'
            for trs in word_info["trs"]:
                char += '-'+trs['tr'][0]['l']['i'][0]+'\n'
            char = char[:-1]
            self.btn = u_btn_left(
                text=char,
                background_color=(1, 1, 1, 0),
                size=(self.size[0], self.size[1] * 0.3),
                on_press=self.add_word,
                color=(0, 0, 0)
            )
            self.graph.add_widget(self.btn)


    def add_word(self, *args):
        self.bk_home.disabled = True
        self.sh_button.disabled = True
        self.textinput.disabled = True
        ch = args[0].text
        self.ch = ch.split('\n')

        with self.canvas:
            self.color_cn = Color(1, 1, 1, .5)
            Rectangle(pos=(0, 0), size=(self.width, self.height))

        self.ad_bkb = u_btn(
            background_color=(0, 0, 0, 1),
            size_hint=(.773 / 1.1, .4 / 1.1),
            pos_hint={'x': .14, 'y': .34},
            disabled=True
        )
        self.add_widget(self.ad_bkb)

        self.ad_label = Label(text='选择单词本',
                              size_hint=(1, .14),
                              pos_hint={'x': 0, 'y': .59},
                              color=(0, 0, 0, 1),
                              font_size='34sp'
                              )
        self.add_widget(self.ad_label)
        self.bk_c.execute('select * from book_data')
        all_book = self.bk_c.fetchall()  # [('a',), ('v',)]
        all_book = [i[0] for i in all_book]
        self.ad_sp = Spinner(
            text='单词本',
            values=all_book,
            size_hint=(.773 / 1.1, .057),
            size=(150, 40),
            pos_hint={'x': .14, 'y': .54},
            background_color=(
                0.41568627450980394, 0.788235294117647, 0.9137254901960784, 0.5),
            background_normal='',
        )
        self.add_widget(self.ad_sp)

        self.ad_bcal = u_btn(text='取消',
                             size_hint=(.25, .25 / 4),
                             pos_hint={'x': .19, 'y': .36},
                             color=(0, 0, 0, 1),
                             on_press=self.ad_back
                             )
        self.add_widget(self.ad_bcal)

        self.ad_bok = u_btn(text='确认',
                            size_hint=(.25, .25 / 4),
                            pos_hint={'x': .54, 'y': .36},
                            color=(0, 0, 0, 1),
                            )
        self.ad_bok.bind(on_press=self.ad_ok)
        self.add_widget(self.ad_bok)
        download_audio(self.ch[0])

    def ad_back(self, *args):
        self.bk_home.disabled = False
        self.sh_button.disabled = False
        self.textinput.disabled = False
        self.color_cn.rgba = (1, 1, 1, 0)
        self.remove_widget(self.ad_bkb)
        self.remove_widget(self.ad_label)
        self.remove_widget(self.ad_sp)
        self.remove_widget(self.ad_bok)
        self.remove_widget(self.ad_bcal)

    def ad_ok(self, *args):
        select_book = self.ad_sp.text
        if select_book == '单词本':
            self.ad_back()
        else:
            self.bk_c.execute(f'select * from {select_book} where english = ?', (self.ch[0],))
            if len(self.bk_c.fetchall()) == 0:
                self.bk_c.execute(f'select * from {select_book}')
                all_word = self.bk_c.fetchall()
                all_chinese = ''
                for i in range(len(self.ch)-1):
                    all_chinese += self.ch[i+1] + '|'
                all_chinese = all_chinese[:-1]
                if len(all_word) > 0:
                    self.btn.text = ''
                    last_word = all_word[-1]
                    self.bk_c.execute(f"UPDATE {select_book} SET children=? WHERE english = ?", (self.ch[0], last_word[0]))  # 写入
                    self.bk_c.execute(f"insert into {select_book} values(?,?,?,?,?)",
                                 (self.ch[0], all_chinese, self.ch[0], last_word[0], 0))  # 写入
                    self.bk_cmt_sql.commit()
                    # self.bk_c.close()
                    # self.bk_cmt_sql.close()
                else:
                    self.btn.text = ''
                    self.bk_c.execute(f"insert into {select_book} values(?,?,?,?,?)",
                                 (self.ch[0], all_chinese, self.ch[0], 'N', 0))  # 写入
                    self.bk_cmt_sql.commit()
                    # self.bk_c.close()
                    # self.bk_cmt_sql.close()
                self.ad_back()

            else:
                self.btn.text = ''
                self.ad_back()


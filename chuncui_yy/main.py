from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '773')
from kivy.core.window import Window
Window.borderless = True  # 取消边框
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,SlideTransition
from screen_i_d.home_screen import Home_s, name_home
from screen_i_d.book_screen import Bk_s,name_bk
from screen_i_d.word_book_screen import W_b_s, name_w_b
from screen_i_d.learn_screen import Ln_s ,name_ln
from screen_i_d.search_screen import S_s,name_s
from screen_i_d.select_chinese_screen import S_c_s,name_s_c_s
from screen_i_d.spell_screen import S_p_s,name_s_p_s
from kivy.core.text import LabelBase

LabelBase.register(name='Roboto', fn_regular=r'./font/simsun.ttc')
al_screen = {
    name_home: Home_s,
    name_w_b: W_b_s,
    name_bk: Bk_s,
    name_s : S_s,
    name_ln: Ln_s,
    name_s_c_s: S_c_s,
    name_s_p_s: S_p_s
}

class u_ScreenManager(ScreenManager):
    def __init__(self,**kwargs):
        super(u_ScreenManager,self).__init__(**kwargs)


class CC_YY(App):
    def __init__(self, **kwargs):
        super(CC_YY, self).__init__(**kwargs)
        self.body = u_ScreenManager()

    def build(self):
        return self.body

    def on_start(self):
        self.body.transition = SlideTransition(direction="up")
        for c, v in al_screen.items():
            self.body.add_widget(v())


CC_YY().run()

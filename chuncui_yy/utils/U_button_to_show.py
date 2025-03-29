from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, BoxShadow
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock


class u_btn(Button):
    def __init__(self, **kwargs):
        super(u_btn, self).__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.background_color = (1, 1, 1, 0)  # 红绿蓝透明度 111是白色,000是黑色
        with self.canvas:
            Color(*get_color_from_hex('#6AC9E9'))
            self.rect = BoxShadow(inset=True, border_radius=[37, 37, 37, 37], size=self.size, pos=self.pos,
                                  blur_radius=37)  # 类阴影
        self.bind(size=self.update_shadow, pos=self.update_shadow)

    def update_shadow(self, widget, value):
        self.rect.size = self.size
        self.rect.pos = self.pos


class u_btn_bk(Button):
    f_img = StringProperty()
    s_img = StringProperty()
    l_text = StringProperty()

    def __init__(self, **kwargs):
        super(u_btn_bk, self).__init__(**kwargs)
        self.background_normal = self.f_img
        self.background_down = self.f_img
        self.button = Button()
        self.add_widget(self.button)
        self.label = Label(text=self.l_text, color=(0, 0, 0), font_size='18sp')
        self.add_widget(self.label)
        self.bind(size=self.update_size, pos=self.update_size)  # 数据绑定

    def update_size(self, *args):
        self.height = self.size[0] * 0.23
        self.button.size_hint = (None, None)
        self.button.background_normal = self.s_img
        self.button.background_down = self.s_img
        self.button.size = (self.size[0] * 0.2, self.size[1])
        self.button.pos = (self.size[0] * 0.8, self.pos[1])
        self.label.size = (self.size[0] * .47, self.size[1] * 0.34)
        self.label.pos = (self.pos[0], self.pos[1] + int(self.size[1] * 0.53))


class u_btn_img(Button):
    img_p = StringProperty()

    def __init__(self, **kwargs):
        super(u_btn_img, self).__init__(**kwargs)
        self.background_normal = self.img_p
        self.background_down = self.img_p


class u_btn_left(Button):
    rt = StringProperty()
    def __init__(self, **kwargs):
        super(u_btn_left, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.halign = 'left'
        self.valign = 'top'
        self.text_size = self.size
        self.padding = [10, 0]


from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock


class smt_btn(Button):
    long_press_time = 0.5  # 长按时间阈值(秒)
    is_long_press = False

    def __init__(self, **kwargs):
        # 从参数中获取回调函数，如果没有则设为None
        self.long_press_callback = kwargs.pop('on_long_press', None)
        self.click_callback = kwargs.pop('on_click', None)
        super(smt_btn, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.halign = 'left'
        self.text_size = self.size
        self.padding = [10, 0]

    def on_press(self):
        self.is_long_press = False
        self._clock_event = Clock.schedule_once(self._do_long_press, self.long_press_time)

    def on_release(self):
        if hasattr(self, '_clock_event'):
            self._clock_event.cancel()
            del self._clock_event

            if not self.is_long_press and self.click_callback:
                self.click_callback(self)  # 传入self作为按钮实例

        self.is_long_press = False

    def _do_long_press(self, dt):
        self.is_long_press = True
        if self.long_press_callback:
            self.long_press_callback(self)  # 传入self作为按钮实例
        else:
            pass


class app(App):
    def build(self):
        return u_btn_left(text='hallo')


if __name__ == '__main__':
    app().run()

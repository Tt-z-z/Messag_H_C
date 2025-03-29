from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window


# 创建自定义的“可点击图片”控件
class u_img_click(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(u_img_click, self).__init__(**kwargs)
        # 可选：设置点击后的反馈（如透明度变化）
        self.always_release = True  # 松开时触发 on_release
        self.allow_stretch=True
        self.keep_ratio = False
        self.bind(size=self.update_size, pos=self.update_size)  # 数据绑定

    def update_size(self, *args):
        self.height = self.size[0] * 0.23


# 主应用类
class MyApp(App):
    def build(self):
        # 设置窗口大小（可选）
        Window.size = (400, 300)

        # 创建ImageButton实例并设置图片源
        btn_img = u_img_click(
            source='your_image.png',  # 替换为你的图片路径
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        return btn_img


if __name__ == '__main__':
    MyApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class SlidingButtonsApp(App):
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical')

        # 创建一个 ScrollView
        scroll_view = ScrollView()

        # 创建一个垂直布局用于存放按钮
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))  # 动态调整高度

        # 添加多个按钮
        for i in range(1, 21):  # 创建 20 个按钮
            button = Button(
                text=f"Button {i}",
                size_hint_y=None,
                # height=50,  # 按钮高度
                background_color=(0.2, 0.6, 1, 1)  # 自定义背景颜色
            )
            button_layout.add_widget(button)

        # 将按钮布局添加到 ScrollView
        scroll_view.add_widget(button_layout)

        # 将 ScrollView 添加到主布局
        main_layout.add_widget(scroll_view)

        return main_layout

if __name__ == '__main__':
    SlidingButtonsApp().run()
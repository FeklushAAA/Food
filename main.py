from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
import os
import ast
import time


# Класс отвечает за запуск стартовой странички приложения, 
# его можно назвать как угодно, например StartScreen. 
# И наследует kivy модуль Screen.
class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)

        # Приложение состоит из 3 окошек, котоыре создаются здесь
        box = BoxLayout(orientation='vertical', spacing=20) #"vertical" делит экран пополам вертикольно, 

        box.size_hint = (0.6, 0.7)
        box.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Добавляем кнопку с подписью "Дневник питания", при нажатии на которую
        # вызывается метод set_screen , который переносит нас на экран
        # дневника питания
        box.add_widget(Button(text='Дневник питания',
        					  font_size = 18,
        					  color='#73ffff',
        					  bold = True,
        					  background_color = '#00fcfc',
         					  on_press=lambda x:
                              set_screen('list_food')))

        # Добавляем кнопку с подписью "Добавить блюдо в дневник питания"
        # в которой вызывается метод 
        box.add_widget(Button(text='Добавить блюдо в дневник питания',
        					  font_size = 18,
        					  color='#73ffff',
        					  bold = True,
        					  background_color = '#00fcfc',
                              on_press=lambda x: set_screen('add_food')))
        					  #on_press вызывает метод при нажатии

        self.add_widget(box) #доабвляет кнопки в слои и окна


class SortedListFood(Screen):
    def __init__(self, **kw):
        super(SortedListFood, self).__init__(**kw)

    def on_enter(self):  # Будет вызвана в момент открытия экрана
        self.layout = GridLayout(cols=1, spacing=20)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Назад в главное меню',
        					bold = True,
        					color='#73ffff',
        					background_color = '#00fcfc',
                            on_press=lambda x: set_screen('menu'),
                            size_hint_y=None, height=dp(40))
        self.layout.add_widget(back_button)

        # RecycleView — модуль, с помощью которого создается вертикальная 
        # прокрутка. 
        # Особенность RecycleView в том, что он строит скролы с элементами 
        # одинаковой ширины и высоты. И работает быстро. 
        # А есть модуль ScrollView, он может строить прокрутки с элементами 
        # разных размеров, но работает медленнее, чем RecycleView

        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

        dic_foods = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        for f, d in sorted(dic_foods.items(), key=lambda x: x[1]):
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
            btn = Button(text=fd,
            			size_hint_y=None,
            			color='#73ffff',
            			bold = True,
        				background_color = '#00fcfc', 
            			height=dp(40))
            self.layout.add_widget(btn)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.layout.clear_widgets()  # очищаем список


class AddFood(Screen):

    def buttonClicked(self, btn1):
        if not self.txt1.text:
            return
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.txt1.text.encode('u8')] = int(time.time())

        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()

        text = "Последнее добавленное блюдо:  " + self.txt1.text
        self.result.text = text
        self.txt1.text = ''

    def __init__(self, **kw):
        super(AddFood, self).__init__(**kw)
        box = BoxLayout(orientation='vertical', spacing=20)
        box.size_hint = (0.6, 0.7)
        box.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        back_button = Button(text='< Назад в главное меню',
        					font_size = 18,
        					color='#73ffff',
        					bold = True,
        					background_color = '#00fcfc',
        					on_press=lambda x:
                            set_screen('menu'),
                            size_hint_y=None, 
                            height=dp(40))
        box.add_widget(back_button)
        self.txt1 = TextInput(text='',
        					multiline=False, 
        					height=dp(40),
                            size_hint=(1,0.4),
                            padding_y = (20,20), 
                            hint_text="Название блюда")
        box.add_widget(self.txt1)
        btn1 = Button(text="Добавить блюдо",
        			font_size = 18,
        			color='#73ffff',
        			bold = True,
        			background_color = '#00fcfc', 
        			size_hint_y=None, 
        			height=dp(80))
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box)


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SortedListFood(name='list_food'))
sm.add_widget(AddFood(name='add_food'))


class FoodOptionsApp(App):
    def __init__(self, **kvargs):
        super(FoodOptionsApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(FoodOptionsApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return sm


if __name__ == '__main__':
    FoodOptionsApp().run()
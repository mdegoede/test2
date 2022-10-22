# need to download modules kivy, kivymd, numpy, sqlite3
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton, MDRaisedButton
from kivy.lang import Builder
from helpers import username_helper, KV
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import numpy as np
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineAvatarIconListItem
import sqlite3

username_helper = """
MDTextField:
    hint_text: "Enter temperature"
    helper_text: "desired temperature"
    icon_right: "temperature-celsius"
    pos_hint:{'center_x':0.5, 'center_y':0.42}
    size_hint_x:0.5
    size_hint_y:0.7
    max_text_length: 2
"""

KV = '''
<ItemConfirm>
    on_release: root.set_icon(check)

    CheckboxLeftWidget:
        id: check
        group: "check"


MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_confirmation_dialog()
'''

Window.size = (360,600)
kivy_defaulttheme_color = np.array([88, 88, 88, 256]) / 256

pink = (np.array([255,192,203, 256]) / 256) / kivy_defaulttheme_color

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class TempApp(MDApp):
    dialog2 = None

    def build(self):
        self.theme_cls.primary_palette='Indigo'
        self.theme_cls.primary_hue='300'
        self.theme_cls.theme_style='Light'
        self.theme_cls.material_style = "M3" # of M2

        button = MDRectangleFlatButton(text='Send', pos_hint={'center_x':0.5, 'center_y':0.32}, on_release=self.show_data)
        icon_btn = MDFloatingActionButton(icon='cog', pos_hint={'center_x':0.9, 'center_y':0.5}, on_release=self.show_colors)
        icon_btn2 = MDFloatingActionButton(icon='book', pos_hint={'center_x': 0.1,'center_y': 0.5}, on_release=self.show_manual)  # or book-open
        layout = BoxLayout(orientation='vertical', spacing=3, padding=8)
        l3 = FloatLayout(size_hint=(1, 0.17), pos_hint={'center_x':0.5, 'center_y':0.85})
        top = MDRaisedButton(text='WELCOME', size_hint=(1, 1), disabled=True, pos_hint={'center_x':0.5, 'center_y':0.5})
        l2 = BoxLayout(orientation='horizontal', spacing=7, padding=0, size_hint=(1, 0.4))
        b3 = MDRaisedButton(text='temperature \n   outside:', disabled=True, size_hint=(0.33, 1))
        b4 = MDRaisedButton(text='  open \nwindow', size_hint=(0.33, 1))
        b5 = MDRaisedButton(text='temperature \n   inside:', disabled=True, size_hint=(0.33, 1))
        self.username = Builder.load_string(username_helper)
        l3.add_widget(top)
        l3.add_widget(icon_btn)
        l3.add_widget(icon_btn2)
        l2.add_widget(b3)
        l2.add_widget(b4)
        l2.add_widget(b5)
        layout.add_widget(l3)
        layout.add_widget(self.username)
        layout.add_widget(button)
        layout.add_widget(l2)

        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists colors(color text)""")
        c.execute("SELECT * FROM colors")
        records = c.fetchall()
        self.theme_cls.primary_palette = records[-1][0]
        conn.commit()
        conn.close()
        return layout

    def show_colors(self, obj):
        Builder.load_string(KV)
        if not self.dialog2:
            self.dialog2 = MDDialog(title="Choose your style!", text='Scroll through the list and touch a name to choose your favourite color.',
                    type="confirmation",
                    items=[
                        ItemConfirm(text="Pink", on_release= self.make_color_pink),
                        ItemConfirm(text="Blue", on_release= self.make_color_blue),
                        ItemConfirm(text="Purple", on_release=self.make_color_Purple),
                        ItemConfirm(text="DeepPurple", on_release=self.make_color_DeepPurple),
                        ItemConfirm(text="Indigo", on_release=self.make_color_Indigo),
                        ItemConfirm(text="LightBlue", on_release=self.make_color_LightBlue),
                        ItemConfirm(text="Cyan", on_release=self.make_color_Cyan),
                        ItemConfirm(text="Teal", on_release=self.make_color_Teal),
                        ItemConfirm(text="Green", on_release=self.make_color_Green),
                        ItemConfirm(text="LightGreen", on_release=self.make_color_LightGreen),
                        ItemConfirm(text="Lime", on_release=self.make_color_Lime),
                        ItemConfirm(text="Yellow", on_release=self.make_color_Yellow),
                        ItemConfirm(text="Amber", on_release=self.make_color_Amber),
                        ItemConfirm(text="Orange", on_release=self.make_color_Orange),
                        ItemConfirm(text="DeepOrange", on_release=self.make_color_DeepOrange),
                        ItemConfirm(text="Brown", on_release=self.make_color_Brown),
                        ItemConfirm(text="Gray", on_release=self.make_color_Gray),
                        ItemConfirm(text="Red", on_release=self.make_color_Red),
                        ItemConfirm(text="BlueGray", on_release=self.make_color_BlueGray)
                    ],
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_dialog2
                        ),
                    ],
                        )
        self.dialog2.open()


    def make_color_blue(self, obj):
        self.theme_cls.primary_palette = 'Blue'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()


    def make_color_pink(self, obj):
        self.theme_cls.primary_palette = 'Pink'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Red(self, obj):
        self.theme_cls.primary_palette = 'Red'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Purple(self, obj):
        self.theme_cls.primary_palette = 'Purple'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_DeepPurple(self, obj):
        self.theme_cls.primary_palette = 'DeepPurple'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Indigo(self, obj):
        self.theme_cls.primary_palette = 'Indigo'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_LightBlue(self, obj):
        self.theme_cls.primary_palette = 'LightBlue'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Cyan(self, obj):
        self.theme_cls.primary_palette = 'Cyan'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Teal(self, obj):
        self.theme_cls.primary_palette = 'Teal'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Green(self, obj):
        self.theme_cls.primary_palette = 'Green'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_LightGreen(self, obj):
        self.theme_cls.primary_palette = 'LightGreen'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Lime(self, obj):
        self.theme_cls.primary_palette = 'Lime'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Yellow(self, obj):
        self.theme_cls.primary_palette = 'Yellow'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Amber(self, obj):
        self.theme_cls.primary_palette = 'Amber'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Orange(self, obj):
        self.theme_cls.primary_palette = 'Orange'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_DeepOrange(self, obj):
        self.theme_cls.primary_palette = 'DeepOrange'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Brown(self, obj):
        self.theme_cls.primary_palette = 'Brown'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_Gray(self, obj):
        self.theme_cls.primary_palette = 'Gray'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()

    def make_color_BlueGray(self, obj):
        self.theme_cls.primary_palette = 'BlueGray'
        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO colors VALUES (:first)", {"first": self.theme_cls.primary_palette,})
        conn.commit()
        conn.close()


    def show_data(self,obj):
        try:
            int(self.username.text)
            if -5 <= int(self.username.text) <= 50:
                check_string = 'Your desired temperature has been updated to ' + self.username.text + '°C.'
            else:
                check_string = 'Please enter a valid number (integer) between -5 and 50.'
        except:
            check_string = 'Please enter a valid number (integer).'
        close_button = MDFlatButton(text='OK', on_release=self.close_dialog)
        self.dialog = MDDialog(title='Update:', text=check_string, buttons=[close_button])
        print(self.username.text)
        self.dialog.open()

    def show_manual(self,obj):
        close_button = MDFlatButton(text='CLOSE', on_release=self.close_dialog3)
        start = "\033[1m"
        end = "\033[0;0m"
        self.dialog3 = MDDialog(title='MANUAL', text='Thank you for using our product! \nTo use the auto-climate app, there are a few features you should know about. In the top of the main screen, there are two buttons: the [b]manual button[/b] (on which you have probably just clicked) and the [b]color-theme button[/b]. If you click in this button, you can choose your favourite color to make the use of this app as much fun as possible. At the bottom of the app, there is one more button: the [b]open-window button[/b]. If you click on this button, your window will autimatically open. Next to the open-window button, you can see the [b]inside[/b] and [b]outside temperature[/b]. In the middle of the screen, you can enter your [b]desired room temperature[/b]. The auto-climate will then check for you when you can open the window to reach your desired room temperature. These are all the features in the app. It is easy to use and will help you safe a lot of energy and money!', buttons=[close_button])
        self.dialog3.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_dialog2(self, obj):
        self.dialog2.dismiss()

    def close_dialog3(self, obj):
        self.dialog3.dismiss()

TempApp().run()

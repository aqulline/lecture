import os
import re

import phonenumbers
from kivy import utils
from kivy.base import EventLoop
from kivy.clock import mainthread, Clock

from kivy.core.window import Window
from kivy.properties import ListProperty, DictProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from phonenumbers import carrier, number_type

from database import Fire_Base as FB

if utils.platform != 'android':
    Window.size = [360, 640]

class NumberField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text) == 0 and substring != "0":
            return

        if len(self.text) == 10:
            return

        if len(self.text) == 1 and substring != "6" and substring != "7":
            return

        if not substring.isdigit():
            return

        return super(NumberField, self).insert_text(substring, from_undo=from_undo)

class Modules(MDCard):
    date = StringProperty("")
    name = StringProperty("")

class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyField, self).insert_text(s, from_undo=from_undo)

class Tab(MDBoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    size_x, size_y = Window.size
    attend_id = ListProperty([])

    present = DictProperty()
    Absent = DictProperty()

    dictionary = {}
    week = None

    module_code = StringProperty("")
    program_name = StringProperty("")
    module_name = StringProperty("")

    # screen
    screens = ['enter']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    def build(self):
        pass

    def on_start(self):
        #self.one()
        Clock.schedule_once(lambda x: self.register_check(), 1)
        self.drop_week()
        self.days()


    def display_Present(self):
        self.root.ids.studs.data = {}
        self.present = FB.present(FB())

        if not self.present:
            self.root.ids.studs.data.append(
                {
                    "viewclass": "Student",
                    "name": "No student Yet!",

                }
            )
        else:
            for i, y in self.present.items():
                self.root.ids.studs.data.append(
                    {
                        "viewclass": "Students",
                        "name": y["student_name"],
                        "registration": y["registration_number"],

                    }
                )
                self.save_present()

    def display_absent(self):
        self.root.ids.absent.data = {}
        self.Absent = FB.absent(FB())

        if not self.Absent:
            self.root.ids.absent.data.append(
                {
                    "viewclass": "Student",
                    "name": "No student Yet!",

                }
            )
        else:
            for i, y in self.Absent.items():
                self.root.ids.absent.data.append(
                    {
                        "viewclass": "Students",
                        "name": y["student_name"],
                        "registration": y["registration_number"],

                    }
                )

    def module(self, name):
        self.root.ids.modules.data = {}
        data = FB.lecture_code(FB(), name)

        if not data:
            self.root.ids.modules.data.append(
                {
                    "viewclass": "Student",
                    "name": "No student Yet!",

                }
            )

        else:
            for i, y in data.items():
                self.root.ids.modules.data.append(
                    {
                        "viewclass": "Modules",
                        "code": y["module_code"],
                        "program": y["program_name"],
                        "name": y["module_name"],

                    }
                )

    def user_login(self, phone, name):

        if FB.get_login(FB(), phone, name):
            sm = self.root
            sm.current = "home"
            self.display_Present()
            self.display_absent()
            self.module(name)
        else:
            toast("Invalid login")

    def validate_user(self, phone, name):
        if not self.phone_number_check_admin(phone):
            pass
        elif name == "":
            toast("please enter your password")
        else:
            FB.lecture(FB(), phone, name)
            self.module(name)
            self.remember_me(phone)
            self.screen_capture("enter")
    def phone_number_check_admin(self, phone):
        new_number = ""
        if phone != "" and len(phone) == 10:
            for i in range(phone.__len__()):
                if i == 0:
                    pass
                else:
                    new_number = new_number + phone[i]
            number = "+255" + new_number
            if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
                toast("Please check your phone number!", 1)
                return False
            else:
                self.public_number = number
                return True
        else:
            toast("enter phone number!")


    def save_present(self, ):
        with open("present.xlsx", "w") as file:
            for key, value in self.present.items():
                file.write(f"{key};{value}\n")

    def move_file(self, source, destination):
        import shutil
        shutil.move(source, destination)

    # Example usage:
    def one(self):
        source_file = "/home/alpha/PycharmProjects/lecture/present.xlsx"
        destination_file = "/home/alpha/present.xlsx"
        self.move_file(source_file, destination_file)
        print("done")

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)


    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    week_days = ListProperty([])

    def drop_week(self):

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_week(x),
            } for i in self.week_days
        ]
        self.week = MDDropdownMenu(
            caller=self.root.ids.week,
            items=menu_items,
            position="auto",
            width_mult=4,
        )
        self.week.bind()

    def set_week(self, text_item):
        self.root.ids.week.text = text_item
        toast(text_item)
        self.present(FB.present(FB(), text_item))
        self.week.dismiss()

    @mainthread
    def days(self):
        data = FB.month(FB())
        for x,y in data.items():
            self.week_days.append(x)

    def remember_me(self, phone):
        with open("lecture.txt", "w") as fl:
            fl.write(phone)
        fl.close()

    def register_check(self):
        sm = self.root
        file_size = os.path.getsize("lecture.txt")
        if file_size == 0:
            self.screen_capture("register")
        else:
            sm.current = "register"
            self.screen_capture("login")

MainApp().run()

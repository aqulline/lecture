from kivy import utils

from kivy.core.window import Window
from kivy.properties import ListProperty, DictProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase

from database import Fire_Base as FB

if utils.platform != 'android':
    Window.size = [360, 640]


class Tab(MDBoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    size_x, size_y = Window.size
    attend_id = ListProperty([])

    present = DictProperty()
    Absent = DictProperty()

    dictionary = {}

    def build(self):
        pass

    def on_start(self):
        #self.one()
        self.display_Present()
        self.display_absent()


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

    def save_present(self, ):
        with open("present.xlsx", "w") as file:
            for key, value in self.present.items():
                file.write(f"{key};{value}\n")

    def move_file(self, source, destination):
        import shutil
        shutil.move(source, destination)

    # Example usage:
    def one(self):
        source_file = "/home/noface/PycharmProjects/lecture/present.xlsx"
        destination_file = "/home/noface/present.xlsx"
        self.move_file(source_file, destination_file)
        print("done")


MainApp().run()

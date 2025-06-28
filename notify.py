#!/usr/bin/env python

import base64
import sqlite3
import time
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors import HoverBehavior

# Connect to the SQLite database
conn = sqlite3.connect("user.db")
cursor = conn.cursor()

# Read the username from the credentials file
with open("credentials.txt", "r") as file:
    username = file.readline().strip()

# Query the database to retrieve the image data for the specified username
cursor.execute("SELECT user_photo FROM user_info WHERE username = ?", (username,))
image_data = cursor.fetchone()[0]  # Assuming only one row is returned

# Convert the image data to Base64 encoding
image_base64 = base64.b64encode(image_data).decode("utf-8")

# Get the current time
current_time = datetime.now()

KV = """
BoxLayout:
    orientation: 'vertical'

    MDFloatLayout:
        MDIconButton:
            icon: "close-circle"
            theme_text_color: "Custom"
            icon_size: "20sp"
            text_color: 1, 0, 0, 1
            pos_hint: {'center_x': 0.06, 'center_y': 0.8}
            opacity: 0.9
            on_release: app.close_application()
        
        Image:
            id: user_pic
            icon: ""
            icon_size: "170sp"
            pos_hint: {'center_x': 0.8, 'center_y': 0.5}

        MDLabel:
            text: 'Assalam Walekum,'
            theme_text_color: 'Custom'
            opacity: 0.8
            text_color: 1, 1, 1, 0.8
            font_style: 'H6'
            pos_hint: {'center_x': 0.6 ,  'center_y': 0.8}

        MDLabel:
            id: user_name
            text: 'Wans'
            pos_hint: {'center_x': 0.6 ,  'center_y': 0.69}
            theme_text_color: 'Custom'
            text_color: 0.5, 0.5, 0.5, 0.5
            font_style: 'Body2'
            
        MDLabel:
            text: "[b] Let[color=#673AB7] 's Work To[/color]gether ! [/b]"
            pos_hint: {'center_x': 0.58, 'center_y': 0.45}
            markup: True
            theme_text_color: 'Custom'
            text_color: 0.5, 0.5, 0.5, 0.5
            font_style: 'H5'
            
        MDLabel:
            text: " Logged-In : "
            pos_hint: {'center_x': 0.59, 'center_y': 0.2}
            markup: True
            theme_text_color: 'Custom'
            text_color: 0.5, 0.5, 0.5, 0.5
            font_name: "Nova"
            font_style: 'Body2'
            
        MDLabel:
            id: time_label
            text: ""
            pos_hint: {'center_x': 0.76, 'center_y': 0.2}
            theme_text_color: 'Custom'
            text_color:  1, 1, 1, 0.3
            font_style: 'Body2'
"""


class MDIconButton(Button, HoverBehavior):
    def on_enter(self):
        self.opacity = 1
        Animation(size_hint=(0.6, 0.1), d=0.3).start(self)

    def on_leave(self):
        self.opacity = 0.2


class MsgApp(MDApp):
    current_time = StringProperty()

    def build(self):
        Window.size = [450, 150]
        Window.minimum_size = Window.size
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        LabelBase.register(name="Nova", fn_regular="./Font/NovaSquare-Regular.ttf")

        sound = SoundLoader.load("./Sound/ting.mp3")
        if sound:
            sound.play()

        screen = Builder.load_string(KV)

        screen_width, screen_height = Window.size
        window_width, window_height = 615, 1250
        Window.left = screen_width - window_width
        Window.top = screen_height - window_height

        Window.borderless = True

        self.last_interaction = time.time()

        current_datetime1 = datetime.now().strftime("%I:%M:%S %p")
        current_date = datetime.now().date()
        screen.ids.time_label.text = f"{current_datetime1}"

        try:
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                print(lines)
        except FileNotFoundError:
            pass

        username = (
            lines[0] if lines else ""
        )  # Accessing the first (and only) element in the list
        username = username.strip("[]")  # Remove square brackets

        screen.ids.user_name.text = f"{username}".capitalize()
        import os

        os.remove("credentials.txt")

        # Determine the file extension dynamically based on the image data
        import imghdr

        image_extension = imghdr.what(None, h=image_data)

        # Set the icon property of the user_pic widget with the correct file extension
        screen.ids.user_pic.source = (
            f"data:image/{image_extension};base64,{image_base64}"
        )

        # Execute the SQL query with the username variable
        cursor.execute(
            "INSERT INTO user_login (user_photo, username, Date_user, Time_user) VALUES (?, ?, ?, ?)",
            (image_data, username, current_date, current_datetime1),
        )
        conn.commit()
        conn.close()

        print("Data inserted successfully")

        # Schedule the inactivity check every 1 second
        Clock.schedule_interval(self.check_inactivity, 1)

        # Bind update_last_interaction to user input events
        Window.bind(on_motion=self.update_last_interaction)
        Window.bind(on_touch_down=self.update_last_interaction)
        Window.bind(on_touch_up=self.update_last_interaction)
        Window.bind(on_key_down=self.update_last_interaction)

        return screen

    def on_stop(self):
        return self.on_request_close()

    def on_request_close(self):
        popup = Popup(
            title="Logout Required",
            content=Label(text="Please log out before closing the window."),
            size_hint=(None, None),
            size=(300, 200),
        )
        popup.open()
        return True

    def check_inactivity(self, dt):
        current_time = time.time()
        timeout = 2  # Timeout set to 2 seconds
        if current_time - self.last_interaction >= timeout:
            self.fade_out_and_hide()

    def update_last_interaction(self, *args):
        self.last_interaction = time.time()

    def fade_out_and_hide(self):
        # Create the fade-out animation
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=lambda *x: self.hide_window())
        anim.start(self.root)

    def hide_window(self):
        Window.hide()
        print("App is hidden and running in the background")

    def close_application(self):
        if self.user_is_logged_out():
            logout_time = datetime.now().strftime("%I:%M:%S %p")
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username FROM user_login WHERE username = ?", (username,)
            )
            id_number = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE user_login SET log_out = ? WHERE username = ?",
                (logout_time, id_number),
            )
            conn.commit()
            conn.close()

            self.stop()
        else:
            self.on_request_close()

    def user_is_logged_out(self):
        return True


if __name__ == "__main__":
    MsgApp().run()

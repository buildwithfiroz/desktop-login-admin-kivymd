from kivy.core.window import Window
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.clock import Clock
import subprocess
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.uix.image import Image
from kivymd.uix.button import MDFlatButton
import sqlite3


class CustomScreen(Screen):  # Your screen class
    def on_success_login(self):
        # If login is successful
        self.ids.login_button.text = ""  # Clear the text
        self.ids.login_button.disabled = True  # Disable the button
        # Add a loading spinner or loading indicator
        # For example, you can use an ActivityIndicator here
        # Make sure to import necessary modules (e.g., MDSpinner)
        spinner = MDSpinner(pos_hint={"center_x": 0.75, "center_y": 0.47})
        self.add_widget(spinner)

        # Perform actions after a delay (simulate loading)``
        Clock.schedule_once(lambda dt: self.load_next_screen(), 2)

    def load_next_screen(self):
        # Perform actions after successful login (loading finished)
        # Remove the spinner
        self.remove_widget(
            self.children[-1]
        )  # Remove the last widget (which is the spinner)
        # Change the button appearance back to its initial state
        self.ids.login_button.text = "Login"
        self.ids.login_button.disabled = False
        # Add code to navigate to the next screen or perform other actions


class Notify(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        Window.borderless = True
        Window.fullscreen = "auto"  # Run in full-screen mode
        global sm
        self.sm = ScreenManager(transition=FadeTransition(duration=0.5))
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file("./Kv/splash.kv"))
        self.sm.add_widget(Builder.load_file("./Kv/login.kv"))
        self.sm.add_widget(Builder.load_file("./Kv/notify.kv"))

        # Create and add the floating image to the login screen
        floating_image = self.create_floating_image()
        floating_img = self.create_floating_img()
        floating = self.create_floating()

        login_screen = self.sm.get_screen(
            "Login"
        )  # Assuming 'login' is the name of the login screen
        login_screen.add_widget(floating_image)
        login_screen.add_widget(floating_img)
        login_screen.add_widget(floating)

        return self.sm

    # Define the disable_shortcut_keys function with the modifiers argument

    def on_start(self):
        self.start()

    def start(self):
        # Get references to the widgets
        screen = self.sm.get_screen("intro")
        label1 = screen.ids.label1
        icon1 = screen.ids.my_icon1
        label2 = screen.ids.label2
        label3 = screen.ids.label3

        # Perform animations
        anim_label1 = Animation(opacity=1, duration=3)
        anim_label1.bind(
            on_complete=lambda *args: self.hide_and_show(label1, icon1, label2, label3)
        )
        anim_label1.start(label1)

    def hide_and_show(self, label1, icon1, label2, label3):
        # Fade out label1 and set the others' opacity to 0
        anim_label1_out = Animation(opacity=0, duration=1)
        anim_icon1_out = Animation(opacity=0, duration=1)
        anim_label2_out = Animation(opacity=0, duration=1)
        anim_label3_out = Animation(opacity=0, duration=1)

        # Schedule the animations
        anim_label1_out.start(label1)
        anim_icon1_out.start(icon1)
        anim_label2_out.start(label2)
        anim_label3_out.start(label3)

        # Schedule the showing of icon1, label2, and label3 after 3 seconds
        Clock.schedule_once(lambda dt: self.show_and_redirect(icon1, label2, label3), 3)

    def show_and_redirect(self, icon1, label2, label3):
        # Show icon1, label2, and label3
        anim_icon1_in = Animation(opacity=1, duration=1)
        anim_label2_in = Animation(opacity=1, duration=1)
        anim_label3_in = Animation(opacity=1, duration=1)

        anim_icon1_in.start(icon1)
        anim_label2_in.start(label2)
        anim_label3_in.start(label3)

        # Redirect to 'login.kv' screen after 3 seconds
        Clock.schedule_once(lambda dt: self.redirect_to_login(), 3)

    def redirect_to_login(self):
        # Set the transition to FadeTransition for this change
        self.sm.transition = FadeTransition(duration=0.5)
        self.sm.current = "Login"

        # Revert back to NoTransition after the screen change
        Clock.schedule_once(
            lambda dt: setattr(self.sm, "transition", NoTransition()), 0.6
        )

    def create_floating_image(self):
        img = Image(source="img/elements/log.png")  # Adjust the image path as needed
        # Set the size of the image
        img.size_hint = (None, None)
        img.size = (200, 200)

        # Set the initial position using pos_hint
        img.pos_hint = {"center_x": 0.9, "center_y": 0.178}

        # Create an animation to continuously move the image up and down (floating effect)
        anim = Animation(pos_hint={"center_y": 0.178}, duration=2) + Animation(
            pos_hint={"center_y": 0.189}, duration=2
        )
        anim.repeat = True
        anim.start(img)

        return img

    def create_floating_img(self):
        img = Image(source="img/elements/js.png")  # Adjust the image path as needed
        # Set the size of the image
        img.size_hint = (None, None)
        img.size = (200, 200)

        # Set the initial position using pos_hint
        img.pos_hint = {"center_x": 0.87, "center_y": 0.11}

        # Create an animation to continuously move the image up and down (floating effect)
        anim = Animation(pos_hint={"center_y": 0.1}, duration=2) + Animation(
            pos_hint={"center_y": 0.12}, duration=2
        )
        anim.repeat = True
        anim.start(img)

        return img

    def create_floating(self):
        img = Image(source="img/elements/music.png")  # Adjust the image path as needed
        # Set the size of the image
        img.size_hint = (None, None)
        img.size = (900, 900)

        # Set the initial position using pos_hint
        img.pos_hint = {"center_x": 0.97, "center_y": 0.11}

        # Create an animation to continuously move the image up and down (floating effect)
        anim = Animation(pos_hint={"center_y": 0.11}, duration=2) + Animation(
            pos_hint={"center_y": 0.119}, duration=2
        )
        anim.repeat = True
        anim.start(img)

        return img

    def get_color(self, color_name):
        return self.theme_cls.get_color_from_name(color_name)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.test3.focus and keycode == 40:  # 40 - Enter key pressed
            self.abc()

    def abc(self):
        print("Test")

    # Python codeo
    def check_input_length(self):
        screen = self.sm.get_screen("Login")
        if screen:
            username_text = screen.ids.user.text if hasattr(screen.ids, "user") else ""
            password_text = (
                screen.ids.pass_s.text if hasattr(screen.ids, "pass_s") else ""
            )

            # Ensure both widgets exist before trying to access their text
            if hasattr(screen.ids, "login_button") and hasattr(
                screen.ids.login_button, "disabled"
            ):
                screen.ids.login_button.disabled = (
                    len(username_text) < 4 or len(password_text) < 4
                )

    def check_credentials(self):
        screen = self.sm.get_screen("Login")
        username = screen.ids.user.text
        password = screen.ids.pass_s.text

        def authenticate(username, password):
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username FROM user_info WHERE username = ? AND user_pass = ?",
                (username, password),
            )
            user = cursor.fetchone()
            conn.close()
            return user is not None

        import sys

        if authenticate(username, password):
            with open("credentials.txt", "w") as file:
                file.write(username)

            # Open notify.py
            subprocess.run([sys.executable, "notify.py"])

            # Stop the current process
            self._stop()
        else:
            self.show_error_dialog()

        if username == "Root" and password == "Root@in":
            # Open admin.py
            subprocess.run([sys.executable, "Admin.py"])
        else:
            pass

    def show_error_dialog(self):
        self.dialog = MDDialog(
            text="Incorrect username or password. Contact the admin.",
            buttons=[MDFlatButton(text="OK", on_release=self.dismiss_dialog)],
        )
        self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()


# Create an instance of Notify
app = Notify()


if __name__ == "__main__":
    Notify().run()

import base64
import imghdr
import sqlite3
from kivy.uix.image import Image
from kivymd.uix.textfield import MDTextField
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivy.properties import NumericProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.config import Config

Config.set("graphics", "resizable", False)

conn = sqlite3.connect("user.db")
cursor = conn.cursor()
# Query the database to retrieve the image data for the specified username


Window.resizable = False
sound = SoundLoader.load("./Sound/delete.mp3")


def read_img(file_path):
    with open(file_path, "rb") as f:
        photo_data = f.read()
    return photo_data


class ValuesFromDatabases(BoxLayout):
    pass


class MD3Card(MDCard):
    pass


class CustomMDTextField(MDTextField):
    min_text_length = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self._check_text_length)

    def _check_text_length(self, instance, value):
        if self.min_text_length is not None and len(value) < self.min_text_length:
            self.error = True
        else:
            self.error = False


class Admin(MDApp):
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.offset = 0
        self.num_entries = 0  # Initialize with 0 entries
        self.user_data_widgets = []  # To keep track of the widgets added for user data

    def refresh_page(self):
        self.load_page(self.offset)

    def clear_user_data(self):
        # Clear only the labels and images added for user data
        screen = self.sm.get_screen("view_screen")
        for widget in self.user_data_widgets:
            screen.remove_widget(widget)
        self.user_data_widgets = []

    def change_color_checkbox(self, active):
        screen = self.sm.get_screen("view_screen")
        if active:
            screen.ids.del_from_database.color = 1, 0, 0, 1  # Change color to red
        else:
            screen.ids.del_from_database.color = (
                0.5,
                0.5,
                0.5,
                1,
            )  # Change color back to default (gray)

    def load_page(self, offset=0):
        screen = self.sm.get_screen("view_screen")

        # Clear previous user data widgets if any
        for widget in screen.children[:]:
            if isinstance(
                widget, (Label, Image, MDIconButton)
            ):  # Also clear MDIconButtons
                screen.remove_widget(widget)

        cursor.execute("SELECT COUNT(*) FROM user_info")
        self.num_entries = cursor.fetchone()[0]  # Get the total number of entries

        screen.ids.new_total_value.text = f"({self.num_entries})"

        cursor.execute(
            "SELECT id, user_photo, username, user_pass, Date_user, Time_user FROM user_info ORDER BY id  LIMIT 6 OFFSET ?",
            (offset,),
        )
        user_data_list = cursor.fetchall()

        pos_y = 0.59

        # Define a dictionary to store user information
        self.user_info = {}

        # Iterate over the fetched data and add labels, icons accordingly
        for user_data in user_data_list:
            id_value, user_photo, username, password, date, time = user_data

            # Add ID label
            md_label_id = Label(
                text=f"{id_value}",
                color=(1, 1, 1, 1),
                bold=True,
                font_size="11sp",
                pos_hint={"center_x": 0.185, "center_y": pos_y},
                opacity=0.79,
            )
            screen.add_widget(md_label_id)
            # Increment the count for the next entry

            # Store the username value when creating the label
            md_label_username = Label(
                text=f"{username}",
                color=(1, 1, 1, 0.8),
                bold=True,
                font_size="11sp",
                pos_hint={"center_x": 0.33, "center_y": pos_y},
                opacity=0.79,
            )
            screen.add_widget(md_label_username)
            self.username_value = username

            # Display user photo
            if user_photo:
                image_base64 = base64.b64encode(user_photo).decode("utf-8")
                image_extension = imghdr.what(None, h=user_photo)

                image_widget = Image(
                    source=f"data:image/{image_extension};base64,{image_base64}",
                    size_hint=(None, None),
                    size=("36sp", "36sp"),
                    pos_hint={"center_x": 0.28, "center_y": pos_y},  # Adjusted pos_hint
                )

                screen.add_widget(image_widget)

                self.user_photo = image_extension
                self.user_p = image_base64

            # Hide the password
            hidden_pass = password[:3] + "*" * (len(password) - 3)
            # Add Password label
            md_label_password = Label(
                text=hidden_pass,
                color=(1, 1, 1, 0.8),
                bold=True,
                font_size="11sp",
                pos_hint={"center_x": 0.47, "center_y": pos_y},
                opacity=0.79,
            )
            screen.add_widget(md_label_password)

            # Add Date label
            md_label_date = Label(
                text=f"{date}",
                color=(1, 1, 1, 1),
                bold=True,
                font_size="11sp",
                pos_hint={"center_x": 0.63, "center_y": pos_y},
                opacity=0.79,
            )
            screen.add_widget(md_label_date)

            # Add Time label
            md_label_time = Label(
                text=f"{time}",
                color=(1, 1, 1, 1),
                bold=True,
                font_size="11sp",
                pos_hint={"center_x": 0.79, "center_y": pos_y},
                opacity=0.79,
            )
            screen.add_widget(md_label_time)

            edit = MDIconButton(
                icon="pencil",
                theme_text_color="Custom",
                icon_size="17sp",
                pos_hint={"center_x": 0.15, "center_y": pos_y},
                text_color=(1, 1, 1, 0.7),
            )
            # Add on_release event handler for delete button
            screen.add_widget(edit)
            edit.bind(
                on_release=lambda instance, user_data=user_data: self.edit_current(
                    instance, user_data
                )
            )

            # Add delete icon
            del_button = MDIconButton(
                icon="delete",
                theme_text_color="Custom",
                pos_hint={"center_x": 0.89, "center_y": pos_y},
                text_color=(1, 0, 0, 1),
            )
            # Add on_release event handler for delete button
            del_button.bind(
                on_release=lambda instance, id=id_value: self.delete_entry(id)
            )
            screen.add_widget(del_button)

            # Adjust position for the next entry
            pos_y -= 0.093

        # Disable next button if remaining entries are less than 6
        screen.ids.next.disabled = offset + 6 >= self.num_entries

    def edit_current(self, instance, user_data):
        # print("User data received:", user_data)
        id_value, user_photo, username, password, date, time = user_data
        # print("Username:", username)
        content_layout1 = BoxLayout(
            orientation="vertical", spacing="25dp", size_hint_y=None
        )  # Set size_hint_y to None

        if user_photo:
            image_base64 = base64.b64encode(user_photo).decode("utf-8")
            image_extension = imghdr.what(None, h=user_photo)
            image_source = f"data:image/{image_extension};base64,{image_base64}"
        else:
            pass

        # Add the image widget
        self.img = Image(
            source=image_source,
            size_hint=(None, None),
            size=("190sp", "190sp"),
            pos_hint={"center_x": 0.5},
        )
        content_layout1.add_widget(self.img)

        self.text = MDLabel(
            text="User Profile",
            theme_text_color="Custom",
            text_color=(0, 0.5, 1, 1),  # Blue color
            font_style="Body2",
            opacity=0.7,
            size_hint_y=None,
            height=dp(30),
            halign="center",
        )  # Center the label horizontally
        content_layout1.add_widget(self.text)

        self.img_widget3 = MDTextField(
            hint_text=f"{username}",
            opacity=0.3,
            icon_left="account",
            mode="rectangle",
            width=dp(1),
            size_hint_y=None,
            height=dp(48),
            disabled=True,
        )
        content_layout1.add_widget(self.img_widget3)

        self.img_widget = CustomMDTextField(
            hint_text="New Password",
            icon_left="key",
            mode="rectangle",
            size_hint_y=None,
            height=dp(48),
            min_text_length=4,
            max_text_length=10,
        )
        content_layout1.add_widget(self.img_widget)

        self.submit_button = MDRaisedButton(
            text="Edit Change",
            _min_width=700,
            size_hint_y=None,
            pos_hint={"center_x": 0.5},
            height=dp(40),
            disabled=True,
        )
        content_layout1.add_widget(self.submit_button)

        popup = Popup(
            title="Edit Information",
            title_align="center",
            content=content_layout1,
            size_hint=(None, None),
            size=(800, 1080),
            separator_height=0,
        )
        popup.title_font = "Roboto-Bold"
        popup.title_color = (1, 1, 1, 0.6)
        popup.open()

        # Bind the height of the BoxLayout to its minimum height
        content_layout1.bind(minimum_height=content_layout1.setter("height"))

        # Bind the button to the update_entry method
        self.submit_button.bind(
            on_release=lambda instance, popup=popup: self.update_entry(
                username, self.img_widget.text, popup
            )
        )
        # Listen for changes in the text input
        self.img_widget.bind(error=self._check_button_status)

    def _check_button_status(self, instance, value):
        self.submit_button.disabled = value

    def update_entry(self, user_name, update_pass, popup):
        # Execute SQL query to update the password
        cursor.execute(
            "UPDATE user_info SET user_pass = ? WHERE username = ?",
            (update_pass, user_name),
        )
        # Commit the transaction
        conn.commit()
        # Reload the page to reflect the changes
        self.load_page(self.offset)
        # Dismiss the popup
        popup.dismiss()

    def delete_entry(self, id):
        # Execute SQL query to delete entry with the given id
        cursor.execute("DELETE FROM user_info WHERE id = ?", (id,))
        # Commit the transaction
        conn.commit()
        # Reload the page to reflect the changes
        self.load_page(self.offset)

    def switch_to_next(self):
        self.offset += 6
        self.load_page(self.offset)

    def switch_to_previous(self):
        if self.offset >= 6:
            self.offset -= 6
            self.load_page(self.offset)
        else:
            self.offset = 0  # Reset offset if it goes below 0
            self.load_page(self.offset)

    def view_page(self):
        try:
            cursor.execute("SELECT COUNT(*) FROM user_info")
            cursor.fetchone()[
                0
            ]  # Fetch the first column of the first row (the count)

            cursor.execute(
                "SELECT id, username, user_pass, Date_user, Time_user FROM user_info"
            )

            user_data_list = cursor.fetchall()  # Fetch all user data including pictures

            screen = self.sm.get_screen("view_screen")

            # # Update the value of the 'new_total_value' id (assuming this is the correct id)

            # # Display each user's data
            # for user_data in user_data_list:
            #     id, username, password, date, time = user_data
            #     # Assign data from the database directly to the labels
            #     screen.add_widget(MDLabel(text=f"{id}\n \n \n \n ", pos_hint={"center_x": .55, "center_y": .52}))
            #     screen.add_widget(MDLabel(text=f"{username}\n \n \n \n ", pos_hint={"center_x": .5, "center_y": .52}))
            #     screen.add_widget(MDLabel(text=f"{password}\n \n \n \n ", pos_hint={"center_x": .3, "center_y": .52}))
            #     screen.add_widget(MDLabel(text=f"{date}\n \n \n \n ", pos_hint={"center_x": .4, "center_y": .52}))
            #     screen.add_widget(MDLabel(text=f"{time}\n \n \n \n ", pos_hint={"center_x": .5, "center_y": .52}))

            # Now let add the ids
            cursor.execute(
                "SELECT id, user_photo, username, user_pass, Date_user, Time_user FROM user_info LIMIT 6 "
            )
            user_data_list = cursor.fetchall()

            screen = self.sm.get_screen("view_screen")
            pos_y = 0.61

            # Iterate over the fetched data and add labels accordingly
            for user_data in user_data_list:
                id_value, user_photo, username, password, date, time = user_data

                # Add ID label
                md_label_id = Label(
                    text=f"{id_value}",
                    color=(1, 1, 1, 1),
                    bold=True,
                    font_size="11sp",
                    pos_hint={"center_x": 0.185, "center_y": pos_y},
                    opacity=0.79,
                )
                screen.add_widget(md_label_id)

                # Add Username label
                md_label_username = Label(
                    text=f"{username}",
                    color=(1, 1, 1, 0.8),
                    bold=True,
                    font_size="11sp",
                    pos_hint={"center_x": 0.33, "center_y": pos_y},
                    opacity=0.79,
                )
                screen.add_widget(md_label_username)

                # Display user photo
                if user_photo:
                    image_base64 = base64.b64encode(user_photo).decode("utf-8")
                    image_extension = imghdr.what(None, h=user_photo)

                    image_widget = Image(
                        source=f"data:image/{image_extension};base64,{image_base64}",
                        size_hint=(None, None),
                        size=("36sp", "36sp"),
                        pos_hint={
                            "center_x": 0.28,
                            "center_y": pos_y,
                        },  # Adjusted pos_hint
                        # keep_ratio=False,
                        # allow_stretch=True
                    )
                    screen.add_widget(image_widget)

                # Reduce the position hint for the next row

                # Hide the password
                hidden_pass = password[:5] + "*" * (len(password) - 5)
                # Add Password label
                md_label_password = Label(
                    text=hidden_pass,
                    color=(1, 1, 1, 0.8),
                    bold=True,
                    font_size="11sp",
                    pos_hint={"center_x": 0.509, "center_y": pos_y},
                    opacity=0.79,
                )
                screen.add_widget(md_label_password)

                # Reduce the position hint for the next row

                #
                # Add Date label
                md_label_date = Label(
                    text=f"{date}",
                    color=(1, 1, 1, 1),
                    bold=True,
                    font_size="11sp",
                    pos_hint={
                        "center_x": 0.699,
                        "center_y": pos_y,
                    },  # Adjusted position hint for date
                    opacity=0.79,
                )
                screen.add_widget(md_label_date)

                # Add Time label
                md_label_time = Label(
                    text=f"{time}",
                    color=(1, 1, 1, 1),
                    bold=True,
                    font_size="11sp",
                    pos_hint={
                        "center_x": 0.859,
                        "center_y": pos_y,
                    },  # Adjusted position hint for time
                    opacity=0.79,
                )
                screen.add_widget(md_label_time)

                # Reduce the position hint for the next row
                pos_y -= 0.1

            # #get the date
            # cursor.execute("SELECT Date_user FROM user_info LIMIT 6 ")
            # user_data_list = cursor.fetchall()

            # screen = self.sm.get_screen('view_screen')

            # #get the time
            # cursor.execute("SELECT TIme_user FROM user_info LIMIT 6 ")
            # user_data_list = cursor.fetchall()

            # screen = self.sm.get_screen('view_screen')

            # #in this we will add the img
            # cursor.execute("SELECT user_photo FROM user_info LIMIT 6 ")
            # user_data_list = cursor.fetchall()

            # screen = self.sm.get_screen('view_screen')

            # # Initial position hint
            # pos_y = 0.55

            # for image_data in user_data_list:
            #     image_base64 = base64.b64encode(image_data[0]).decode('utf-8')
            #     image_extension = imghdr.what(None, h=image_data[0])

            #     image_widget = Image(
            #         source=f'data:image/{image_extension};base64,{image_base64}',
            #         size_hint=(None, None),
            #         size=('36sp', '36sp'),
            #         pos_hint={"center_x": .28, "y": pos_y},  # Adjusted pos_hint
            #         # keep_ratio=False,
            #         # allow_stretch=True
            #     )

            #     screen.add_widget(image_widget)

            #     # Reduce the position hint for the next image
            #     pos_y -= 0.089

        except sqlite3.Error as e:
            print("SQLite error:", e)
        except Exception as e:
            print("Error:", e)

    def build(self):
        Window.size = [1200, 730]
        self.dialog = None
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        global sm
        self.sm = ScreenManager()
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(Builder.load_file("./Kv/admin/admin.kv"))
        self.sm.add_widget(Builder.load_file("./Kv/admin/view.kv"))
        self.sm.add_widget(Builder.load_file("./Kv/admin/add.kv"))
        self.sm.add_widget(Builder.load_file("./Kv/login.kv"))
        self.view_page()

        return self.sm

    def open_help_dialog(self):
        image_paths = [
            "./img/Final/helper_home.png",
            "./img/Final/helper_login.png",
            "./img/Final/helper_user.png",
            "./img/Final/helper_intro.png",
            "./img/Final/helper_admin_view.png",
            "./img/Final/Edit.png",
            "./img/Final/helper_view_page.png",
            "./img/Final/final.png",
            "./img/Final/Get_strt.png",
        ]

        self.image_index = 0  # Initialize image index

        content_layout1 = RelativeLayout()
        self.img_widget = Image(
            source=image_paths[self.image_index],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        content_layout1.add_widget(self.img_widget)

        # Create a button to change the image
        clear_button1 = MDFloatingActionButton(
            icon="chevron-right",
            size_hint=(None, None),
            size=(dp(150), dp(48)),
            pos_hint={"center_x": 0.92, "center_y": 0.1},
        )
        clear_button1.bind(on_release=self.change_image)
        content_layout1.add_widget(clear_button1)

        # Create the Popup window with the image content
        popup = Popup(
            title="ADMIN HELPER",
            title_align="center",
            content=content_layout1,
            size_hint=(None, None),
            size=(1440, 900),
            separator_height=6,
        )
        # Set the title font to bold
        popup.title_font = "Roboto-Bold"
        popup.title_color = 1, 1, 1, 0.6
        popup.open()

    def change_image(self, *args):
        image_paths = [
            "./img/Final/helper_home.png",
            "./img/Final/helper_login.png",
            "./img/Final/helper_user.png",
            "./img/Final/helper_intro.png",
            "./img/Final/helper_admin_view.png",
            "./img/Final/Edit.png",
            "./img/Final/helper_view_page.png",
            "./img/Final/final.png",
            "./img/Final/Get_strt.png",
        ]

        self.image_index = (self.image_index + 1) % len(
            image_paths
        )  # Increment the index cyclically

        # Change the source of the image widget
        self.img_widget.source = image_paths[self.image_index]

    def change(self):
        screen = self.sm.get_screen("view_screen")

        # Check if the icon is currently displayed
        mg_to_search = screen.ids.mg_to_search
        if isinstance(
            mg_to_search, TextInput
        ):  # If TextInput is already there, remove it and revert to the icon
            mg_to_search_parent = mg_to_search.parent
            mg_to_search_parent.remove_widget(mg_to_search)

            # Recreate the MDIconButton
            mg_to_search = MDIconButton(
                icon="magnify",
                theme_text_color="Custom",
                color=(0.5, 0.5, 0.5, 0.5),
                pos_hint={"center_x": 0.92, "center_y": 0.96},
                opacity=0.8,
            )

            # Add the MDIconButton back to the parent
            mg_to_search_parent.add_widget(mg_to_search)
        else:  # Otherwise, replace the icon with MDTextField
            mg_to_search_parent = mg_to_search.parent
            mg_to_search_parent.remove_widget(mg_to_search)

            # Create a MDTextField widget to replace the MDIconButton
            search_textfield = MDTextField(
                hint_text="Search",
                mode="line",
                max_text_length=1,
                icon_left="magnify",
                size_hint=(None, None),
                size=(450, 40),
                pos_hint={"center_x": 0.84, "center_y": 0.96},
            )

            # Add the MDTextField to the same parent as the MDIconButton
            mg_to_search_parent.add_widget(search_textfield)

    def open_file_chooser(self):
        # Create a file chooser with filters
        file_chooser = FileChooserIconView()
        # Bind the on_submit event to a method that updates the AsyncImage source
        file_chooser.bind(on_submit=self.update_image_source)
        file_chooser.path = "/Users/firozshaikh/Desktop/Data_science/Project/Desktop App/Python /Kivy/Desktop App/Notify"

        # Create a popup and add the file chooser to it
        popup = Popup(
            title="Select an Image",
            content=file_chooser,
            size_hint=(None, None),
            size=(1200, 600),
        )
        popup.open()

    def update_image_source(self, file_chooser, selected_file, touch, **kwargs):
        if selected_file:
            image_path = selected_file[0]  # Get the selected file path
            screen = self.sm.get_screen("add_sceen")

            # Update the image source using the image_path
            screen.ids.user_pic.source = image_path  # Replace 'your_image_id' with the actual ID of your image widget
            print(f"Selected file: {image_path}")
            return image_path

    # def reset_fields(self, *args):

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Confirmation",
                text="Are you sure you want to save changes?",
                buttons=[
                    MDFlatButton(text="Cancel", on_release=self.dismiss_dialog),
                    MDFlatButton(text="Yes", on_release=self.insert_data),
                ],
            )
        self.dialog.open()

    def insert_data(self, *args):
        screen = self.sm.get_screen(
            "add_sceen"
        )  # Assuming 'add_sceen' is the correct screen name
        if screen:
            username_text = (
                screen.ids.user_name.text if hasattr(screen.ids, "user_name") else ""
            )
            password_text = (
                screen.ids.pass_s.text if hasattr(screen.ids, "pass_s") else ""
            )
            image_source = (
                screen.ids.user_pic.source if hasattr(screen.ids, "user_pic") else ""
            )
            print(image_source)
            # Get current date
            current_date = datetime.now().date()

            # Get current time
            current_time = datetime.now().strftime("%I:%M:%S %p")

            # Ensure all necessary widgets exist before trying to access their properties
            if hasattr(screen.ids, "save_changes_button") and hasattr(
                screen.ids.save_changes_button, "disabled"
            ):
                save_changes_button = screen.ids.save_changes_button
                if len(username_text) >= 4 and len(password_text) >= 4:
                    save_changes_button.disabled = False
                else:
                    save_changes_button.disabled = True

            # Insert data into the database
            if username_text and password_text and image_source:
                # Read the image file
                photo_data = read_img(image_source)
                cursor.execute(
                    "INSERT INTO user_info (user_photo, username, user_pass, Date_user, Time_user) VALUES (?, ?, ?, ?, ?)",
                    (
                        photo_data,
                        username_text,
                        password_text,
                        current_date,
                        current_time,
                    ),
                )
                # Commit the transaction
                conn.commit()

                print("Data inserted successfully")

                default_image_path = "img/wans.png"  # Replace 'path_to_default_image.png' with your default image path
                screen.ids.user_pic.source = default_image_path

                current_screen = self.root.current

            # Access the 'main' screen and its search_field
            if current_screen == "add_sceen":
                main_screen = self.root.get_screen("add_sceen")
                pass_S = main_screen.ids.pass_s
                user_name = main_screen.ids.user_name

                pass_S.text = ""
                user_name.text = ""

                sound = SoundLoader.load("./Sound/ting.mp3")
                if sound:
                    sound.play()

                # Show confirmation dialog and insert data when "Yes" is clicked
                self.show_confirmation_dialog()

        self.dialog.dismiss()

    # def dismiss_dialog(self, *args):

    def switch_to_login(self):
        Window.borderless = True
        Window.fullscreen = "auto"  # Run in full-screen mode
        self.sm.current = "Login"

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
        import subprocess

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
            subprocess.run([sys.executable, "admin.py"])
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

    def switch_to_view_screen(self):
        # Switch to the view screen
        self.sm.current = "view_screen"

    def switch_to_add_sceen(self):
        # Switch to the view screen
        self.sm.current = "add_sceen"

    def switch_to_admin(self):
        # Switch to the view screen
        self.sm.current = "admin"

    def read_img(file_path):
        with open(file_path, "rb") as f:
            photo_data = f.read()

        return photo_data

    def check_submit_button_state(self):
        screen = self.sm.get_screen(
            "add_sceen"
        )  # Assuming 'add_sceen' is the correct screen name
        if screen:
            username_text = (
                screen.ids.user_name.text if hasattr(screen.ids, "user_name") else ""
            )
            password_text = (
                screen.ids.pass_s.text if hasattr(screen.ids, "pass_s") else ""
            )
            image_source = (
                screen.ids.user_pic.source if hasattr(screen.ids, "user_pic") else ""
            )
            print(image_source)
            # Get current date
            datetime.now().date()

            # Get current time
            datetime.now().strftime("%I:%M:%S %p")

            # Ensure all necessary widgets exist before trying to access their properties
        if hasattr(screen.ids, "save_changes_button") and hasattr(
            screen.ids.save_changes_button, "disabled"
        ):
            save_changes_button = screen.ids.save_changes_button
            if len(username_text) >= 4 and len(password_text) >= 4:
                save_changes_button.disabled = False
            else:
                save_changes_button.disabled = True

        # # Insert data into the database when the button is clicked
        # def insert_data(*args):
        #     if username_text and password_text and image_source:
        #         # Read the image file
        #         photo_data = read_img(image_source)
        #         cursor.execute('INSERT INTO user_info (user_photo, username, pass, Date_user, Time_user) VALUES (?, ?, ?, ?, ?)',
        #                         (photo_data, username_text, password_text, current_date, current_time))
        #         # Commit the transaction
        #         conn.commit()
        #         print("Data inserted successfully")

        # # Assign the insertion function to the button's on_release callback
        # save_changes_button.on_release = insert_data

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


# Create an instance of Notify
app = Admin()


if __name__ == "__main__":
    Admin().run()

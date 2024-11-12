import sqlite3
from flet import *
import flet
from flet_core import MainAxisAlignment


# Створюємо базу даних і таблицю користувачів
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS dishes
             (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL)''')
conn.commit()
conn.close()


class InputField(UserControl):
    def __init__(self, width, height, hint_text, icon, password=False):
        super().__init__()
        self.text_field = TextField(
            hint_text=hint_text,
            border=InputBorder.NONE,
            color='white',
            hint_style=TextStyle(
                color='white',
            ),
            height=height,
            width=width / 5 * 4,
            bgcolor='transparent',
            text_style=TextStyle(
                size=18,
                weight=FontWeight.W_400,
            ),
            password=password,
        )
        self.body = Container(
            Row([
                self.text_field,
                Icon(
                    icon,
                    color='white',
                )
            ]),
            border=border.all(1, '#44f4f4f4'),
            border_radius=18,
            bgcolor='transparent',
            alignment=alignment.center,
            width=width
        )

    def build(self):
        return self.body

    @property
    def value(self):
        return self.text_field.value

    @value.setter
    def value(self, value):
        self.text_field.value = value


class UserDatabase:
    @staticmethod
    def register_user(username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

    @staticmethod
    def login_user(username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        return user


class DishDatabase:
    @staticmethod
    def add_dish(name, description, price):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO dishes (name, description, price) VALUES (?, ?, ?)", (name, description, price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_dishes():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM dishes")
        dishes = c.fetchall()
        conn.close()
        return dishes

    @staticmethod
    def delete_dish(dish_id):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM dishes WHERE id=?", (dish_id,))
        conn.commit()
        conn.close()


class RegistrationPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.username_input = InputField(width=320, height=50, hint_text='Username', icon=icons.PERSON_ROUNDED)
        self.password_input = InputField(width=320, height=50, hint_text='Password', icon=icons.LOCK_ROUNDED, password=True)

    def build(self):
        return Container(
            Stack([
                Image(
                    src='C:/Users/Lenovo/Documents/VNTU/ООП/individual-task/menu_restaurant/ital-pizza.jpg',
                ),
                Container(
                    Container(
                        Column([
                            Row([
                                Text(
                                    "Registration",
                                    color='white',
                                    weight=FontWeight.W_700,
                                    size=26,
                                    text_align='center',
                                ),
                            ], alignment=MainAxisAlignment.CENTER),
                            Row([self.username_input], alignment=MainAxisAlignment.CENTER),
                            Row([self.password_input], alignment=MainAxisAlignment.CENTER),
                            Row([
                                ElevatedButton(
                                    text="Registration",
                                    color='black',
                                    bgcolor='white',
                                    width=320,
                                    height=50,
                                    on_click=self.register
                                )
                            ], alignment=MainAxisAlignment.CENTER),
                            Row([
                                Text(
                                    "Do you have an account?",
                                    color='white', size=16
                                ),
                                TextButton(
                                    text="Login",
                                    on_click=lambda e: self.page.go('/login'),
                                    style=ButtonStyle(
                                        color='white'
                                    )
                                )
                            ], alignment=MainAxisAlignment.CENTER, spacing=0),
                        ], alignment=MainAxisAlignment.CENTER),
                        width=400,
                        height=400,
                        blur=Blur(sigma_x=10, sigma_y=12, tile_mode=BlurTileMode.MIRROR),
                        border_radius=18,
                        border=border.all(1, '#44f4f4f4'),
                        bgcolor='#10f4f4f4',
                        alignment=alignment.center
                    ),
                    margin=margin.only(top=150),
                    alignment=alignment.center
                )
            ])
        )

    def register(self, e):
        username = self.username_input.value
        password = self.password_input.value
        UserDatabase.register_user(username, password)
        self.page.go('/login')


class LoginPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.username_input = InputField(width=320, height=50, hint_text='Username', icon=icons.PERSON_ROUNDED)
        self.password_input = InputField(width=320, height=50, hint_text='Password', icon=icons.LOCK_ROUNDED, password=True)

    def build(self):
        return Container(
            Stack([
                Image(
                    src='C:/Users/Lenovo/Documents/VNTU/ООП/individual-task/menu_restaurant/ital-pizza.jpg',
                ),
                Container(
                    Container(
                        Column([
                            Row([
                                Text(
                                    "Login",
                                    color='white',
                                    weight=FontWeight.W_700,
                                    size=26,
                                    text_align='center',
                                ),
                            ], alignment=MainAxisAlignment.CENTER),
                            Row([self.username_input], alignment=MainAxisAlignment.CENTER),
                            Row([self.password_input], alignment=MainAxisAlignment.CENTER),
                            Row([
                                ElevatedButton(
                                    text="Login",
                                    color='black',
                                    bgcolor='white',
                                    width=320,
                                    height=50,
                                    on_click=self.login
                                )
                            ], alignment=MainAxisAlignment.CENTER),
                            Row([
                                Text(
                                    "Don't have an account?",
                                    color='white', size=16
                                ),
                                TextButton(
                                    text="Register",
                                    on_click=lambda e: self.page.go('/'),
                                    style=ButtonStyle(
                                        color='white'
                                    )
                                )
                            ], alignment=MainAxisAlignment.CENTER, spacing=0),
                        ], alignment=MainAxisAlignment.CENTER),
                        width=400,
                        height=400,
                        blur=Blur(sigma_x=10, sigma_y=12, tile_mode=BlurTileMode.MIRROR),
                        border_radius=18,
                        border=border.all(1, '#44f4f4f4'),
                        bgcolor='#10f4f4f4',
                        alignment=alignment.center
                    ),
                    margin=margin.only(top=150),
                    alignment=alignment.center
                )
            ])
        )

    def login(self, e):
        username = self.username_input.value
        password = self.password_input.value
        user = UserDatabase.login_user(username, password)
        if user:
            self.page.go('/loading')
        else:
            self.page.snack_bar = SnackBar(Text("Invalid username or password"), open=True)
        self.page.update()


class LoadingScreen(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        self.page.go('/main_menu')
        return Container(
            Text("Loading...", color="white", size=24),
            alignment=alignment.center,
            bgcolor='black',
            width=self.page.window_width,
            height=self.page.window_height
        )


class MainMenu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return Container(
            Column([
                Row([
                    ElevatedButton(
                        text="Add Dish",
                        on_click=lambda e: self.page.go('/add_dish')
                    )
                ], alignment=MainAxisAlignment.CENTER),
                Row([
                    ElevatedButton(
                        text="View Menu",
                        on_click=lambda e: self.page.go('/view_menu')
                    )
                ], alignment=MainAxisAlignment.CENTER),
                Row([
                    ElevatedButton(
                        text="Delete Dish",
                        on_click=lambda e: self.page.go('/delete_dish')
                    )
                ], alignment=MainAxisAlignment.CENTER)
            ], alignment=MainAxisAlignment.CENTER),
            alignment=alignment.center
        )


class AddDishPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.name_input = InputField(width=320, height=50, hint_text='Dish Name', icon=icons.FOOD_BANK)
        self.description_input = InputField(width=320, height=50, hint_text='Description', icon=icons.DESCRIPTION)
        self.price_input = InputField(width=320, height=50, hint_text='Price', icon=icons.MONETIZATION_ON)

    def build(self):
        return Container(
            alignment=alignment.center,  # Центруємо всю сторінку
            padding=padding.all(20),  # Додаємо відступи
            content=Column([
                self._center_widget(self.name_input),
                self._center_widget(self.description_input),
                self._center_widget(self.price_input),
                Row([  # Центруємо кнопки
                    ElevatedButton(
                        text="Add Dish",
                        on_click=self.add_dish
                    ),
                    ElevatedButton(
                        text="Back to Menu",
                        on_click=lambda e: self.page.go('/main_menu')
                    )
                ], alignment=MainAxisAlignment.CENTER, spacing=10)
            ], alignment=MainAxisAlignment.CENTER),
        )

    def _center_widget(self, widget):
        return Container(
            alignment=alignment.center,  # Центруємо кожне поле
            content=widget
        )

    def add_dish(self, e):
        name = self.name_input.value
        description = self.description_input.value
        price = float(self.price_input.value)
        DishDatabase.add_dish(name, description, price)
        self.page.snack_bar = SnackBar(Text(f"Dish '{name}' added successfully!"), open=True)
        self.page.update()



class ViewMenuPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        dishes = DishDatabase.get_dishes()
        dish_list = Column([
            Row([
                Text(f"{dish[1]} - {dish[3]:.2f}₴"),
                Text(dish[2], italic=True)
            ], alignment=MainAxisAlignment.CENTER)
            for dish in dishes
        ], alignment=MainAxisAlignment.CENTER)

        return Container(
            alignment=alignment.center,  # Центруємо всю сторінку
            padding=padding.all(20),  # Додаємо відступи
            content=Column([
                Container(
                    content=Text("Menu", size=24, weight=FontWeight.W_700),
                    alignment=alignment.center  # Центруємо контейнер з текстом
                ),
                Container(
                    content=dish_list,
                    alignment=alignment.center  # Центруємо список страв
                ),
                Container(
                    content=ElevatedButton(
                        text="Back to Menu",
                        on_click=lambda e: self.page.go('/main_menu')
                    ),
                    alignment=alignment.center  # Центруємо контейнер з кнопкою
                )
            ], alignment=MainAxisAlignment.CENTER),
        )




class DeleteDishPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        dishes = DishDatabase.get_dishes()
        dish_options = [
            dropdown.Option(dish[1]) for dish in dishes
        ]
        self.dish_id_map = {dish[1]: dish[0] for dish in dishes}

        self.dish_dropdown = Dropdown(
            options=dish_options,
            label="Select Dish to Delete",
            width=320  # Фіксована ширина для випадаючого списку
        )

        return Container(
            alignment=alignment.center,  # Центруємо всю сторінку
            padding=padding.all(20),  # Додаємо відступи
            content=Column([
                Container(
                    content=self.dish_dropdown,
                    alignment=alignment.center  # Центруємо випадаючий список
                ),
                Row([  # Центруємо кнопки
                    ElevatedButton(
                        text="Delete Dish",
                        on_click=self.delete_dish
                    ),
                    ElevatedButton(
                        text="Back to Menu",
                        on_click=lambda e: self.page.go('/main_menu')
                    )
                ], alignment=MainAxisAlignment.CENTER, spacing=10)
            ], alignment=MainAxisAlignment.CENTER),
        )

    def delete_dish(self, e):
        selected_dish_name = self.dish_dropdown.value
        if selected_dish_name:
            selected_dish_id = self.dish_id_map[selected_dish_name]
            DishDatabase.delete_dish(selected_dish_id)
            self.page.snack_bar = SnackBar(Text(f"Dish '{selected_dish_name}' deleted successfully!"), open=True)
            self.page.update()





def main(page: Page):
    page.padding = 0
    page.window.resizable = False
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

    page.route = '/'

    def route_change(route):
        page.clean()
        if page.route == '/':
            page.add(RegistrationPage(page).build())
        elif page.route == '/login':
            page.add(LoginPage(page).build())
        elif page.route == '/loading':
            page.add(LoadingScreen(page).build())
        elif page.route == '/main_menu':
            page.add(MainMenu(page).build())
        elif page.route == '/add_dish':
            page.add(AddDishPage(page).build())
        elif page.route == '/view_menu':
            page.add(ViewMenuPage(page).build())
        elif page.route == '/delete_dish':
            page.add(DeleteDishPage(page).build())

    page.on_route_change = route_change
    route_change(page.route)

flet.app(target=main)

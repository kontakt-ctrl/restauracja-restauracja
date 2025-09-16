from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from db.menu import get_categories, get_items_by_category
from lang.translations import get_string

class MenuScreen(Screen):
    def __init__(self, lang="pl", on_add_to_cart=None, app=None, **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        self.on_add_to_cart = on_add_to_cart
        self.app = app
        self.selected_cat = None
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        layout = GridLayout(cols=2, padding=20, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        categories = get_categories(self.lang)
        for cat in categories:
            box = BoxLayout(orientation='vertical', size_hint=(1, None), height=220, spacing=5, padding=10)
            # Obsługa zdjęcia kategorii
            if cat.get("image_url"):
                box.add_widget(Image(source=cat["image_url"], size_hint_y=0.55))
            else:
                box.add_widget(Label(text="[ brak zdjęcia ]", size_hint_y=0.55, color=(.6, .6, .6, 1)))
            # Nazwa kategorii - tłumaczenie
            box.add_widget(Label(text=cat["name"], halign="center", font_size="18sp", color=(0.1,0.3,0.6,1), bold=True, size_hint_y=0.20))
            btn = Button(
                text=get_string("select_language", self.lang),
                background_color=(0.1, 0.7, 0.2, 1),
                color=(1,1,1,1),
                on_release=lambda inst, cid=cat["id"]: self.show_items(cid),
                size_hint_y=0.25
            )
            box.add_widget(btn)
            layout.add_widget(box)
        self.add_widget(layout)

    def show_items(self, category_id):
        self.clear_widgets()
        items = get_items_by_category(category_id, self.lang)
        layout = GridLayout(cols=1, padding=20, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for item in items:
            box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=110, spacing=8, padding=10)
            # Zdjęcie produktu
            if item.get("image_url"):
                box.add_widget(Image(source=item["image_url"], size_hint_x=0.35))
            else:
                box.add_widget(Label(text="[ brak zdjęcia ]", size_hint_x=0.35, color=(.7, .7, .7, 1)))
            info_box = BoxLayout(orientation="vertical", size_hint_x=0.45)
            info_box.add_widget(Label(
                text=item["name"],
                font_size="16sp",
                color=(0.2,0.2,0.2,1),
                halign="left",
                bold=True
            ))
            info_box.add_widget(Label(
                text=f"{item['price_cents']/100:.2f} PLN",
                font_size="14sp",
                color=(0.1,0.5,0.15,1),
                halign="left"
            ))
            box.add_widget(info_box)
            add_btn = Button(
                text=get_string("cart", self.lang) + " +",
                background_color=(0.1,0.5,0.7,1),
                color=(1,1,1,1),
                on_release=lambda inst, item_id=item["id"]: self.add_to_cart(item_id),
                size_hint_x=0.20
            )
            box.add_widget(add_btn)
            layout.add_widget(box)
        self.add_widget(layout)

    def add_to_cart(self, item_id):
        if self.on_add_to_cart:
            self.on_add_to_cart(item_id)

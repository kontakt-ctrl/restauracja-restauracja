from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from db.menu import get_items_by_category
from lang.translations import get_string
from db.orders import create_order

class CartScreen(Screen):
    def __init__(self, cart, on_order=None, app=None, lang="pl", **kwargs):
        super().__init__(**kwargs)
        self.cart = cart
        self.on_order = on_order
        self.app = app
        self.lang = lang
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        total = 0
        for item in self.cart:
            details = get_items_by_category(item["menu_item_id"], self.lang)
            if details:
                di = details[0]
                row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=70, spacing=8)
                # Miniaturka
                if di.get("image_url"):
                    row.add_widget(Image(source=di["image_url"], size_hint_x=0.25))
                else:
                    row.add_widget(Label(text="[ brak zdjęcia ]", size_hint_x=0.25, color=(.7, .7, .7, 1)))
                # Opis
                row.add_widget(Label(
                    text=f"{di['name']} x {item['quantity']} = {(di['price_cents']/100)*item['quantity']:.2f} PLN",
                    halign="left",
                    color=(0.15,0.15,0.15,1),
                    font_size="15sp"
                ))
                layout.add_widget(row)
                total += di['price_cents'] * item['quantity'] / 100
        layout.add_widget(Label(
            text=get_string("order_summary", self.lang) + f": {total:.2f} PLN",
            halign="right",
            font_size="16sp",
            color=(0.1, 0.5, 0.2, 1)
        ))
        order_btn = Button(
            text=get_string("pay_now", self.lang),
            background_color=(0.1, 0.6, 0.2, 1),
            color=(1,1,1,1),
            on_release=lambda inst: self.show_payment_popup(),
            size_hint_y=None,
            height=48
        )
        layout.add_widget(order_btn)
        self.add_widget(layout)

    def show_payment_popup(self):
        # Okno podsumowania zamówienia przed płatnością
        popup_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        total = 0
        for item in self.cart:
            details = get_items_by_category(item["menu_item_id"], self.lang)
            if details:
                di = details[0]
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=8)
                if di.get("image_url"):
                    row.add_widget(Image(source=di["image_url"], size_hint_x=0.22))
                else:
                    row.add_widget(Label(text="[ brak zdjęcia ]", size_hint_x=0.22, color=(.7, .7, .7, 1)))
                row.add_widget(Label(
                    text=f"{di['name']} x {item['quantity']} = {(di['price_cents']/100)*item['quantity']:.2f} PLN",
                    halign="left",
                    font_size="15sp"
                ))
                popup_layout.add_widget(row)
                total += di['price_cents'] * item['quantity'] / 100
        popup_layout.add_widget(Label(
            text=get_string("order_summary", self.lang) + f": {total:.2f} PLN",
            font_size="17sp",
            color=(0.1, 0.5, 0.2, 1)
        ))
        pay_btn = Button(
            text=get_string("pay_now", self.lang),
            background_color=(0.1, 0.6, 0.2, 1),
            color=(1,1,1,1),
            size_hint_y=None,
            height=48,
            on_release=lambda inst: self.make_order_and_close(popup)
        )
        popup_layout.add_widget(pay_btn)
        popup = Popup(title=get_string("order_summary", self.lang), content=popup_layout, size_hint=(None, None), size=(500, 420), auto_dismiss=False)
        popup.open()

    def make_order_and_close(self, popup):
        # Tworzenie nowego zamówienia
        create_order(self.cart, language=self.lang)
        if popup:
            popup.dismiss()
        if self.on_order:
            self.on_order(self.cart)

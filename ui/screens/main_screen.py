from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from lang.translations import get_string

LANGS = [
    {"code": "pl", "label": "Polski", "flag": "flags/pl.png"},
    {"code": "en", "label": "English", "flag": "flags/en.png"},
    {"code": "de", "label": "Deutsch", "flag": "flags/de.png"},
    {"code": "fr", "label": "Français", "flag": "flags/fr.png"},
    {"code": "es", "label": "Español", "flag": "flags/es.png"},
    {"code": "uk", "label": "Українська", "flag": "flags/uk.png"},
    {"code": "cs", "label": "Čeština", "flag": "flags/cs.png"},
    {"code": "sk", "label": "Slovenčina", "flag": "flags/sk.png"},
    {"code": "no", "label": "Norsk", "flag": "flags/no.png"},
    {"code": "sv", "label": "Svenska", "flag": "flags/sv.png"},
    {"code": "da", "label": "Dansk", "flag": "flags/da.png"},
    {"code": "ru", "label": "Русский", "flag": "flags/ru.png"},
    {"code": "zh", "label": "中文", "flag": "flags/zh.png"},
    {"code": "ja", "label": "日本語", "flag": "flags/ja.png"},
    {"code": "ar", "label": "العربية", "flag": "flags/ar.png"},
]

ORDER_TYPES = [
    {"code": "na_miejscu", "label": get_string("dine_in", "pl")},
    {"code": "na_wynos", "label": get_string("take_away", "pl")},
]

class MainScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.cart = []
        self.lang = "pl"
        self.selected_category_id = None
        self.order_type = None
        self.idle_timeout = 60
        self.popup_timeout = 15
        self.idle_event = None
        self.popup_event = None

        self.layout = BoxLayout(orientation="vertical")
        Window.bind(on_touch_down=self.on_user_activity)
        self.reset_idle_timer()




##
        # Logo
        self.logo_box = BoxLayout(orientation="vertical", size_hint_y=None, height=120, padding=10)
        self.logo_box.add_widget(Image(source="logo.png", allow_stretch=False, keep_ratio=True))
        self.layout.add_widget(self.logo_box)

        # Columns
        self.columns_box = BoxLayout(orientation="horizontal")

        # Left column
        self.left_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.4)
        with self.left_box_outer.canvas.before:
            Color(0.92, 0.95, 1, 1)
            self.left_rect = Rectangle()
        self.left_box_outer.bind(pos=self._update_left_rect, size=self._update_left_rect)
        self.left_top_spacer = Widget(size_hint_y=0.35)
        self.left_box = BoxLayout(orientation="vertical", size_hint_y=0.3, padding=[10,0,5,0], spacing=8)
        self.left_bottom_spacer = Widget(size_hint_y=0.35)
        self.left_box_outer.add_widget(self.left_top_spacer)
        self.left_box_outer.add_widget(self.left_box)
        self.left_box_outer.add_widget(self.left_bottom_spacer)
        self.columns_box.add_widget(self.left_box_outer)

        # Right column
        self.right_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.6)
        with self.right_box_outer.canvas.before:
            Color(0.98, 1, 0.95, 1)
            self.right_rect = Rectangle()
        self.right_box_outer.bind(pos=self._update_right_rect, size=self._update_right_rect)
        self.right_top_spacer = Widget(size_hint_y=0.35)
        self.right_box = BoxLayout(orientation="vertical", size_hint_y=0.3, padding=[5,0,10,0], spacing=8)
        self.right_bottom_spacer = Widget(size_hint_y=0.35)
        self.right_box_outer.add_widget(self.right_top_spacer)
        self.right_box_outer.add_widget(self.right_box)
        self.right_box_outer.add_widget(self.right_bottom_spacer)
        self.columns_box.add_widget(self.right_box_outer)

        self.layout.add_widget(self.columns_box)

        nav_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=70, padding=10, spacing=22)
        self.menu_btn = Button(text=get_string("menu", self.lang), on_release=self.show_menu, font_size="19sp")
        self.cart_btn = Button(text=self.get_cart_btn_text(), on_release=self.open_cart_popup, font_size="19sp")
        self.lang_btn = Button(text=get_string("select_language", self.lang), on_release=self.open_lang_popup, font_size="19sp")
        nav_bar.add_widget(self.menu_btn)
        nav_bar.add_widget(self.cart_btn)
        nav_bar.add_widget(self.lang_btn)
        self.layout.add_widget(nav_bar)

        self.add_widget(self.layout)
        Clock.schedule_once(lambda dt: self.show_order_type_popup(), 0.2)

    def reset_idle_timer(self, *args):
        if self.idle_event:
            self.idle_event.cancel()
        self.idle_event = Clock.schedule_once(self.show_idle_popup, self.idle_timeout)

    def on_user_activity(self, *args):
        if hasattr(self, 'idle_popup') and self.idle_popup and self.idle_popup._window:
            self.idle_popup.dismiss()
            if self.popup_event:
                self.popup_event.cancel()
        self.reset_idle_timer()

    def show_idle_popup(self, *args):
        msg = get_string("continue_order", self.lang)
        yes_text = get_string("yes", self.lang)
        no_text = get_string("no", self.lang)

        layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        layout.add_widget(Label(text=msg, font_size="28sp", halign="center", color=(.1,.1,.1,1)))
        btn_box = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=70)
        yes_btn = Button(text=yes_text, font_size="23sp", background_color=(0.1,0.6,0.2,1), color=(1,1,1,1))
        no_btn = Button(text=no_text, font_size="23sp", background_color=(0.8,0.1,0.1,1), color=(1,1,1,1))
        btn_box.add_widget(yes_btn)
        btn_box.add_widget(no_btn)
        layout.add_widget(btn_box)

        self.idle_popup = Popup(
            title=get_string("attention", self.lang),
            content=layout,
            auto_dismiss=False,
            size_hint=(None, None),
            size=(540, 320),
        )

        def continue_order(*_):
            self.idle_popup.dismiss()
            if self.popup_event:
                self.popup_event.cancel()
            self.reset_idle_timer()

        def reset_to_start(*_):
            self.idle_popup.dismiss()
            self.cart.clear()
            self.update_cart_btn()
            self.show_order_type_popup()
            self.reset_idle_timer()

        yes_btn.bind(on_release=continue_order)
        no_btn.bind(on_release=reset_to_start)

        self.idle_popup.open()
        self.popup_event = Clock.schedule_once(lambda *_: reset_to_start(), self.popup_timeout)

    def _update_left_rect(self, *args):
        self.left_rect.pos = self.left_box_outer.pos
        self.left_rect.size = self.left_box_outer.size

    def _update_right_rect(self, *args):
        self.right_rect.pos = self.right_box_outer.pos
        self.right_rect.size = self.right_box_outer.size

    def get_cart_btn_text(self):
        count = sum(item["quantity"] for item in self.cart)
        return f"{get_string('cart', self.lang)} [{count}]"

    def update_cart_btn(self):
        self.cart_btn.text = self.get_cart_btn_text()

    def refresh_ui_language(self):
        self.menu_btn.text = get_string("menu", self.lang)
        self.update_cart_btn()
        self.lang_btn.text = get_string("select_language", self.lang)




    def show_order_type_popup(self):
        from kivy.uix.anchorlayout import AnchorLayout
        from kivy.uix.image import Image
        from kivy.metrics import dp

        overlay = BoxLayout(orientation="vertical", spacing=0)
        with overlay.canvas.before:
            Color(1, 1, 1, 1)
            bg_rect = Rectangle(source="restaurant_bg2.png", size=overlay.size, pos=overlay.pos)
        def update_overlay_rect(*args):
            bg_rect.pos = overlay.pos
            bg_rect.size = overlay.size
        overlay.bind(pos=update_overlay_rect, size=update_overlay_rect)

        # --- LOGO NA GÓRZE - TAK SAMO JAK W MENU GŁÓWNYM ---
        logo_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=220, padding=10)
        with logo_box.canvas.before:
            Color(1, 1, 1, 0.33)
            logo_bg = RoundedRectangle(pos=logo_box.pos, size=logo_box.size, radius=[25])
            Color(0, 0, 0, 0.12)
            logo_shadow = RoundedRectangle(pos=(logo_box.x, logo_box.y-8), size=(logo_box.width, logo_box.height+16), radius=[30])
        def update_logo_bg(*args):
            logo_bg.pos = logo_box.pos
            logo_bg.size = logo_box.size
            logo_shadow.pos = (logo_box.x, logo_box.y-8)
            logo_shadow.size = (logo_box.width, logo_box.height+16)
        logo_box.bind(pos=update_logo_bg, size=update_logo_bg)
        logo_box.add_widget(Image(source="logo.png", allow_stretch=True, keep_ratio=True))
        overlay.add_widget(logo_box)

        # --- KOLUMNY (jak w menu) ---
        columns_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=150)  # <-- zmniejszona wysokość!
        #columns_box = BoxLayout(orientation="horizontal")
        left_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.4)
        with left_box_outer.canvas.before:
            Color(1, 1, 1, 0.22)
            left_bg = RoundedRectangle(pos=left_box_outer.pos, size=left_box_outer.size, radius=[18])
            leaf_pattern = Rectangle(
                source="leaves_pattern.png",
                pos=left_box_outer.pos,
                size=left_box_outer.size
            )
        def update_left_bg(*args):
            left_bg.pos = left_box_outer.pos
            left_bg.size = left_box_outer.size
            leaf_pattern.pos = left_box_outer.pos
            leaf_pattern.size = left_box_outer.size
        left_box_outer.bind(pos=update_left_bg, size=update_left_bg)
        left_box_outer.add_widget(Widget())
        right_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.6)
        with right_box_outer.canvas.before:
            Color(1, 1, 1, 0.18)
            right_bg = RoundedRectangle(pos=right_box_outer.pos, size=right_box_outer.size, radius=[18])
            utensil_pattern = Rectangle(
                source="utensil_pattern.png",
                pos=right_box_outer.pos,
                size=right_box_outer.size
            )
        def update_right_bg(*args):
            right_bg.pos = right_box_outer.pos
            right_bg.size = right_box_outer.size
            utensil_pattern.pos = right_box_outer.pos
            utensil_pattern.size = right_box_outer.size
        right_box_outer.bind(pos=update_right_bg, size=update_right_bg)
        right_box_outer.add_widget(Widget())
        columns_box.add_widget(left_box_outer)
        columns_box.add_widget(right_box_outer)
        overlay.add_widget(columns_box)

        # --- PRZYCISKI WYBORU TYP ZAMÓWIENIA, WELCOME ---
        center_box = BoxLayout(orientation="vertical", spacing=dp(36), padding=[dp(60), 0, dp(60), 0], size_hint=(1, 0.58))
        center_box.add_widget(Label(
            #text="CHANGE LANGUAGE",  # Stały tekst po angielsku
            text=get_string("welcome", self.lang),
            font_size="36sp",
            halign="center",
            color=(0.10, 0.18, 0.28, 1),
            size_hint_y=None,
            height=dp(80),
            bold=True
        ))
        dine_in_btn = Button(
            text=get_string("dine_in", self.lang),
            background_color=(0.12, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size="32sp",
            size_hint_y=None,
            height=dp(140),
            size_hint_x=1,
            bold=True,
            on_release=lambda inst: self.set_order_type("na_miejscu", order_type_popup)
        )
        take_away_btn = Button(
            text=get_string("take_away", self.lang),
            background_color=(0.15, 0.5, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size="32sp",
            size_hint_y=None,
            height=dp(140),
            size_hint_x=1,
            bold=True,
            on_release=lambda inst: self.set_order_type("na_wynos", order_type_popup)
        )
        center_box.add_widget(dine_in_btn)
        center_box.add_widget(take_away_btn)
        overlay.add_widget(center_box)

        # --- WYBÓR JĘZYKA ---
        lang_anchor = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, 1))
        lang_btn = Button(
            text="CHANGE LANGUAGE",  # Stały tekst po angielsku
            #text=get_string("select_language", self.lang),
            font_size="26sp",
            bold=True,
            color=(1, 0.843, 0, 1),
            background_color=(1, 0.843, 0, 1),
            border=(2, 2, 2, 2),
            size_hint=(None, None),
            size=(280, 70),
            on_release=lambda *_: self.open_lang_popup_in_order_type(order_type_popup)
        )
        lang_anchor.add_widget(lang_btn)
        overlay.add_widget(lang_anchor)

        order_type_popup = Popup(content=overlay, auto_dismiss=False, background='', size_hint=(1, 1))
        order_type_popup.open()


##


    def open_lang_popup_in_order_type(self, order_type_popup):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.image import Image
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView

        list_layout = BoxLayout(orientation="vertical", spacing=8, padding=[12,12,12,12], size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for lang in LANGS:
            row = BoxLayout(orientation="horizontal", spacing=16, size_hint_y=None, height=dp(64))
            row.add_widget(Image(source=lang["flag"], size_hint_x=None, width=dp(56), allow_stretch=True))
            lang_btn = Button(
                text="        " + lang["label"],
                font_size="25sp",
                bold=True,
                color=(1,1,1,1),
                background_normal="",
                background_color=(0.20,0.25,0.55,0.45),
                size_hint_y=None,
                height=dp(56),
                size_hint_x=1,
                on_release=lambda inst, code=lang["code"]: set_language_in_popup(code),
                halign="left"
            )
            row.add_widget(lang_btn)
            list_layout.add_widget(row)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll.add_widget(list_layout)

        lang_popup = Popup(
            title=get_string("select_language", self.lang),
            content=scroll,
            size_hint=(0.8, 0.8),
            auto_dismiss=False
        )
        def set_language_in_popup(code):
            self.lang = code
            lang_popup.dismiss()
            order_type_popup.dismiss()
            self.refresh_ui_language()
            self.show_order_type_popup()
        lang_popup.open()


##

    def _update_bg_rect_popup(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size

    def set_order_type(self, type_value, popup):
        self.order_type = type_value
        popup.dismiss()
        self.show_menu()



    def show_menu(self, *args):
        self.layout.clear_widgets()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(source="restaurant_bg.png", pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

        # Logo
        self.logo_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=220, padding=10)
        with self.logo_box.canvas.before:
            Color(1, 1, 1, 0.33)
            self.logo_bg = RoundedRectangle(pos=self.logo_box.pos, size=self.logo_box.size, radius=[25])
            Color(0, 0, 0, 0.12)
            self.logo_shadow = RoundedRectangle(pos=(self.logo_box.x, self.logo_box.y-8), size=(self.logo_box.width, self.logo_box.height+16), radius=[30])
        self.logo_box.bind(pos=self._update_logo_bg, size=self._update_logo_bg)
        def animate_shadow(*args):
            import math, time
            offset = 8 + 4 * math.sin(time.time())
            self.logo_shadow.pos = (self.logo_box.x, self.logo_box.y-offset)
        from kivy.clock import Clock
        Clock.schedule_interval(animate_shadow, 1/30)
        self.logo_box.add_widget(Image(source="logo.png", allow_stretch=True, keep_ratio=True))
        self.layout.add_widget(self.logo_box)

        # Columns
        self.columns_box = BoxLayout(orientation="horizontal")
        # Left column
        self.left_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.4)
        self.left_top_spacer = Widget(size_hint_y=0.15)
        self.left_box = BoxLayout(orientation="vertical", size_hint_y=0.3, padding=[10,0,5,0], spacing=8)
        self.left_bottom_spacer = Widget(size_hint_y=0.45)
        self.left_box_outer.add_widget(self.left_top_spacer)
        self.left_box_outer.add_widget(self.left_box)
        self.left_box_outer.add_widget(self.left_bottom_spacer)
        self.columns_box.add_widget(self.left_box_outer)
        # Right column
        self.right_box_outer = BoxLayout(orientation="vertical", size_hint_x=0.6)
        with self.right_box_outer.canvas.before:
            Color(1, 1, 1, 0.18)
            self.right_bg = RoundedRectangle(pos=self.right_box_outer.pos, size=self.right_box_outer.size, radius=[18])
            self.utensil_pattern = Rectangle(
                source="utensil_pattern.png",
                pos=self.right_box_outer.pos,
                size=self.right_box_outer.size
            )
        self.right_box_outer.bind(pos=self._update_right_bg, size=self._update_right_bg)
        self.right_top_spacer = Widget(size_hint_y=0.15)
        self.right_box = BoxLayout(orientation="vertical", size_hint_y=0.3, padding=[5,0,10,0], spacing=8)
        self.right_bottom_spacer = Widget(size_hint_y=0.45)
        self.right_box_outer.add_widget(self.right_top_spacer)
        self.right_box_outer.add_widget(self.right_box)
        self.right_box_outer.add_widget(self.right_bottom_spacer)
        self.columns_box.add_widget(self.right_box_outer)
        self.layout.add_widget(self.columns_box)

        # Nawigacja
        nav_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=70, padding=10, spacing=22)
        self.menu_btn = Button(text=get_string("menu", self.lang), on_release=self.show_menu, font_size="19sp")
        self.cart_btn = Button(text=self.get_cart_btn_text(), on_release=self.open_cart_popup, font_size="19sp")
        self.lang_btn = Button(text=get_string("select_language", self.lang), on_release=self.open_lang_popup, font_size="19sp")
        nav_bar.add_widget(self.menu_btn)
        nav_bar.add_widget(self.cart_btn)
        nav_bar.add_widget(self.lang_btn)
        self.layout.add_widget(nav_bar)

        # Kategorie po lewej stronie
        from db.menu import get_categories
        categories = get_categories(self.lang)
        self.left_box.clear_widgets()
        for cat in categories:
            cat_box = BoxLayout(orientation="horizontal", size_hint=(1, None), height=90, spacing=12, padding=[4,4,4,4])
            # Zdjęcie kategorii
            if cat.get("image_url"):
                cat_img = Image(source=cat["image_url"], size_hint=(None, 1), width=70, allow_stretch=True, keep_ratio=True)
            else:
                cat_img = Label(text="[Brak zdjęcia]", size_hint=(None, 1), width=70, color=(1, 1, 1, 1))
            cat_box.add_widget(cat_img)
            # Przycisk kategorii
            cat_btn = Button(
                text=cat["name"].upper(),
                font_size="30sp",
                bold=True,
                halign="center",
                valign="middle",
                background_color=(1, 1, 1, 1),
                color=(0,0,0,1),
                background_normal="",
                size_hint=(1, 1),
                on_release=lambda inst, cid=cat["id"]: self.show_products(cid)
            )
            cat_btn.bind(
                size=lambda instance, value: setattr(instance, 'text_size', instance.size)
            )
            cat_box.add_widget(cat_btn)
            # Ramka
            with cat_box.canvas.before:
                Color(1, 1, 1, 1)
                cat_box._border = RoundedRectangle(pos=cat_box.pos, size=cat_box.size, radius=[13], width=1)
            cat_box.bind(pos=lambda obj,*a: setattr(obj._border, 'pos', obj.pos))
            cat_box.bind(size=lambda obj,*a: setattr(obj._border, 'size', obj.size))
            self.left_box.add_widget(cat_box)
        self.right_box.clear_widgets()

        # --- DUŻY PRZYCISK ANULUJ ZAMÓWIENIE na dole ---
        cancel_btn = Button(
            text=get_string("cancel_order", self.lang),
            font_size="32sp",
            bold=True,
            background_color=(0.85, 0.2, 0.25, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=96,
            on_release=lambda inst: self.cancel_order_and_reset()
        )
        self.layout.add_widget(cancel_btn)

    def cancel_order_and_reset(self):
        self.cart.clear()
        self.order_type = None
        self.update_cart_btn()
        self.show_order_type_popup()


##

    def _update_bg_rect(self, *args):
        self.bg_rect.pos = self.layout.pos
        self.bg_rect.size = self.layout.size

    def _update_logo_bg(self, *args):
        self.logo_bg.pos = self.logo_box.pos
        self.logo_bg.size = self.logo_box.size
        self.logo_shadow.pos = (self.logo_box.x, self.logo_box.y-8)
        self.logo_shadow.size = (self.logo_box.width, self.logo_box.height+16)

    def _update_left_bg(self, *args):
        self.left_bg.pos = self.left_box_outer.pos
        self.left_bg.size = self.left_box_outer.size
        self.leaf_pattern.pos = self.left_box_outer.pos
        self.leaf_pattern.size = self.left_box_outer.size

    def _update_right_bg(self, *args):
        self.right_bg.pos = self.right_box_outer.pos
        self.right_bg.size = self.right_box_outer.size
        self.utensil_pattern.pos = self.right_box_outer.pos
        self.utensil_pattern.size = self.right_box_outer.size


    def show_products(self, category_id):
        self.selected_category_id = category_id
        self.right_box.clear_widgets()
        from db.menu import get_items_by_category
        items = get_items_by_category(category_id, self.lang)
        for item in items:
            def on_add(inst, item_id=item["id"], img_src=item.get("image_url")):
                self.add_to_cart(item_id, inst, img_src)
            product_btn = Button(
                background_normal="",
                background_color=(0.18, 0.21, 0.24, 1),  # ciemnoszare, ale nie czarne!
                size_hint=(1, None),
                height=110,
                on_release=on_add
            )
            row = BoxLayout(orientation="horizontal", spacing=12, padding=[8,8,8,8])
            if item.get("image_url"):
                img = Image(source=item["image_url"], size_hint=(None, 1), width=90, allow_stretch=True)
            else:
                img = Label(text="[Brak zdjęcia]", size_hint=(None, 1), width=90, color=(.7, .7, .7, 1))
            row.add_widget(img)
            info = BoxLayout(orientation="vertical", spacing=3, padding=[6,0,0,0])
            name_lbl = Label(
                text=item["name"].upper(),
                font_size="26sp",
                bold=True,
                color=(1,1,1,1),
                halign="left",
                valign="top",
                size_hint_y=None,
                height=36
            )
            name_lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
            info.add_widget(name_lbl)
            ingredients = item.get("ingredients")
            if ingredients and ingredients.strip():
                ingredients_lbl = Label(
                    text=ingredients,
                    font_size="15sp",
                    color=(0.98,0.85,0.15,1),
                    halign="left",
                    valign="top",
                    size_hint_y=None,
                    height=22
                )
            else:
                ingredients_lbl = Label(
                    text="[Brak danych o składnikach]",
                    font_size="15sp",
                    color=(0.6,0.55,0.55,1),
                    halign="left",
                    valign="top",
                    size_hint_y=None,
                    height=22
                )
            ingredients_lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
            info.add_widget(ingredients_lbl)
            price_lbl = Label(
                text=f"{item.get('price_cents',0)/100:.2f} PLN   +",
                font_size="19sp",
                color=(1,1,1,1),
                bold=True,
                halign="right",
                valign="bottom",
                size_hint_y=None,
                height=32
            )
            price_lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
            info.add_widget(price_lbl)
            row.add_widget(info)
            product_btn.add_widget(row)
            with product_btn.canvas.before:
                Color(1, 0.85, 0.15, 1)
                product_btn._border = RoundedRectangle(pos=product_btn.pos, size=product_btn.size, radius=[13], width=2)
            product_btn.bind(pos=lambda obj,*a: setattr(obj._border, 'pos', obj.pos))
            product_btn.bind(size=lambda obj,*a: setattr(obj._border, 'size', obj.size))
            self.right_box.add_widget(product_btn)
##

    def open_cart_popup(self, *args):
        from kivy.uix.scrollview import ScrollView
        from kivy.core.window import Window

        popup_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        from db.menu import get_item_by_id
        total = 0

        def refresh_cart_popup():
            cart_popup.dismiss()
            self.open_cart_popup()

        for entry in self.cart:
            item = get_item_by_id(entry["menu_item_id"], self.lang)
            if item:
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=5)
                if item.get("image_url"):
                    row.add_widget(Image(source=item["image_url"], size_hint_x=0.26))
                else:
                    row.add_widget(Label(text="[Brak zdjęcia]", size_hint_x=0.26, color=(.7, .7, .7, 1)))
                row.add_widget(Label(
                    text=f"{item['name']} x {entry['quantity']} = {(item['price_cents']/100)*entry['quantity']:.2f} PLN",
                    halign="left",
                    font_size="15sp"
                ))
                remove_btn = Button(
                    text=get_string("remove", self.lang),
                    size_hint_x=None,
                    width=90,
                    background_color=(0.8,0.1,0.1,1),
                    color=(1,1,1,1),
                    on_release=lambda inst, item_id=item["id"]: self.remove_from_cart(item_id, refresh_cart_popup)
                )
                row.add_widget(remove_btn)
                popup_layout.add_widget(row)
                total += item['price_cents'] * entry['quantity'] / 100
        popup_layout.add_widget(Label(text=f"{get_string('order_summary', self.lang)}: {total:.2f} PLN", font_size="16sp", color=(0.1, 0.5, 0.2, 1)))
        btns_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=56, spacing=18)
        btns_box.add_widget(Button(text=get_string("back", self.lang), on_release=lambda inst: cart_popup.dismiss()))
        btns_box.add_widget(Button(
            text=get_string("pay", self.lang),
            background_color=(0.1,0.6,0.2,1),
            color=(1,1,1,1),
            on_release=lambda inst: self.pay_order(cart_popup)
        ))
        popup_layout.add_widget(btns_box)

        # Rozmiar: 80% wysokości ekranu
        popup_height = int(Window.height * 0.65)
        popup_width = int(Window.width * 0.6)

        cart_popup = Popup(
            title=get_string("your_cart", self.lang),
            content=popup_layout,
            size_hint=(None, None),
            size=(popup_width, popup_height),
            auto_dismiss=False
        )
        cart_popup.open()


##


    def remove_from_cart(self, item_id, refresh_callback=None):
        self.cart = [entry for entry in self.cart if entry["menu_item_id"] != item_id]
        self.update_cart_btn()
        if refresh_callback:
            refresh_callback()

    def pay_order(self, cart_popup):
        cart_popup.dismiss()
        from db.orders import create_order
        from db.models import get_session, Order
        order_id = create_order(self.cart, language=self.lang, type=self.order_type)
        session = get_session()
        try:
            order = session.query(Order).filter_by(id=order_id).first()
            if order:
                order_number = order.order_number
            else:
                order_number = "???"
        finally:
            session.close()
        self.cart.clear()
        self.update_cart_btn()
        self.show_order_info_popup(order_number)





# ... (reszta pliku jak dotąd)


    def show_order_info_popup(self, order_number):
        from kivy.core.window import Window
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.popup import Popup
        from kivy.metrics import dp
        from kivy.graphics import Rectangle

        popup_width = int(Window.width * 0.7)
        popup_height = int(Window.height * 0.6)

        layout = BoxLayout(
            orientation="vertical",
            padding=[0, dp(60), 0, dp(60)],
            spacing=dp(40),
            size_hint=(1, 1)
        )

        with layout.canvas.before:
            layout.bg_rect = Rectangle(source="restaurant_bg3.png", pos=layout.pos, size=layout.size)
        def update_bg_rect(instance, value):
            layout.bg_rect.pos = layout.pos
            layout.bg_rect.size = layout.size
        layout.bind(pos=update_bg_rect, size=update_bg_rect)

        label = Label(
            text=f"TWÓJ NUMER ZAMÓWIENIA: {order_number}",
            font_size="64sp",
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            bold=True,
            size_hint=(1, 1)
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        layout.add_widget(label)

        btn = Button(
            text="ZAMKNIJ",
            font_size="36sp",
            background_color=(0, 0, 0, 0.4),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            width=dp(260),
            height=dp(90),
            pos_hint={"center_x": 0.5},
            bold=True
        )
        layout.add_widget(btn)

        popup = Popup(
            title="",
            content=layout,
            size_hint=(None, None),
            size=(popup_width, popup_height),
            auto_dismiss=False,
            background='',
        )

        def close_popup(*args):
            popup.dismiss()
            self.show_order_type_popup()

        btn.bind(on_release=close_popup)
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: close_popup(), 30)
        popup.open()



##

    def open_lang_popup(self, *args):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.image import Image
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView

        list_layout = BoxLayout(orientation="vertical", spacing=8, padding=[12,12,12,12], size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for lang in LANGS:
            row = BoxLayout(orientation="horizontal", spacing=16, size_hint_y=None, height=dp(64))
            row.add_widget(Image(source=lang["flag"], size_hint_x=None, width=dp(56), allow_stretch=True))
            lang_btn = Button(
                text="        " + lang["label"],
                font_size="25sp",
                bold=True,
                color=(0,0,0,1),
                background_color=(1,1,1,1),
                background_normal="",
                size_hint_y=None,
                height=dp(56),
                size_hint_x=1,
                on_release=lambda inst, code=lang["code"]: self.set_language(code, lang_popup),
                halign="left"
            )
            row.add_widget(lang_btn)
            list_layout.add_widget(row)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll.add_widget(list_layout)

        lang_popup = Popup(
            title=get_string("select_language", self.lang),
            content=scroll,
            size_hint=(0.5, 0.6),
            auto_dismiss=False
        )
        lang_popup.open()

    def set_language(self, code, lang_popup):
        self.lang = code
        lang_popup.dismiss()
        self.refresh_ui_language()
        self.show_menu()





    def add_to_cart(self, item_id, start_widget=None, image_source=None):
        found = next((i for i in self.cart if i["menu_item_id"] == item_id), None)
        if found:
            found["quantity"] += 1
        else:
            self.cart.append({"menu_item_id": item_id, "quantity": 1})
        self.update_cart_btn()
        if start_widget is not None:
            self.fly_to_cart_animation(start_widget, image_source)



##

    def fly_to_cart_animation(self, start_widget, image_source=None):
        from kivy.uix.image import Image
        from kivy.uix.widget import Widget
        from kivy.animation import Animation

        # Wyznacz globalną pozycję startową (środek widgetu produktu)
        sx, sy = start_widget.to_window(start_widget.center_x, start_widget.center_y, initial=True)
        # Pozycja końcowa - środek przycisku koszyka
        ex, ey = self.cart_btn.to_window(self.cart_btn.center_x, self.cart_btn.center_y, initial=True)
        # Przekształć te współrzędne na współrzędne rodzica layoutu (potrzebne do overlay)
        px, py = self.layout.to_widget(sx, sy, relative=True)
        pex, pey = self.layout.to_widget(ex, ey, relative=True)

        # Stwórz obrazek (miniatura produktu) lub kolorowe kółko
        if image_source:
            img = Image(source=image_source, size_hint=(None, None), size=(56, 56), allow_stretch=True)
        else:
            from kivy.uix.label import Label
            img = Label(text="+", font_size="48sp", color=(1, .5, .2, 1), size_hint=(None, None), size=(56, 56), bold=True)
            with img.canvas.before:
                from kivy.graphics import Color, Ellipse
                Color(1, 0.7, 0.2, 0.9)
                img._ellipse = Ellipse(pos=img.pos, size=img.size)
            img.bind(pos=lambda instance, val: setattr(img._ellipse, "pos", instance.pos))
            img.bind(size=lambda instance, val: setattr(img._ellipse, "size", instance.size))

        # Dodaj do głównego layoutu (na wierzchu)
        self.layout.add_widget(img)
        img.pos = (px - img.width/2, py - img.height/2)

        # Animacja - szybki lot do koszyka + zmniejszenie + fade out
        anim = Animation(
            x=pex - img.width/2,
            y=pey - img.height/2,
            size=(100, 100),
            opacity=0.0,
            duration=0.55,
            t="out_quad"
        )
        def on_anim_complete(*_):
            if img.parent:
                img.parent.remove_widget(img)
        anim.bind(on_complete=on_anim_complete)
        anim.start(img)

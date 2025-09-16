from kivymd.app import MDApp
import os
from kivy.core.window import Window
from ui.screens.main_screen import MainScreen
from ui.screens.orders_screen import OrdersScreen

class TranslatorApp(MDApp):
    def build(self):
        instance = os.environ.get("INSTANCE", "A")
        if instance == "A":
            Window.size = (1024, 768)
            Window.left = 0
            Window.top = 0
        else:
            Window.size = (1080, 1920)
            Window.left = 1024
            Window.top = 0
        Window.borderless = True
        Window.fullscreen = 'auto'  # zamiast True!
        Window.set_title(f"Translator Restauracja {instance}")
        try:
            Window.show()
        except Exception:
            pass
        try:
            Window.raise_window()
        except Exception:
            pass

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.language = "pl"
        if instance == "A":
            return OrdersScreen(lang=self.language)
        else:
            return MainScreen(app=self)

TranslatorApp().run()

from kivymd.uix.screen import MDScreen
from db.menu import get_categories, get_items_by_category

class CategoryScreen(MDScreen):
    def __init__(self, lang="pl", **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        self.build_screen()

    def build_screen(self):
        categories = get_categories(self.lang)
        # Wyświetl kategorie po lewej
        for cat in categories:
            # Dodaj przyciski/karty kategorii do GUI
            pass

    def show_items(self, category_id):
        items = get_items_by_category(category_id, self.lang)
        # Wyświetl produkty z wybranej kategorii
        for item in items:
            # Dodaj do GUI np. zdjęcia, nazwy, ceny
            pass
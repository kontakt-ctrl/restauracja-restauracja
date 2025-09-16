from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from db.orders import get_orders
from lang.translations import get_string

class QueueScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_queue()

    def build_queue(self):
        self.clear_widgets()
        # Dopasuj kwerendę get_orders() do tego, co zwraca Twoja funkcja!
        ready_orders = get_orders(status="ready")
        pending_orders = get_orders(status="pending")
        box = MDBoxLayout(orientation="vertical")
        box.add_widget(MDLabel(text=get_string("ready_orders", "pl"), theme_text_color="Custom", text_color=(0.1, 0.7, 0.2, 1), font_style="H5"))
        for i, order in enumerate(ready_orders):
            lbl = MDLabel(text=f"{order.order_number}", theme_text_color="Custom", text_color=(0.1, 0.7, 0.2, 1))
            box.add_widget(lbl)
        box.add_widget(MDLabel(text=get_string("pending_orders", "pl"), theme_text_color="Custom", text_color=(0.8, 0.5, 0.1, 1), font_style="H6"))
        for order in pending_orders:
            box.add_widget(MDLabel(text=f"{order.order_number}", theme_text_color="Custom", text_color=(0.8, 0.5, 0.1, 1)))
        self.add_widget(box)

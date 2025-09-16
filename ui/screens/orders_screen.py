from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Line, RoundedRectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
from db.orders import get_orders
from datetime import datetime, timedelta
from kivy.properties import ColorProperty

class AnimatedDivider(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_color = [0.6, 0.6, 0.9, 1]
        Clock.schedule_interval(self.animate_line, 0.7)
        self.bind(pos=self.update_line, size=self.update_line)

    def animate_line(self, dt):
        anim = Animation(line_color=[0.2, 0.7, 1, 1], duration=0.35) + Animation(line_color=[0.6, 0.6, 0.9, 1], duration=0.35)
        anim.start(self)

    def update_line(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.line_color)
            Line(points=[self.center_x, self.y, self.center_x, self.top], width=5)

class OrderCard(BoxLayout):
    bg_color = ColorProperty([1, 1, 1, 1])
    def __init__(self, order_number, is_new=False, ready=False, **kwargs):
        super().__init__(orientation="vertical", padding=8, spacing=0, **kwargs)
        self.order_number = order_number
        self.is_new = is_new
        self.ready = ready

        self.bg_color = [1, 0.6, 0.1, 1] if not ready else [0.85, 1, 0.85, 1]
        if is_new and not ready:
            self.bg_color = [1, 1, 0.2, 1]
            self.animate_bg()
        self.bind(pos=self.draw_bg, size=self.draw_bg)

        lbl = Label(
            text=str(order_number),
            font_size="32sp",
            bold=True,
            color=(0.95,0.35,0.07,1) if not ready else (0.1,0.7,0.2,1),
            halign="center",
            valign="middle"
        )
        self.add_widget(lbl)

    def animate_bg(self):
        self.anim_start_time = datetime.utcnow()
        def blink_anim(*args):
            if datetime.utcnow() - self.anim_start_time > timedelta(seconds=30):
                self.bg_color = [1, 0.6, 0.1, 1]
                self.unbind(bg_color=self.draw_bg)
                return False
            else:
                anim = Animation(bg_color=[1, 0.8, 0.1, 1], duration=0.4) + Animation(bg_color=[1, 1, 0.2, 1], duration=0.4)
                anim.repeat = False
                anim.start(self)
                return True
        self.bind(bg_color=self.draw_bg)
        Clock.schedule_interval(blink_anim, 0.8)
        blink_anim()

    def draw_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[18,])

class BlinkingLabel(Label):
    def __init__(self, blink_color_1=(1,1,1,1), blink_color_2=(1,1,1,0.2), **kwargs):
        super().__init__(**kwargs)
        self.blink_color_1 = blink_color_1
        self.blink_color_2 = blink_color_2
        self.color = self.blink_color_1
        self.anim = None
        Clock.schedule_once(lambda dt: self.start_blinking(), 0)

    def start_blinking(self):
        self.anim = Animation(color=self.blink_color_2, duration=0.5) + Animation(color=self.blink_color_1, duration=0.5)
        self.anim.repeat = True
        self.anim.start(self)

class GradientBox(BoxLayout):
    """BoxLayout z gradient jako tło"""
    def __init__(self, gradient_file, **kwargs):
        super().__init__(**kwargs)
        self.gradient_file = gradient_file
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Rectangle(source=self.gradient_file, pos=self.pos, size=self.size)

class OrdersScreen(Screen):
    def __init__(self, lang="pl", **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        self.refresh_interval = 1
        Clock.schedule_interval(self.update_orders, self.refresh_interval)
        self.build_layout()

    def build_layout(self):
        self.clear_widgets()
        root = BoxLayout(orientation="horizontal", spacing=0)
        # Lewa kolumna (tło gradient2.png)
        left = GradientBox("gradient2.png", orientation="vertical", padding=[30,20,20,20], spacing=14, size_hint_x=0.48)
        left.add_widget(Label(
            text="W trakcie przygotowania",
            font_size="36sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=64,
            halign="center"
        ))
        left.add_widget(BlinkingLabel(
            text="In preparation",
            font_size="30sp",
            bold=True,
            color=(1,1,1,1),
            halign="center",
            size_hint_y=None,
            height=54
        ))

        # Kontener 80% wysokości na zamówienia
        self.left_orders_outer = BoxLayout(orientation="vertical", size_hint_y=0.8)
        self.left_orders_grid = GridLayout(cols=2, spacing=8, padding=[0,0,0,0], size_hint_y=None)
        self.left_orders_grid.bind(minimum_height=self.left_orders_grid.setter('height'))
        self.left_orders_outer.add_widget(self.left_orders_grid)
        left.add_widget(self.left_orders_outer)

        # Środkowy box na logo.png z czarnym tłem
        logo_box = BoxLayout(orientation="vertical", size_hint_x=None, width=160, padding=[0, 30, 0, 30])
        with logo_box.canvas.before:
            Color(0, 0, 0, 1)
            self.logo_bg_rect = Rectangle(pos=logo_box.pos, size=logo_box.size)
        def update_logo_bg_rect(*args):
            self.logo_bg_rect.pos = logo_box.pos
            self.logo_bg_rect.size = logo_box.size
        logo_box.bind(pos=update_logo_bg_rect, size=update_logo_bg_rect)
        logo_img = Image(source="logo.png", allow_stretch=True, keep_ratio=True)
        logo_box.add_widget(Widget(size_hint_y=0.2))
        logo_box.add_widget(logo_img)
        logo_box.add_widget(Widget(size_hint_y=0.2))

        # Prawa kolumna (tło gradient.png)
        right = GradientBox("gradient.png", orientation="vertical", padding=[20,20,30,20], spacing=14, size_hint_x=0.48)
        right.add_widget(Label(
            text="Gotowe do odbioru",
            font_size="36sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=64,
            halign="center"
        ))
        right.add_widget(BlinkingLabel(
            text="Ready for pickup",
            font_size="30sp",
            bold=True,
            color=(1,1,1,1),
            halign="center",
            size_hint_y=None,
            height=54
        ))
        right.add_widget(BlinkingLabel(
            text="Smacznego / Enjoy Your meal",
            font_size="30sp",
            bold=True,
            color=(1, 0.843, 0, 1),  # złoty
            blink_color_1=(1,0.843,0,1),
            blink_color_2=(1,0.843,0,0.2),
            halign="center",
            size_hint_y=None,
            height=54
        ))

        # Kontener 80% wysokości na zamówienia gotowe
        self.right_orders_outer = BoxLayout(orientation="vertical", size_hint_y=0.8)
        self.right_orders_grid = GridLayout(cols=2, spacing=8, padding=[0,0,0,0], size_hint_y=None)
        self.right_orders_grid.bind(minimum_height=self.right_orders_grid.setter('height'))
        self.right_orders_outer.add_widget(self.right_orders_grid)
        right.add_widget(self.right_orders_outer)

        # Divider z animacją
        self.divider = AnimatedDivider(size_hint_x=None, width=10)

        root.add_widget(left)
        root.add_widget(logo_box)
        root.add_widget(right)
        self.add_widget(root)
        self.update_orders(0)

    def update_orders(self, dt):
        now = datetime.utcnow()
        pending_orders = get_orders(status="pending")
        ready_orders = get_orders(status="ready")
        pending_orders = sorted(pending_orders, key=lambda o: o.created_at, reverse=True)
        ready_orders = sorted(ready_orders, key=lambda o: o.ready_at or o.created_at, reverse=True)

        self.left_orders_grid.clear_widgets()
        self.right_orders_grid.clear_widgets()

        # OGRANICZENIE do 24 najnowszych zamówień!
        pending_orders = pending_orders[:24]

        for idx, order in enumerate(pending_orders):
            is_new = idx == 0 and (now - order.created_at < timedelta(seconds=30))
            card = OrderCard(order.order_number, is_new=is_new, ready=False, size_hint_y=None, height=70)
            self.left_orders_grid.add_widget(card)

        for idx, order in enumerate(ready_orders):
            ready_time = order.ready_at or order.created_at
            is_new = idx == 0 and (now - ready_time < timedelta(seconds=30))
            card = OrderCard(order.order_number, is_new=is_new, ready=True, size_hint_y=None, height=70)
            self.right_orders_grid.add_widget(card)

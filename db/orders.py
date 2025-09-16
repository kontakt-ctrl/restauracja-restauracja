from db.models import Order, OrderItem, MenuItem, get_session
from db.payments import add_payment
from datetime import datetime
import socket

def create_order(cart, language="pl", type="na_miejscu"):
    """
    Tworzy nowe zamówienie oraz odpowiedni wpis w tabeli payments.
    cart: list of dicts {menu_item_id, quantity}
    type: "na_miejscu" lub "na_wynos"
    """
    session = get_session()
    try:
        last_order = session.query(Order).order_by(Order.order_number.desc()).first()
        order_number = (last_order.order_number + 1) if last_order else 1
        order = Order(order_number=order_number, status="pending", language=language, type=type)
        session.add(order)
        session.flush()
        total_amount_cents = 0
        for item in cart:
            menu_item = session.query(MenuItem).filter_by(id=item["menu_item_id"]).first()
            if not menu_item:
                continue
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item["menu_item_id"],
                quantity=item["quantity"]
            )
            session.add(order_item)
            total_amount_cents += menu_item.price_cents * item["quantity"]
        session.commit()

        # Dodaj wpis do tabeli payments
        hostname = socket.gethostname()
        add_payment(
            hostname=hostname,
            order_number=order_number,
            amount_cents=total_amount_cents,
            status="pending",
            terminal_log="",
            description="Płatność oczekuje na realizację"
        )

        return order.id
    finally:
        session.close()

def get_orders(status=None):
    session = get_session()
    try:
        query = session.query(Order)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Order.created_at.desc()).all()
    finally:
        session.close()

def get_order_details(order_id):
    session = get_session()
    try:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            return None
        items = []
        for oi in order.items:
            items.append({
                "name": oi.menu_item.name_pl,
                "quantity": oi.quantity,
                "price_cents": oi.menu_item.price_cents
            })
        return {
            "order_number": order.order_number,
            "status": order.status,
            "created_at": order.created_at,
            "items": items
        }
    finally:
        session.close()

import escpos.printer

def print_receipt(order):
    try:
        p = escpos.printer.Usb(0x04b8, 0x0e15)
        p.text("Rachunek\n")
        for item in order.items:
            p.text(f"{item.menu_item.name_pl} x{item.quantity}  {item.menu_item.price_cents/100:.2f} PLN\n")
        p.text(f"Suma: {sum([item.menu_item.price_cents*item.quantity for item in order.items])/100:.2f} PLN\n")
        p.text(f"Numer zamówienia: {order.order_number}\n")
        p.cut()
    except Exception as e:
        print(f"Printer error: {e}")
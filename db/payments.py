from db.models import Payment, get_session
from datetime import datetime

def add_payment(hostname, order_number, amount_cents, status, terminal_log=None, description=None):
    session = get_session()
    try:
        payment = Payment(
            created_at=datetime.utcnow(),
            hostname=hostname,
            order_number=order_number,
            amount_cents=amount_cents,
            status=status,
            terminal_log=terminal_log,
            description=description
        )
        session.add(payment)
        session.commit()
        return payment.id
    finally:
        session.close()

import socket

class PaymentError(Exception):
    pass

def process_payment(amount_cents):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 10009))
        s.sendall(f'PAY;{amount_cents}\n'.encode())
        response = s.recv(1024).decode()
        s.close()
        if "APPROVED" in response:
            return True
        elif "DECLINED" in response:
            raise PaymentError("Transakcja odrzucona.")
        elif "PIN_ERROR" in response:
            raise PaymentError("Błędny PIN.")
        else:
            raise PaymentError("Błąd terminala.")
    except Exception as e:
        raise PaymentError(str(e))
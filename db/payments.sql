CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(128) NOT NULL,
    order_number INTEGER NOT NULL REFERENCES orders(order_number),
    amount_cents INTEGER NOT NULL,
    status VARCHAR(32) NOT NULL, -- np. pending/approved/declined/error
    terminal_log TEXT,
    description TEXT
);

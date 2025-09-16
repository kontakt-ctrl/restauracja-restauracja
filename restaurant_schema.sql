CREATE TABLE menu_category (
    id SERIAL PRIMARY KEY,
    name_pl VARCHAR(64) NOT NULL,
    name_en VARCHAR(64),
    name_de VARCHAR(64),
    name_fr VARCHAR(64),
    name_es VARCHAR(64),
    name_uk VARCHAR(64),
    name_cs VARCHAR(64),
    name_sk VARCHAR(64),
    name_no VARCHAR(64),
    name_sv VARCHAR(64),
    name_da VARCHAR(64),
    name_ru VARCHAR(64),
    name_zh VARCHAR(64),
    name_ja VARCHAR(64),
    name_ar VARCHAR(64),
    image_url TEXT
);

CREATE TABLE menu_item (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES menu_category(id),
    name_pl VARCHAR(128) NOT NULL,
    name_en VARCHAR(128),
    name_de VARCHAR(128),
    name_fr VARCHAR(128),
    name_es VARCHAR(128),
    name_uk VARCHAR(128),
    name_cs VARCHAR(128),
    name_sk VARCHAR(128),
    name_no VARCHAR(128),
    name_sv VARCHAR(128),
    name_da VARCHAR(128),
    name_ru VARCHAR(128),
    name_zh VARCHAR(128),
    name_ja VARCHAR(128),
    name_ar VARCHAR(128),
    price_cents INTEGER NOT NULL,
    image_url TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending', -- pending/paid/ready
    type VARCHAR(16) NOT NULL, -- 'na_miejscu', 'na_wynos'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,
    ready_at TIMESTAMP,
    language VARCHAR(8) DEFAULT 'pl'
);

CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    menu_item_id INTEGER REFERENCES menu_item(id),
    quantity INTEGER NOT NULL
);

-- Dostępy dla użytkownika pi_restaurant
CREATE USER pi_restaurant WITH PASSWORD 'securepassword';
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO pi_restaurant;
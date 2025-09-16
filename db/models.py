from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    return Session()

class MenuCategory(Base):
    __tablename__ = "menu_category"
    id = Column(Integer, primary_key=True)
    name_pl = Column(String(64), nullable=False)
    name_en = Column(String(64))
    image_url = Column(Text)
    is_available = Column(Boolean, default=True)

class MenuItem(Base):
    __tablename__ = "menu_item"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("menu_category.id"))
    name_pl = Column(String(128), nullable=False)
    name_en = Column(String(128))
    price_cents = Column(Integer, nullable=False)
    image_url = Column(Text)
    is_available = Column(Boolean, default=True)
    # DODANO SKŁADNIKI
    ingredients = Column(Text)
    category = relationship("MenuCategory")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_number = Column(Integer, unique=True, nullable=False)
    status = Column(String(32), default="pending")
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    ready_at = Column(DateTime)
    language = Column(String(8), default="pl")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"))
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    hostname = Column(String(128), nullable=False)
    order_number = Column(Integer, nullable=False)
    amount_cents = Column(Integer, nullable=False)
    status = Column(String(32), nullable=False)  # pending/approved/declined/error
    terminal_log = Column(Text)
    description = Column(Text)

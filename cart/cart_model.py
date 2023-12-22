from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default='pending')  # Status can be 'pending', 'delivered', etc.

    # Many-to-One relationship with the user who created the cart
    user_id = Column(Integer, ForeignKey('users.id'))

    # Many-to-One relationship with the user who delivered the cart
    deliverer_id = Column(Integer, ForeignKey('users.id'))

    # Many-to-Many relationship with products
    products = relationship('Product', secondary='cart_product_association', back_populates='carts')


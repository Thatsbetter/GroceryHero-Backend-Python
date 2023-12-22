class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    price = Column(Float, nullable=False)

# Association table for the many-to-many relationship between Cart and Product
cart_product_association = Table('cart_product_association', Base.metadata,
    Column('cart_id', Integer, ForeignKey('carts.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)
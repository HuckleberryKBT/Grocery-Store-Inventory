from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Mapped, mapped_column, relationship, sessionmaker)


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session=Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    product = relationship('Product', back_populates='brand')

    def __repr__(self):
        return f'''
        Brand ID: {self.brand_id}
        Brand Name: {self.brand_name}
        '''

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey('brands.brand_id'))
    brand = relationship('Brands', back_populates="product")

    def __repr__(self):
        return f'''
        ID: {self.product_id},
        Name: {self.product_name},
        Quantity: {self.product_quantity},
        Price: ${self.product_price/100}
        Last Updated: {self.date_updated}
        Brand ID: {self.brand_id}

        '''
import csv
from models import (session, Brands, Product)
from cleaners import (clean_date, clean_price)

def add_brands_from_csv():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
            if row[0] != 'brand_name' and brand_in_db == None:
                brand_name = row[0]
                new_brand = Brands(brand_name=brand_name)
                session.add(new_brand)
    session.commit()



def add_inventory_from_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            if row[0] != 'product_name':
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
                brand_id = session.query(Brands).filter(Brands.brand_name==row[4]).first().brand_id
                product_in_db = session.query(Product).filter(Product.product_name==product_name).one_or_none()
                if product_in_db == None:
                    new_product  = Product(
                        product_name=product_name,
                        product_quantity=product_quantity,
                        product_price=product_price,
                        brand_id=brand_id,
                        date_updated= date_updated
                    )
                    session.add(new_product)
                else:
                    product_in_db.product_quantity=product_quantity
                    product_in_db.product_price=product_price
                    product_in_db.date_updated = date_updated
                    product_in_db.brand_id=brand_id
    session.commit()


def backup_brands_to_csv(brands):
    with open('backup_brands.csv', 'a', newline='') as csvfile:
        fieldNames = ['brand_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        for brand in brands:
            writer.writerow({'brand_name':brand.brand_name})
        

def backup_inventory_to_csv(inventory):
    with open('backup_inventory.csv', 'a', newline='') as csvfile:
        fieldNames = ['product_name','product_price', 'product_quantity', 'date_updated', 'brand_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        for product in inventory:
            date_str = str(product.date_updated)
            split_date = date_str.split('-')
            print(split_date)
            writer.writerow({
                'product_name': product.product_name,
                'product_price': f'${product.product_price/100}',
                'product_quantity': product.product_quantity,
                'date_updated': f'{split_date[1]}/{split_date[2]}/{split_date[0]}',
                'brand_name': session.query(Brands).filter(Brands.brand_id == product.brand_id).first().brand_name
            })
        







from models import (Base, session, Brands, Product, engine)
from csvhandlers import (add_brands_from_csv, add_inventory_from_csv, backup_brands_to_csv,backup_inventory_to_csv)
from cleaners import (clean_date, clean_id,clean_quantity, clean_price)
from collections import Counter
from datetime import datetime
from sqlalchemy import func
from statistics import mean
import time



def menu():
    while True:
        print('''
            \n****Grocery Store Inventory****
            \rV) View Product Details
            \rN) Add a new product
            \rA) Inventory Analysis 
            \rB) Backup Inventory
            \rQ) Quit\n''')
        choice = input('What would you like to do? ').upper()
        if choice in ['V','N','A','B', 'Q']:
            return choice
        else:
            input('''\nPlease choose one of the options above
            \rPress enter to try again.''')


def submenu():
    while True:
        print('''
            \n1) Edit Product
            \r2) Delete Product
            \r3) Return to main menu\n''')
        choice = input('What would you like to do? ')
        if choice in ['1','2','3']:
            return choice
        else:
            input('''\nPlease choose one of the options above
            \rPress enter to try again.''')



def product_selection():
        id_options = []
        for product in session.query(Product):
            id_options.append(product.product_id)
        id_error = True
        while id_error:
            id_choice = input(f'''
                \nID options: {id_options}
                \rSelect a Product ID: ''')
            id_choice = clean_id(id_choice, id_options)
            if type(id_choice) == int:
                id_error = False
        product_selected = session.query(Product).join(Brands, Product.brand_id == Brands.brand_id).filter(Product.product_id==id_choice).first()
        print(f'''
        \nProduct Name: {product_selected.product_name}
        \rQuantity: {product_selected.product_quantity}
        \rPrice: ${product_selected.product_price/100}
        \rLast Updated: {product_selected.date_updated}
        \rBrand: {product_selected.brand.brand_name}
        ''')
        return product_selected

def add_brand(name):
    new_brand = Brands(brand_name=name)
    session.add(new_brand)
    session.commit()


def generate_date():
    now = datetime.now()
    str_date = now.strftime("%m/%d/%Y")
    date = clean_date(str_date)
    return date

def add_product():
    product_name = input('Product Name: ')
    ##Get and format quantity
    quantity_error = True
    while quantity_error:
        product_quantity = input('Product Quantity(ex. 24): ')
        product_quantity = clean_quantity(product_quantity)
        if type(product_quantity) == int:
            quantity_error = False
    ##Get and format price
    price_error = True
    while price_error:
        product_price = input('Product Price(ex. $10.99) : ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
    #Get brand name, check if it exists, and create the brand in our brands table if not
    brand_name = input('Brand Name: ')
    brand_name_in_db = session.query(Brands).filter(Brands.brand_name == brand_name).one_or_none()
    if brand_name_in_db == None:
        add_brand(brand_name)
    brand_id = brand_name_in_db = session.query(Brands).filter(Brands.brand_name == brand_name).first().brand_id
    #Create and format date for today
    date_updated = generate_date()
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


def analyze_inventory():
    data = session.query(Product).order_by(Product.product_price).all()
    least_expensive_item = data[0]
    most_expensive_item = data[len(data)-1]
    product_prices = []
    product_quantities = []
    brand_ids = []
    for item in data:
        brand_ids.append(item.brand_id)
        product_prices.append(item.product_price)
        product_quantities.append(item.product_quantity)
    id_data = Counter(brand_ids)
    most_common_brand_id = id_data.most_common(1)[0][0]
    most_common_brand = session.query(Brands).filter(Brands.brand_id == most_common_brand_id).first().brand_name
    print(f'The most_common brand is {most_common_brand}')
    print(f'The most expensive item is: {most_expensive_item}')
    print(f'The least expensive item is: {least_expensive_item}')
    print(f'The average amount of inventory for each product is: {mean(product_quantities)}')
    print(f'The average cost of products in your inventory is: ${mean(product_prices)/100}')


def edit_product(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == "Product Price":
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Brand Name':
        brand_name = session.query(Brands).filter(Brands.brand_id == current_value).first().brand_name
        print(f'Current Value: {brand_name}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == "Product Price":
        while True:
            changes = input('What would you like to change the value to? ')
            changes = clean_price(changes)
            if type(changes) == int:
                return changes
    elif column_name == "Brand Name":
        while True:
                edited_brand_name = input('What would you like to change the value to? ')
                edited_brand_in_db = session.query(Brands).filter(Brands.brand_name == edited_brand_name).one_or_none()
                if edited_brand_in_db == None:
                    add_brand(edited_brand_name)
                    brand_id = brand_name_in_db = session.query(Brands).filter(Brands.brand_name == edited_brand_name).first().brand_id
                    return brand_id
                else:
                    brand_id = brand_name_in_db = session.query(Brands).filter(Brands.brand_name == edited_brand_name).first().brand_id
                    return brand_id
            
    else:
        return input('What would you like to change the value to? ')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            product = product_selection()
            time.sleep(1.5)
            sub_choice = int(submenu())
            if sub_choice == 1:
                product.product_name = edit_product('Product Name', product.product_name)
                product.product_price = edit_product('Product Price', product.product_price)
                product.product_quantity = edit_product("Product Quantity", product.product_quantity)
                product.brand_id = edit_product('Brand Name', product.brand_id)
                product.date_updated = generate_date()
                session.commit()
                print('Product updated!')
            elif sub_choice == 2:
                session.delete(product)
                session.commit()
                print('Product deleted!')
        
        elif choice == 'N':
            add_product()
        elif choice == 'A':
            analyze_inventory()
        elif choice == 'B':
            db_brands = session.query(Brands).all()
            db_inventory = session.query(Product).all()
            backup_brands_to_csv(db_brands)
            backup_inventory_to_csv(db_inventory)
        else:
            return




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_brands_from_csv()
    add_inventory_from_csv()
    app()
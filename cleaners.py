import datetime

#clean price
def clean_price(price_str):
    try:
        split_price = price_str.split('$')
        if len(split_price) != 1:
            price_float = float(split_price[1])
        else:
            raise ValueError
    except ValueError:
        input('''
            \n**********PRICE ERROR **********
            \rThe price should be a number with a currency symbol
            \rEX: $10.99
            \rPress enter to try again
            \r*******************************''')
        return
    else:
        return int(price_float * 100)


# clean date
def clean_date(date_str):
    try:
        split_date = date_str.split("/")
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date =  datetime.date(year, month, day)

    except ValueError:
        input('''
            \n**********DATE ERROR **********
            \rThe date format should include a valid month, date, and year in the past, separated by a forward slash
            \rEX: 2/3/2023
            \rPress enter to try again
            \r*******************************''')
        return
    else:
        return return_date


#clean id
def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
            \n**********ID ERROR **********
            \rThe ID should be a number
            \rPress enter to try again
            \r*******************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n**********ID ERROR **********
            \r The ID should be a valid selection from the list below
            \rOptions: {options}
            \rPress enter to try again
            \r*******************************''')
            return

def clean_quantity(value):
    try:
        quantity = int(value)
    except ValueError:
        input('''
            \n**********Quantity ERROR **********
            \rThe Quantity should be a number
            \rPress enter to try again
            \r*******************************''')
        return
    else:
        return quantity
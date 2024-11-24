
list_shrub = ["храст", "shrub", "bush"]

def sum_positional_bush_price(*args):
    result = 0.00
    for item in args:
        if type(item) == dict and 'name' in item:
             if item['name'].lower() in list_shrub:
                result += item.get('cost', 0)

    return result


def sum_naming_bush_price(unique_set, **kwargs):
    result = 0.00
    for name, bush in kwargs.items():
        if type(bush) == dict and 'name' in bush:
            if bush['name'].lower() in list_shrub:
                for letter in name:
                    unique_set.add(letter)
                if 'cost' in bush:
                    result += bush['cost']
    return result


def function_that_says_ni(*args, **kwargs):
    price = 0.00
    price += sum_positional_bush_price(*args)
    
    unique_set = set()
    price += sum_naming_bush_price(unique_set, **kwargs)

    price_in_int = int(price)
    if 0 < price_in_int <= 42:
        if len(unique_set) % price_in_int == 0:
            return f"{price:.2f}лв"
        
    return "Ni!"

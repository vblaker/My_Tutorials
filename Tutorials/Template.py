from string import Template

class MyTemplate(Template):
    delimiter = '#'


def main():

    cart = []
    cart.append(dict(item="Coke", price_per_item=1, qty=6))
    cart.append(dict(item="Cake", price_per_item=12, qty=1))
    cart.append(dict(item="Fish", price_per_item=16, qty=4))

    t = MyTemplate("#qty x #item at #price_per_item = ")
    total = 0
    print("Cart:", cart)
    print('Number of items in the cart is: {0}'.format(len(cart)))

    for data in cart:
        print(t.substitute(data) + str(data["price_per_item"]*data["qty"]))
        total += data["price_per_item"] * data["qty"]

    print("Total: "+str(total))


if __name__ == '__main__':
    main()

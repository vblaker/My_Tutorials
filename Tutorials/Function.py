import external_modules

external_modules.fish()


def beef():
    print("First function!")


def bitcoin_to_usd(btc):
    amount = btc * 527
    print(amount)
    return amount


def get_gender(sex='Unknown'):
    if sex is 'm':
        sex = "Male"
    if sex is 'f':
        sex = "Female"
    print(sex)


# Passing arguments by keywords
def dumb_sentence(name='Vad', action='ate', item='tuna'):
    print(name, action, item)


# Unpacking arguments

def health_calculator(age, apples_ate, cigs_smoked):
    ans = (100 - age) + (apples_ate * 3.5) - (cigs_smoked * 2)
    print(ans)


data = [27, 20, 0]
# health_calculator(data[0],data[1],data[2])
health_calculator(*data)


USD = bitcoin_to_usd(3.85)
print("Bitcoins to USD amount is:", USD)

get_gender('m')
get_gender('f')
get_gender()
dumb_sentence()
dumb_sentence('Joe', 'crapped', 'cracker')


def add_number(*args):

    total = 0
    for a in args:
        total += a
    print(total)


add_number(3)
add_number(4, 5, 7)
add_number(324524, 23456345764)

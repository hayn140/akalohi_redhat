is_hot = input('Is it hot? (yes/no): ')
if is_hot == 'yes':
    is_hot = True
elif is_hot == 'no':
    is_hot = False
else:
    print('Invalid Input')
    #return None

#is_cold = input

if is_hot:
    print("It's a hot day")
    print("Drink plenty of water")
elif is_hot == False:
    print("It's a cold day")
    print("Wear warm clothes")
else:
    print("It's a lovely day")
print("Enjoy your day")

print('''


      ''')

home_price = 1000000.00
good_credit = False

if good_credit:
    print('Because you have good credit, you will need to put down 10%')
    print('Downpayment: $' + str(float(home_price) * 0.10))
else:
    print("Because you don't have good credit, you will need to put down 20%")
    print('Downpayment: $' + str(float(home_price) * 0.20))

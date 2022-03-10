from users import User
from sorts import Sort
from orders import OrderBook
from exchanges import Exchange

# Creating objects from classes
users_obj = User()
orders_obj = OrderBook()
exchange_obj = Exchange(orders_obj)
sort_obj = Sort(orders_obj, exchange_obj)

# User input for login or register
print("\n***WELCOME***\n")

while True:
    selection = input("Please enter 'reg' to register or enter 'log' to login: ").upper()

    if selection == "REG":
        user_name = users_obj.register()
        break
    elif selection == "LOG":
        user_name = users_obj.login()
        break
    else:
        print("***Warning*** \nPlease enter 'reg' or 'log'.")
        continue

if user_name != "admin":
    
    while True:
        print("What would you like to do? Please select:")
        what_to_do = input(" View Orders (v) \n New Order (n) \n Cancel Order (c) \n Replace Order (r) \n Exit (e): ").upper()

        if what_to_do == "N":
            orders_obj.new_order(user_name)
            print("Your order is created.")
        
        elif what_to_do == "V":
            orders_obj.view_orders(user_name)

        elif what_to_do == "C":
            orders_obj.cancel_order(user_name)
            print("Your order is canceled.")
            
        elif what_to_do == "R":
            orders_obj.replace_order(user_name)
            print("Your order is replaced.")
        elif what_to_do == "E":
            print("BYE!")
            exit(0)
        else:
            print("Wrong selection.")
                

elif user_name == "admin":
    while True:

        print("What would you like to do? Please select:")
        admin_to_do = input("View Buy Orders (b)\n View Sell Orders (s)\n Execute Trade (t)\n View Trade History (h) \n View Today's Trade Value (v) \n Exit(e):").upper()

        if admin_to_do == "B":
            orders_obj.view_buy_orders()
            
        elif admin_to_do == "S":
            orders_obj.view_sell_orders()
            
        elif admin_to_do == "T":
            type = input("Single match or multi match?(Please enter single or multi): ").upper()
            if type == "SINGLE":
                sort_obj.executeTrade()
            elif type == "MULTI":
                sort_obj.executeTrade(algo_type="multi")
            else: 
                print("Wrong type selected.")

        elif admin_to_do == "H":
            print(exchange_obj.view_history())

        elif admin_to_do == "V":
            print("Today's trade value: ", exchange_obj.update_todays_trade())
        
        elif admin_to_do == "E":
            print("BYE!")
            exit(0)
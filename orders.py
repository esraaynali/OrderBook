import enum
import json
from create_files import getting_orders

class OrderBook:
    def __init__(self):
        self.buy_order, self.sell_order = getting_orders()

    def new_order(self,name):
        """Creates new orders by getting stock names, price and quantity from the user

        Args:
            name (str): username
        """

        while True:
            try:  
                stock_input = input("Please enter the stock name: ").upper()
                price_input = float(input("Please enter the price: "))
                quantity_input = int(input("Please enter the quantity: "))
                order_type = input("Do you want to sell (s) or buy (b)?: ").upper()
                break
            except:
                print ("Value Error: Invalid type.")    
                continue

        #Checking order types
        if order_type == "S":

            for order in self.sell_order:
                #Check if the stock name is already stored
                if stock_input == order:
                    # append values for the key
                    self.sell_order[order]["price"].append(price_input)
                    self.sell_order[order]["quantity"].append(quantity_input)
                    self.sell_order[order]["status"].append("New Order")
                    self.sell_order[order]["username"].append(name)
                    break

                else:
                #If stock name is not in the default stocks list, update the order dictionary
                    new_order = {stock_input: {"price" : [price_input], "quantity": [quantity_input], "status" : ["New Order"], "username": [name]}}
                    self.sell_order.update(new_order)
                    break

            #Writing json files for new buy orders
            with open("sell_orders.json","w") as f:
                json.dump(self.sell_order, f, indent=4)
            
        elif order_type == "B":

            for order in self.buy_order:
                #Check if the stock name is already stored
                if stock_input == order:
                     # append values for the key
                    self.buy_order[order]["price"].append(price_input)
                    self.buy_order[order]["quantity"].append(quantity_input)
                    self.buy_order[order]["status"].append("New Order")
                    self.buy_order[order]["username"].append(name)
                    break
                else:
                #If stock name is not in the default stocks list, update the order dictionary
                    new_order = {stock_input: {"price" : [price_input], "quantity": [quantity_input], "status" : ["New Order"], "username": [name]}}
                    self.buy_order.update(new_order)
                    break

            #Writing json files with new buy orders
            with open("buy_orders.json","w") as f:
                json.dump(self.buy_order, f, indent=4)
                
        else:
            print("Wrong type entered.") 
            self.new_order()

    def order_finder(self, order_dict, name):
        """
        Finds the orders of a given username and returns their quantity and price information

        Args:
            order_dict (dict): buy or sell order dictionary
            name (str): username

        Returns:
            dict: The keys of this dict are the stock names and the values are a list of tuples that has
                    two elements which are quantity and price respectively.
        """
        personal_orders = {}
        # Creating a personal_stocks list which stores index, quantity anf price of a order
        for stock_name, order_infos in order_dict.items():
            personal_stocks = [(e, quantity, price) for e, (username, quantity, price) in\
                    enumerate(zip(order_infos["username"], order_infos["quantity"], order_infos["price"])) if username == name]
         
            if personal_stocks:
                personal_orders[stock_name] = personal_stocks
        
        return personal_orders

    def view_orders(self, name):
        """Prints the order dictionary for a given name

        Args:
            name (str): username
        """
        while True:
            type = input("Do you want to view your buy order (b) or sell order (s)?: ").upper()
            
            if type not in ["S", "B"]:
                print(f"Invalid order type please type b or s")
                continue

            if type == "S":
                print(self.order_finder(self.sell_order,name))
                break
            elif type == "B":
                print(self.order_finder(self.buy_order,name))
                break

    def order_selection(self, order_dict, stock_name, personal_orders):
        """ Sorts the personal orders and shows them to the user

        Args:
            order_dict (dict): buy or sell order dictionary
            stock_name (str): stock name that entered by the user
            personal_orders (dict): personal_orders dictionary that stores quantity and price info

        Returns:
            [tupe]: sorted orders, copy of the order dictionary
        """
        if stock_name not in personal_orders.keys():
            print(f"You haven't placed an order for {stock_name} stock!")

        else:
            print(f"*****Your orders for {stock_name}*****\n")
            print("ID Price Quantity")

            # sorting orders by price -> max to min for a better view
            sorted_orders = sorted(personal_orders[stock_name], key=lambda x: x[2], reverse=True) #2. index stores the price info
            # printing index, quantity and price info for user
            for e, (_ ,quantity, price) in enumerate(sorted_orders):
                print(f"{e}. {price} - {quantity}")
             
            cp_order = order_dict[stock_name].copy()
        
        return sorted_orders, cp_order

    def cancel_order(self,name):
        """ Asks for stock and type for cancellation and remove it from the order dictionary and creates new json file for the orders

        Args:
            name (str): username
        """

        while True:
        
            cancel_stock = input("Please enter the stock name: ").upper()
            
            cancel_type = input("Do you want to cancel your buy order (b) or sell order (s)?: ").upper()
            
            if cancel_type not in ["B", "S"]:
                print(f"Invalid order type please type b or s")
                continue

            if cancel_type == "B":
                if cancel_stock not in self.buy_order.keys():
                    print(f"Given stock name is not in available stocks - Available stocks -> {self.buy_order.keys()}")
                    continue
                
                #Finding the orders of the user
                personal_orders = self.order_finder(self.buy_order, name)
                sorted_orders, copy_order = self.order_selection(self.buy_order,cancel_stock, personal_orders)
                index = int(input("Please select order to cancel(by ID):"))  

                # Removing order by its ID with pop()
                for key, value in copy_order.items():
                    self.buy_order[cancel_stock][key].pop(sorted_orders[index][0])

                # Writing again the orders json file
                with open("buy_orders.json","w") as f:
                    json.dump(self.buy_order, f, indent=4)
                break
        
            elif cancel_type == "S":
                if cancel_stock not in self.sell_order.keys():
                    print(f"Given stock name is not in available stocks - Available stocks -> {self.sell_order.keys()}")
                    continue

                personal_orders = self.order_finder(self.sell_order, name)
                sorted_orders, copy_order = self.order_selection(self.sell_order,cancel_stock, personal_orders)                
                index = int(input("Please select order to cancel(by ID):"))
                
                for key, value in copy_order.items():
                    self.sell_order[cancel_stock][key].pop(sorted_orders[index][0]) 
                
                with open("sell_orders.json","w") as f:
                    json.dump(self.sell_order, f, indent=4)
             
                break
        
    def update_selection(self, replace_stock, order_dict,name):
        """Updates the order dictionary

        Args:
            replace_stock (str): stock name
            order_dict (dict): order dictionary
            name (str): username

        Returns:
            [dict]: updated order dictionary
        """

        if replace_stock not in order_dict.keys():
            print(f"Given stock name is not in available stocks - Available stocks -> {order_dict.keys()}")
            
        # #Finding the orders of the user 
        personal_orders = self.order_finder(order_dict, name)
        sorted_orders, copy_order = self.order_selection(order_dict,replace_stock, personal_orders)                

        if replace_stock not in personal_orders.keys():
            print(f"You haven't placed an order for {replace_stock} stock!")
            

        else:     
            index = int(input("Please select order to replace(by ID):"))   
            # Getting new quantity and price for the replacement          
            replace_quant = int(input("Please enter the new quantity:"))
            replace_price = float(input("Please enter the new price:"))               
            
            for key, value in copy_order.items():
                # Replacing quantity
                if key == "quantity":
                    order_dict[replace_stock][key][sorted_orders[index][0]] = replace_quant
                # Replacing price
                if key == "price":
                    order_dict[replace_stock][key][sorted_orders[index][0]] = replace_price

        return order_dict    

    def replace_order(self,name):
        """Replaces orders and updates json files for orders

        Args:
            name (str): username
        """
        while True:
            replace_stock = input("Please enter the stock name: ").upper()
            replace_type = input("Do you want to replace your buy order (b) or sell order (s)?: ").upper()

            if replace_type not in ["B", "S"]:
                print(f"Invalid order type please type b or s")
                continue

            if replace_type == "B":
                # Updating orders
                self.buy_order = self.update_selection(replace_stock, self.buy_order, name)
                with open("buy_orders.json","w") as f:
                    json.dump(self.buy_order, f, indent=4)
                    break
                
            if replace_type == "S":
                self.sell_order = self.update_selection(replace_stock, self.sell_order, name)
                with open("sell_orders.json","w") as f:
                    json.dump(self.sell_order, f, indent=4)
                    break

    def view_buy_orders(self):
        """Takes buy_order dict and prints the order detail for selected stock
        """

        while True:
            stock_name = input("Please enter the stock name: ").upper()

            if stock_name not in self.buy_order.keys():
                print(f"Given stock name is not in available stocks - Available stocks -> {self.buy_order.keys()}")

            else:
                for key,value in self.buy_order.items():
                    if key == stock_name:
                        print(value)
                break
    
    def view_sell_orders(self):
        """Takes sel_order dict and prints the order detail for selected stock
        """
    
        while True:
            stock_name = input("Please enter the stock name: ").upper()

            if stock_name not in self.sell_order.keys():
                print(f"Given stock name is not in available stocks - Available stocks -> {self.sell_order.keys()}")
            
            else:
                for key,value in self.sell_order.items():
                    if key == stock_name:
                        print(value)
                break

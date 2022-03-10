import csv
import json
import random
import numpy as np

random.seed(42)

def order_to_json():
    """
    Creats separate json files with default orders for buy and sell
    """

    with open("buy_orders.json","w") as f:
        json.dump(buy_order, f, indent=4)
    with open("sell_orders.json","w") as f:
        json.dump(sell_order, f, indent=4)

    print("Json files are created.")

def users_to_csv():
    """
    Creats csv file with default users
    """

    try:
        with open("user_info.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username" , "password"])
            for key, value in users.items():
                writer.writerow([key, value["password"]])
    except PermissionError as e:
        print(f"{e} -> Please make sure your csv file is closed on your system.")

def fill_order_dicts(order_dict):
    """Adds 1000 orders to buy and sell order dictionary(500 each)

    Args:
        order_dict ([dict]): order dictionary
    """
    num_of_orders = 10
    for stock_name in stocks:
        order_dict[stock_name] = {"price" : [], "quantity": [], "status" : ["New Order"], "username" : []}

    for i in range(num_of_orders):
        for stock_name in stocks:
            order_dict[stock_name]["price"].append(round(np.random.normal(100,1),2))
            order_dict[stock_name]["quantity"].append(random.randrange(1, 200))
            order_dict[stock_name]["status"].append("New Order")
            order_dict[stock_name]["username"].append(random.choice(list(users.keys())))

# Dummy users
users = {"admin": {"password": "adminpass"},
    "esra": {"password" : "1234"},
    "user1" : {"password" : "1234"},
    "user2" : {"password" : "1234"},
    "user3" : {"password" : "1234"}}

buy_order, sell_order = {}, {}
stocks = ["AAPL","MSFT","GOOG","AMZN","TSLA","FB","PG","TSM","NVDA","UNH",
          "JNJ","JPM","BAC","HD","WMT","BABA","XOM","PFE","ASML","DIS",
          "MA","CSCO","ADBE","CVX","PEP","ABBV","LLY","TM","NFLX","CRM",
          "ABT","ORCL","NKE","TMO","NTES","VZ","NVO","COST","ACN","WFC",
          "MRK","DHR","INTC","NVS","PYPL","MCD","QCOM","AZN","MS","UPS"]

def getting_orders():
    #Loads buy orders
    with open('buy_orders.json') as f:
            buy_order = json.load(f)
    
    #Loads sell orders
    with open('sell_orders.json') as f:
            sell_order = json.load(f)

    return buy_order, sell_order

def getting_users():
    #Loads user infos
    reader = csv.DictReader(open("user_info.csv"))
    user_file = {}
    for row in reader:
        key = row.pop("username")
        if key in user_file:
            pass
        user_file[key] = row
    return user_file

"""Those commands are commented out because no need to create new files."""
# #create csv for users
# users_to_csv()

# #add 500 order each
# fill_order_dicts(buy_order)
# fill_order_dicts(sell_order)

# #create json files for buy orders and sell orders
# order_to_json()